# .claude/skills/paper-landscape/scripts/hub.py
"""Hub-spoke orchestration (§5 / 中枢-D1 / 中枢-D2 / 吸收-D3/D4).

The HUB is the single ledger writer. It performs NO analysis. Per tick it:
  1. discovers a ranked candidate pool (over-pulled to >= 2*N — 中枢-D2),
  2. removes ledger skip-set keys (version-aware idempotency),
  3. dispatches spokes (max N concurrent across papers; serial within a paper —
     the spoke itself enforces branch2->branch1 ordering),
  4. counts only 'done' papers toward N; on failure it quarantines to _failed/
     and backfills the next pool candidate until N done or the pool is exhausted,
  5. (Task 3+) runs a bounded watchdog that re-fires stalled / falsely-claimed
     -done work (bounded by N — never a daemon).

All ledger writes go through ``ledger.record(...)``; spokes never write the
ledger (single-writer, avoids YAML corruption — logging.md).
"""

from __future__ import annotations

import inspect
import re
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from scripts.campaign import gate_needed, load_campaign
from scripts.landscapes import LandscapeResult, generate_landscapes
from scripts.paths import FAILURE_STALLED, VAULT_BRANCH_PATH_FIELDS

FAILED_REL = Path("_failed")


@dataclass(frozen=True)
class SpokeResult:
    """Outcome of one paper's spoke pipeline (ingest->...->G2/G3->branches)."""

    status: str  # "done" | "failed"
    person_vault_path: str | None
    ai_package_path: str | None
    failure_class: str | None
    failure_reason: str | None
    source_url: str | None
    attempted_tier: str | None


@dataclass(frozen=True)
class HubResult:
    done_count: int
    failed_count: int
    exhausted: bool


class Ledger(Protocol):  # structural — the real corpus-ledger satisfies this
    def skip_set(self) -> set[str]: ...
    def record(
        self,
        key: str,
        *,
        status: str,
        failure_class: str | None = ...,
        person_vault_path: str | None = ...,
        ai_package_path: str | None = ...,
    ) -> None: ...
    def entries(self) -> list[dict]: ...
    def non_done_keys(self) -> list[str]: ...
    def consistency_check(self) -> list[str]: ...


DiscoverFn = Callable[[str, int], list[dict]]
# A spoke takes a candidate and optionally a `cancel` threading.Event (the
# production spoke accepts it; ad-hoc test spokes may omit it — see
# _run_spoke_guarded, which passes it only when the signature accepts it).
SpokeFn = Callable[..., SpokeResult]


def _safe_key(raw: str) -> str:
    """Filesystem- and ledger-safe form of an identity string.

    A DOI fallback contains '/' (e.g. ``10.1234/example.paper``) and a title
    fallback contains spaces, so the raw value cannot be used directly as a
    ``_failed/{key}.md`` filename or a ledger row key. Map any char outside
    ``[A-Za-z0-9._-]`` to '_' so the key is path-safe and stable (Codex
    Round-14: a DOI-only failure crashed the tick with FileNotFoundError when the
    '/' was treated as a path separator).
    """
    return re.sub(r"[^A-Za-z0-9._-]+", "_", raw).strip("_") or "unknown"


def _candidate_key(candidate: dict) -> str:
    """Round 2 F7: derive the ledger/skip key from candidate identity.

    Discovery emits a plain dict and does NOT carry a `key`; the hub derives one
    (arxiv_id preferred, doi fallback) and attaches it at intake. A pre-attached
    `key` (e.g. a test fixture) is honored for determinism. The result is always
    filesystem-safe (see ``_safe_key``).
    """
    return _safe_key(
        candidate.get("key")
        or candidate.get("arxiv_id")
        or candidate.get("doi")
        or candidate.get("title", "unknown")
    )


def _quarantine(workspace: Path, candidate: dict, result: SpokeResult) -> None:
    """Write a small tracked _failed/ record for manual hand-off (中枢-D2)."""
    failed_dir = Path(workspace) / FAILED_REL
    failed_dir.mkdir(parents=True, exist_ok=True)
    key = _candidate_key(candidate)  # Round 1/2 F7: derived, not a discovery field
    lines = [
        f"# FAILED: {key}",
        "",
        f"- arxiv_id: {candidate.get('arxiv_id', key)}",
        f"- title: {candidate.get('title', '')}",
        f"- failure_class: {result.failure_class}",
        f"- failure_reason: {result.failure_reason}",
        f"- source_url: {result.source_url or candidate.get('source_url', '')}",
        f"- attempted_tier: {result.attempted_tier}",
        f"- failed_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}",
        "",
    ]
    (failed_dir / f"{key}.md").write_text("\n".join(lines), encoding="utf-8")


