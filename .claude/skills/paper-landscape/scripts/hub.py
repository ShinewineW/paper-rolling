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

import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

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


DiscoverFn = Callable[[str, int], list[dict]]
SpokeFn = Callable[[dict], SpokeResult]


def _candidate_key(candidate: dict) -> str:
    """Round 2 F7: derive the ledger/skip key from candidate identity.

    Discovery emits a plain dict and does NOT carry a `key`; the hub derives one
    (arxiv_id preferred, doi fallback) and attaches it at intake. A pre-attached
    `key` (e.g. a test fixture) is honored for determinism.
    """
    return (
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


def run_tick(
    *,
    workspace: Path,
    topic: str,
    n_target: int,
    ledger: Ledger,
    discover: DiscoverFn,
    spoke: SpokeFn,
    max_concurrent: int = 5,
) -> HubResult:
    """Process one /loop tick: dispatch + skip + backfill until N done or pool out.

    Spokes run serial here (deterministic, testable); the real harness fans them
    out via the Agent/Task tool up to ``max_concurrent`` papers in parallel. N is
    the count of SUCCESSFUL papers (中枢-D2), not attempts.
    """
    pool = discover(topic, n_target)
    skip = ledger.skip_set()
    for c in pool:
        c.setdefault(
            "key", _candidate_key(c)
        )  # Round 2 F7: hub derives + attaches key (discovery does not emit it)
    queue = [c for c in pool if c["key"] not in skip]

    done = 0
    failed = 0
    for candidate in queue:
        if done >= n_target:
            break
        result = spoke(candidate)
        if result.status == "done":
            ledger.record(
                candidate["key"],
                status="done",
                person_vault_path=result.person_vault_path,
                ai_package_path=result.ai_package_path,
            )
            done += 1
        else:
            ledger.record(candidate["key"], status="failed", failure_class=result.failure_class)
            _quarantine(workspace, candidate, result)
            failed += 1

    exhausted = done < n_target
    return HubResult(done_count=done, failed_count=failed, exhausted=exhausted)