def _is_truly_done(record: dict) -> bool:
    """A 'done' ledger record is only trustworthy if both vault paths exist.

    'non-done-but-claimed-done' (吸收-D3): status=='done' yet a vault path is
    missing — the spoke lied/crashed mid-emit. Such records are re-fired.

    Iterates the centralized branch set (paths.VAULT_BRANCH_PATH_FIELDS, ADR-0002)
    so adding an output branch extends this check automatically.
    """
    return record.get("status") == "done" and all(
        bool(record.get(field)) for field in VAULT_BRANCH_PATH_FIELDS
    )


class Watchdog:
    """Bounded re-fire on stall or false-done (吸收-D3).

    NOT a daemon: it re-fires at most ``max_refires`` times total and only while
    the tick is still short of N. False-done records (claimed done, missing vault
    paths) are re-fired in place; ``stall_seconds`` is the wall-clock stall
    threshold used by the real harness (0 in tests → re-fire immediately).
    """

    def __init__(self, *, stall_seconds: int = 1200, max_refires: int = 5) -> None:
        self.stall_seconds = stall_seconds
        self.max_refires = max_refires

    def recover(
        self,
        *,
        workspace: Path,
        ledger: Ledger,
        spoke: SpokeFn,
        queue: list[dict],
        n_target: int,
        done_so_far: int,
    ) -> int:
        """Re-fire false-done papers; return number brought to true-done.

        Bounded by ``max_refires`` total spoke re-fires AND by N (stops once the
        tick reaches N). A persistently false-done paper consumes the re-fire
        budget rather than looping forever.
        """
        by_key = {c["key"]: c for c in queue}
        recovered = 0
        refires = 0
        done = done_so_far
        while done < n_target and refires < self.max_refires:
            # False-done = recorded 'done' but missing a vault path.
            suspect = [
                r["key"]
                for r in ledger.entries()
                if r.get("status") == "done" and not _is_truly_done(r)
            ]
            if not suspect:
                break
            key = suspect[0]
            candidate = by_key.get(key)
            if candidate is None:
                break
            refires += 1
            # Same per-paper isolation as the main dispatch (Codex Round-15): a
            # hung/crashing spoke on the re-fire path must not abort/hang the tick.
            result = _run_spoke_guarded(spoke, candidate, stall_seconds=self.stall_seconds)
            if result.status == "done" and result.person_vault_path and result.ai_package_path:
                ledger.record(
                    key,
                    status="done",
                    person_vault_path=result.person_vault_path,
                    ai_package_path=result.ai_package_path,
                )
                recovered += 1
                done += 1
            # else: still false-done — re-checked next loop, bounded by max_refires.
        return recovered


def _run_spoke_guarded(
    spoke: SpokeFn, candidate: dict, *, stall_seconds: int | None
) -> SpokeResult:
    """Run one paper's spoke ISOLATED from the tick (中枢-D2 failure isolation).

    Bounds the spoke to ``stall_seconds`` wall-clock via a daemon worker thread
    and catches any unexpected exception, so a hung or crashing spoke can never
    abort the unattended /loop tick — it becomes a failed SpokeResult the hub
    quarantines + back-fills. ``stall_seconds`` None/<=0 means no wall-clock cap
    (the spoke's own injected seams enforce their timeouts). The synchronous
    reference uses one worker; the production harness fans spokes out concurrently
    with the same per-paper budget (Codex Round-14).
    """
    box: dict[str, object] = {}
    # Stall-abort signal: SET on timeout so a late-finishing daemon spoke aborts
    # before promoting to the vault (Codex R17). Passed only to spokes that accept
    # it, so ad-hoc test spokes `def spoke(cand)` keep working.
    cancel = threading.Event()
    accepts_cancel = "cancel" in inspect.signature(spoke).parameters

    def _worker() -> None:
        try:
            box["result"] = spoke(candidate, cancel=cancel) if accepts_cancel else spoke(candidate)
        except Exception as exc:  # noqa: BLE001 — per-paper isolation; never abort the tick
            box["error"] = exc

    worker = threading.Thread(target=_worker, daemon=True)
    worker.start()
    worker.join(timeout=stall_seconds if stall_seconds and stall_seconds > 0 else None)

    src = candidate.get("oa_pdf_url") or candidate.get("source_url")
    if worker.is_alive():
        # Still running past the budget — abandon it (the daemon dies at process
        # exit) and move on so the tick keeps making progress. Signal cancel so a
        # late finisher does NOT promote products after we record this paper failed.
        cancel.set()
        return SpokeResult(
            status="failed",
            person_vault_path=None,
            ai_package_path=None,
            failure_class=FAILURE_STALLED,
            failure_reason=f"spoke exceeded the {stall_seconds}s wall-clock budget",
            source_url=src,
            attempted_tier=None,
        )
    if "error" in box:
        exc = box["error"]
        return SpokeResult(
            status="failed",
            person_vault_path=None,
            ai_package_path=None,
            failure_class=FAILURE_STALLED,
            failure_reason=f"spoke raised {type(exc).__name__}: {exc}",
            source_url=src,
            attempted_tier=None,
        )
    return box["result"]  # type: ignore[return-value]


def run_tick(
    *,
    workspace: Path,
    topic: str,
    n_target: int,
    ledger: Ledger,
    discover: DiscoverFn,
    spoke: SpokeFn,
    max_concurrent: int = 5,
    watchdog: Watchdog | None = None,
) -> HubResult:
    """Process one /loop tick: dispatch + skip + backfill until N done or pool out.

    Spokes run serial here (deterministic, testable); the real harness fans them
    out via the Agent/Task tool up to ``max_concurrent`` papers in parallel. N is
    the count of SUCCESSFUL papers (中枢-D2), not attempts. A claimed-done result
    with missing vault paths is recorded but NOT counted (吸收-D3) — the watchdog
    re-fires it.
    """
    pool = discover(topic, n_target)
    skip = ledger.skip_set()
    for c in pool:
        c.setdefault(
            "key", _candidate_key(c)
        )  # Round 2 F7: hub derives + attaches key (discovery does not emit it)
    # Force-include (中枢-D1): every NOT-already-done force-included paper must be
    # ATTEMPTED this tick, so raise the target to cover them even if there are more
    # forced papers than the per-tick N. They sit at the front of the pool. Count
    # only un-skipped forced so already-done forced papers don't inflate the
    # discovered backfill.
    forced_pending = sum(1 for c in pool if c.get("forced") and c["key"] not in skip)
    n_target = max(n_target, forced_pending)
    queue = [c for c in pool if c["key"] not in skip]

    stall_seconds = watchdog.stall_seconds if watchdog is not None else None
    done = 0
    failed = 0
    for candidate in queue:
        if done >= n_target:
            break
        # Per-paper isolation (中枢-D2): a hung or crashing spoke must not abort
        # the unattended tick — it becomes a failed result we quarantine + backfill.
        result = _run_spoke_guarded(spoke, candidate, stall_seconds=stall_seconds)
        if result.status == "done" and result.person_vault_path and result.ai_package_path:
            ledger.record(
                candidate["key"],
                status="done",
                person_vault_path=result.person_vault_path,
                ai_package_path=result.ai_package_path,
            )
            done += 1
        elif result.status == "done":
            # Claimed done but vault paths missing — record so the watchdog can
            # detect & re-fire; does NOT count toward N (吸收-D3).
            ledger.record(
                candidate["key"],
                status="done",
                person_vault_path=result.person_vault_path,
                ai_package_path=result.ai_package_path,
            )
        else:
            ledger.record(candidate["key"], status="failed", failure_class=result.failure_class)
            _quarantine(workspace, candidate, result)
            failed += 1

    if watchdog is not None and done < n_target:
        done += watchdog.recover(
            workspace=workspace,
            ledger=ledger,
            spoke=spoke,
            queue=queue,
            n_target=n_target,
            done_so_far=done,
        )

    exhausted = done < n_target
    return HubResult(done_count=done, failed_count=failed, exhausted=exhausted)


class GateRequired(RuntimeError):
    """Raised when a /loop tick is attempted before the campaign Hard Gate.

    The harness catches this and runs the HITL campaign-setup flow (SKILL.md):
    confirm topic + N, write config/campaign.yaml, then retry the tick.
    """


@dataclass(frozen=True)
class TickResult:
    hub: HubResult
    landscape: LandscapeResult


def run_campaign_tick(
    *,
    workspace: Path,
    ledger: Ledger,
    discover: DiscoverFn,
    spoke: SpokeFn,
    requested_topic: str | None = None,
    requested_n: int | None = None,
    max_concurrent: int = 5,
    watchdog: Watchdog | None = None,
) -> TickResult:
    """One /loop tick end-to-end: gate-check -> dispatch batch -> rebuild landscape.

    On an established campaign with no topic/N change this runs fully autonomously
    (no re-gate, no mid-pipeline questions — 中枢-D2 / 吸收-D4). If no campaign is
    locked (or topic/N changed), raises GateRequired so the harness runs the HITL
    setup gate first.
    """
    if gate_needed(workspace, requested_topic=requested_topic, requested_n=requested_n):
        raise GateRequired(
            "campaign Hard Gate required: confirm topic + per-tick N "
            "(write config/campaign.yaml) before processing"
        )
    cfg = load_campaign(workspace)
    assert cfg is not None  # gate_needed False guarantees a locked config
    # LS-4 startup consistency self-heal: demote any `done` ledger row whose
    # person_vault or ai_package half is missing on disk, so the key leaves the
    # skip-set and is reprocessed this tick (ledger↔FS drift self-heal). Runs
    # AFTER the gate passes and BEFORE the batch dispatch.
    ledger.consistency_check()
    if watchdog is None:
        watchdog = Watchdog()
    hub = run_tick(
        workspace=workspace,
        topic=cfg.topic,
        n_target=cfg.n_per_tick,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
        max_concurrent=max_concurrent,
        watchdog=watchdog,
    )
    landscape = generate_landscapes(workspace, topic=cfg.topic)
    return TickResult(hub=hub, landscape=landscape)
