# tests/test_hub.py
from pathlib import Path

import pytest
from scripts.hub import HubResult, SpokeResult, run_tick


class FakeLedger:
    """In-memory stand-in for the real corpus-ledger (single-writer)."""

    def __init__(self, skip: set[str] | None = None) -> None:
        self._skip = set(skip or set())
        self.records: list[dict] = []

    def skip_set(self) -> set[str]:
        return set(self._skip)

    def record(
        self,
        key,
        *,
        status,
        failure_class=None,
        person_vault_path=None,
        ai_package_path=None,
        retry_after=None,
    ) -> None:
        self.records.append(
            {
                "key": key,
                "status": status,
                "failure_class": failure_class,
                "person_vault_path": person_vault_path,
                "ai_package_path": ai_package_path,
                "retry_after": retry_after,
            }
        )
        # 'done' keys join the skip-set so a subsequent tick won't reprocess.
        if status == "done":
            self._skip.add(key)

    def entries(self) -> list[dict]:
        return list(self.records)

    def non_done_keys(self) -> list[str]:
        done = {r["key"] for r in self.records if r["status"] == "done"}
        return [k for k in (r["key"] for r in self.records) if k not in done]

    def _latest_by_key(self) -> dict[str, dict]:
        latest: dict[str, dict] = {}
        for r in self.records:
            latest[r["key"]] = r
        return latest

    def consistency_check(self) -> list[str]:
        """LS-4: demote any `done` row whose vault halves are missing on disk.

        Mirrors the real Ledger.consistency_check: a `done` row must have both a
        person_vault and ai_package dir present; if either is missing, append a
        `failed` row so the key leaves the skip-set and is reprocessed.
        """
        demoted: list[str] = []
        for key, row in self._latest_by_key().items():
            if row["status"] != "done":
                continue
            pv = row.get("person_vault_path")
            ai = row.get("ai_package_path")
            ok = bool(pv) and Path(pv).exists() and bool(ai) and Path(ai).exists()
            if not ok:
                demoted.append(key)
        for key in demoted:
            self.records.append(
                {
                    "key": key,
                    "status": "failed",
                    "failure_class": "convert_error",
                    "person_vault_path": None,
                    "ai_package_path": None,
                }
            )
            self._skip.discard(key)
        return demoted


def _candidate(key: str) -> dict:
    return {"key": key, "arxiv_id": key, "title": f"Paper {key}", "source_url": f"http://x/{key}"}


def _ok(cand: dict) -> SpokeResult:
    k = cand["key"]
    return SpokeResult(
        status="done",
        person_vault_path=f"person_vault/2026-06-05_{k}",
        ai_package_path=f"ai_package/2026-06-05_{k}",
        failure_class=None,
        failure_reason=None,
        source_url=cand["source_url"],
        attempted_tier="tier1",
    )


def _fail(cand: dict) -> SpokeResult:
    return SpokeResult(
        status="failed",
        person_vault_path=None,
        ai_package_path=None,
        failure_class="convert_error",
        failure_reason="both tiers failed",
        source_url=cand["source_url"],
        attempted_tier="tier2",
    )


def test_backfill_reaches_n_despite_failures(tmp_path: Path):
    # Target N=3. Pool of 7 (2-3×N over-pull). p2 and p4 fail → backfill must
    # pull replacements until 3 papers are 'done' (中枢-D2: N = successes).
    ledger = FakeLedger()
    pool = [_candidate(f"p{i}") for i in range(7)]
    failing = {"p2", "p4"}

    def spoke(cand: dict) -> SpokeResult:
        return _fail(cand) if cand["key"] in failing else _ok(cand)

    res: HubResult = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=3,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=3,
    )

    done = [r for r in ledger.records if r["status"] == "done"]
    failed = [r for r in ledger.records if r["status"] == "failed"]
    assert len(done) == 3
    assert {r["key"] for r in failed} == {"p2"}
    assert res.done_count == 3
    assert res.exhausted is False


def test_force_include_all_attempted_even_above_n(tmp_path: Path):
    # 3 force-included papers but n_target=1 — the hub raises the target so EVERY
    # forced paper is attempted this tick (中枢-D1), not silently capped at N.
    ledger = FakeLedger()
    pool = [{**_candidate(f"f{i}"), "forced": True} for i in range(3)]
    attempted: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        attempted.append(cand["key"])
        return _ok(cand)

    res: HubResult = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=3,
    )

    assert set(attempted) == {"f0", "f1", "f2"}
    assert res.done_count == 3


def test_force_include_already_done_does_not_inflate_target(tmp_path: Path):
    # f0 is forced but already in the skip-set (processed a prior tick). The hub
    # must count only NOT-done forced when bumping n_target, so a done forced
    # paper does not pull extra discovered backfill. With n_target=1 and one
    # pending forced (f1), exactly one paper is attempted — f1, the un-skipped
    # forced — and the discovered spares (d0/d1) are not touched.
    ledger = FakeLedger(skip={"f0"})
    pool = [
        {**_candidate("f0"), "forced": True},
        {**_candidate("f1"), "forced": True},
        _candidate("d0"),
        _candidate("d1"),
    ]
    attempted: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        attempted.append(cand["key"])
        return _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=2,
    )
    assert attempted == ["f1"]  # f0 skipped (done), target not inflated past 1
    assert res.done_count == 1


def test_force_include_failure_backfills_from_discovery(tmp_path: Path):
    # 中枢-D1/D2 interaction (pins the intended budget semantics): with n_target=1
    # and 2 pending forced, the hub bumps the target to 2 (attempt all forced). f0
    # FAILS ingest (forced ≠ gate-exempt) and is quarantined; the tick then
    # backfills from the discovered spares to reach the bumped target of 2 — so a
    # failed forced paper costs one discovered slot, it does not silently shrink N.
    ledger = FakeLedger()
    pool = [
        {**_candidate("f0"), "forced": True},
        {**_candidate("f1"), "forced": True},
        _candidate("d0"),
        _candidate("d1"),
    ]
    attempted: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        attempted.append(cand["key"])
        return _fail(cand) if cand["key"] == "f0" else _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=2,
    )
    assert "f0" in attempted and "f1" in attempted  # both forced attempted
    assert "d0" in attempted  # discovery backfilled the failed forced slot
    assert "d1" not in attempted  # bumped target (2) met — no over-pull past it
    assert {r["key"] for r in ledger.records if r["status"] == "failed"} == {"f0"}
    assert res.done_count == 2  # f1 + d0


def test_skip_set_papers_not_reprocessed(tmp_path: Path):
    # p0 already done in the ledger skip-set → never dispatched this tick.
    ledger = FakeLedger(skip={"p0"})
    pool = [_candidate(f"p{i}") for i in range(5)]
    dispatched: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        dispatched.append(cand["key"])
        return _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=2,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=2,
    )
    assert "p0" not in dispatched
    assert res.done_count == 2


def test_pool_exhausted_reports_exhausted(tmp_path: Path):
    # Only 2 candidates, all fail, target N=3 → can't reach N, exhausted=True.
    ledger = FakeLedger()
    pool = [_candidate("p0"), _candidate("p1")]
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=3,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=_fail,
        max_concurrent=3,
    )
    assert res.done_count == 0
    assert res.exhausted is True
    assert len([r for r in ledger.records if r["status"] == "failed"]) == 2


# tests/test_hub.py  (append)
from scripts.hub import Watchdog  # noqa: E402


def test_watchdog_refires_on_false_done(tmp_path: Path):
    # A paper that the spoke claimed 'done' but left no vault paths (falsely
    # claimed done) must be re-fired by the watchdog, bounded by N (吸收-D3).
    ledger = FakeLedger()
    pool = [_candidate(f"p{i}") for i in range(3)]

    # First attempt for p1 returns done-but-empty (non-done-but-claimed-done);
    # the watchdog's re-fire returns a proper done.
    attempts: dict[str, int] = {}

    def spoke(cand: dict) -> SpokeResult:
        k = cand["key"]
        attempts[k] = attempts.get(k, 0) + 1
        if k == "p1" and attempts[k] == 1:
            return SpokeResult(
                status="done",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=None,
                failure_reason=None,
                source_url=cand["source_url"],
                attempted_tier="tier1",
            )
        return _ok(cand)

    wd = Watchdog(stall_seconds=0, max_refires=3)
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=3,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=3,
        watchdog=wd,
    )
    # p1 was re-fired once and then succeeded.
    assert attempts["p1"] == 2
    assert res.done_count == 3
    assert res.exhausted is False


def test_watchdog_is_bounded_not_a_daemon(tmp_path: Path):
    # If re-fires keep yielding false-done, the watchdog stops after max_refires
    # (bounded — never loops forever).
    ledger = FakeLedger()
    pool = [_candidate("p0")]
    calls = {"n": 0}

    def always_false_done(cand: dict) -> SpokeResult:
        calls["n"] += 1
        return SpokeResult(
            status="done",
            person_vault_path=None,
            ai_package_path=None,
            failure_class=None,
            failure_reason=None,
            source_url=cand["source_url"],
            attempted_tier="tier1",
        )

    wd = Watchdog(stall_seconds=0, max_refires=2)
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=always_false_done,
        max_concurrent=1,
        watchdog=wd,
    )
    # 1 initial dispatch + at most 2 re-fires = 3 spoke calls; then it gives up.
    assert calls["n"] <= 3
    assert res.exhausted is True


# tests/test_hub.py  (append)
from scripts.campaign import CampaignConfig, write_campaign  # noqa: E402
from scripts.hub import GateRequired, run_campaign_tick  # noqa: E402


def test_run_campaign_tick_blocks_when_no_campaign(tmp_path: Path):
    # First-time: no campaign config → the gate MUST block (中枢-D1).
    import pytest

    ledger = FakeLedger()
    with pytest.raises(GateRequired):
        run_campaign_tick(
            workspace=tmp_path,
            ledger=ledger,
            discover=lambda topic, n: [_candidate("p0")],
            spoke=_ok,
        )


def test_run_campaign_tick_runs_and_builds_landscape(tmp_path: Path):
    # Established campaign → /loop tick runs autonomously and regenerates the
    # landscape after the batch (no re-gate, zero mid-pipeline questions).
    write_campaign(
        tmp_path, CampaignConfig(topic="multi object tracking", n_per_tick=2, is_ad_domain=False)
    )
    ledger = FakeLedger()

    # Spoke writes a minimal ai_package entry so landscapes has something to read.
    def spoke(cand: dict) -> SpokeResult:
        k = cand["key"]
        ara = tmp_path / "ai_package" / f"2026-06-05_{k}" / "ara"
        ara.mkdir(parents=True, exist_ok=True)
        (ara / "PAPER.md").write_text(
            "---\n"
            f"title: T{k}\nyear: 2025\nkey: {k}\nschema_version: 1\n"
            "headline_metric: mota\nheadline_value: 70.0\nparams_million: 50.0\n---\n",
            encoding="utf-8",
        )
        return SpokeResult(
            status="done",
            person_vault_path=f"person_vault/2026-06-05_{k}",
            ai_package_path=f"ai_package/2026-06-05_{k}",
            failure_class=None,
            failure_reason=None,
            source_url=cand["source_url"],
            attempted_tier="tier1",
        )

    res = run_campaign_tick(
        workspace=tmp_path,
        ledger=ledger,
        discover=lambda topic, n: [_candidate(f"p{i}") for i in range(4)],
        spoke=spoke,
    )
    assert res.hub.done_count == 2
    # Landscape regenerated for the campaign topic slug.
    assert (tmp_path / "landscapes" / "multi-object-tracking" / "report.md").exists()


def test_run_campaign_tick_self_heals_stale_done_row(tmp_path: Path):
    # LS-4: a 'done' ledger row whose vault paths don't exist on disk is stale
    # (ledger↔FS drift). run_campaign_tick MUST run consistency_check before the
    # batch so the key is demoted, leaves the skip-set, and is reprocessed —
    # NOT silently skipped.
    write_campaign(
        tmp_path, CampaignConfig(topic="multi object tracking", n_per_tick=1, is_ad_domain=False)
    )
    ledger = FakeLedger()
    # Pre-seed a 'done' row pointing at vault dirs that were never created.
    ledger.record(
        "p0",
        status="done",
        person_vault_path=str(tmp_path / "person_vault" / "gone_p0"),
        ai_package_path=str(tmp_path / "ai_package" / "gone_p0"),
    )
    assert "p0" in ledger.skip_set()  # stale row currently suppresses p0

    dispatched: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        k = cand["key"]
        dispatched.append(k)
        ara = tmp_path / "ai_package" / f"2026-06-05_{k}" / "ara"
        ara.mkdir(parents=True, exist_ok=True)
        (ara / "PAPER.md").write_text(
            "---\n"
            f"title: T{k}\nyear: 2025\nkey: {k}\nschema_version: 1\n"
            "headline_metric: mota\nheadline_value: 70.0\nparams_million: 50.0\n---\n",
            encoding="utf-8",
        )
        return SpokeResult(
            status="done",
            person_vault_path=f"person_vault/2026-06-05_{k}",
            ai_package_path=f"ai_package/2026-06-05_{k}",
            failure_class=None,
            failure_reason=None,
            source_url=cand["source_url"],
            attempted_tier="tier1",
        )

    res = run_campaign_tick(
        workspace=tmp_path,
        ledger=ledger,
        discover=lambda topic, n: [_candidate("p0")],
        spoke=spoke,
    )
    # The stale key was demoted (a 'failed' row appended) and reprocessed.
    assert "p0" in dispatched
    assert any(
        r["key"] == "p0" and r["status"] == "failed" for r in ledger.entries()
    )  # demoted by consistency_check
    assert res.hub.done_count == 1


def test_doi_only_failure_quarantines_with_pathsafe_key(tmp_path: Path):
    # Codex Round-14: a DOI-only candidate (arxiv_id None) derived the raw DOI as
    # its key; the '/' broke the `_failed/{key}.md` write (FileNotFoundError) and
    # crashed the tick. The key is now sanitized to a path-safe form.
    led = FakeLedger()
    cand = {"arxiv_id": None, "doi": "10.1234/example.paper", "title": "Some Paper"}
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=led,
        discover=lambda topic, n: [cand],
        spoke=_fail,
    )
    assert res.failed_count == 1  # quarantined, not crashed
    failed = list((tmp_path / "_failed").glob("*.md"))
    assert len(failed) == 1
    assert failed[0].name == "10.1234_example.paper.md"  # '/' sanitized to '_'


def test_run_tick_isolates_a_crashing_spoke(tmp_path: Path):
    # Codex Round-14 (中枢-D2 failure isolation): a spoke that raises an
    # unexpected exception must NOT abort the unattended tick — it is isolated as
    # a failure and the next candidate back-fills toward N.
    led = FakeLedger()
    pool = [_candidate("p0"), _candidate("p1")]

    def spoke(cand: dict) -> SpokeResult:
        if cand["key"] == "p0":
            raise RuntimeError("boom")  # unexpected crash mid-spoke
        return _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=led,
        discover=lambda topic, n: pool,
        spoke=spoke,
    )
    assert res.done_count == 1  # p0 crash isolated -> p1 back-filled (tick not aborted)
    assert res.failed_count == 1


def test_run_tick_isolates_a_stalled_spoke(tmp_path: Path):
    # Codex Round-14: a spoke that hangs past the watchdog's wall-clock budget
    # must NOT hang the unattended tick — it is abandoned as a failure and the
    # next candidate back-fills.
    import time as _time

    led = FakeLedger()
    pool = [_candidate("p0"), _candidate("p1")]

    def spoke(cand: dict) -> SpokeResult:
        if cand["key"] == "p0":
            _time.sleep(30)  # hang well past the 1s budget (daemon thread; abandoned)
        return _ok(cand)

    wd = Watchdog(stall_seconds=1, max_refires=0)
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=led,
        discover=lambda topic, n: pool,
        spoke=spoke,
        watchdog=wd,
    )
    assert res.done_count == 1  # p0 timed out -> failed; p1 back-filled
    assert res.failed_count == 1


def test_guarded_spoke_is_signalled_to_cancel_on_stall(tmp_path: Path):
    # Codex R17: a non-killable daemon spoke can't be force-stopped, but when the
    # guard abandons it on stall it SETS the spoke's cancel signal — so the late
    # finisher aborts before promoting to the vault (verified at the produce layer
    # in tests/output/test_produce.py). Here we pin the wiring: cancel reaches the
    # spoke and is set on timeout.
    import threading
    import time as _time

    from scripts.hub import _run_spoke_guarded
    from scripts.paths import FAILURE_STALLED

    saw: dict = {}
    finished = threading.Event()

    def slow_spoke(cand: dict, *, cancel=None) -> SpokeResult:
        saw["cancel_obj"] = cancel
        _time.sleep(0.5)  # overrun the 0.15s budget so the guard abandons us
        saw["set_after_timeout"] = cancel.is_set()
        finished.set()
        return _ok(cand)

    res = _run_spoke_guarded(slow_spoke, _candidate("p0"), stall_seconds=0.15)
    assert res.status == "failed"
    assert res.failure_class == FAILURE_STALLED
    assert finished.wait(3.0)  # let the abandoned daemon run to completion
    assert saw["cancel_obj"] is not None  # the spoke received a cancel signal...
    assert saw["set_after_timeout"] is True  # ...and the guard set it on timeout


def test_watchdog_recover_isolates_a_crashing_refire(tmp_path: Path):
    # Codex Round-15: the watchdog RE-FIRE path must use the same per-paper
    # isolation as the main dispatch — a crashing re-fire spoke must NOT abort
    # the unattended tick.
    led = FakeLedger()
    pool = [_candidate("p0")]
    calls = {"n": 0}

    def spoke(cand: dict) -> SpokeResult:
        calls["n"] += 1
        if calls["n"] == 1:
            # First dispatch: claim 'done' but leave no vault paths -> false-done,
            # which the watchdog will try to re-fire.
            return SpokeResult(
                status="done",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=None,
                failure_reason=None,
                source_url=None,
                attempted_tier=None,
            )
        raise RuntimeError("refire boom")  # the re-fire crashes

    wd = Watchdog(stall_seconds=0, max_refires=2)
    # Must NOT raise — recover() isolates the crashing re-fire (bounded by max_refires).
    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=led,
        discover=lambda topic, n: pool,
        spoke=spoke,
        watchdog=wd,
    )
    assert res.exhausted is True  # p0 never truly done; tick completed without crashing


def test_run_tick_list_mode_pages_and_does_not_raise_n(tmp_path: Path):
    # 指定列表 (auto_discover=False): discover() returns the whole list but the hub
    # must respect n_target as a hard cap (pagination), NOT raise it to cover all
    # forced-pending candidates (ADR-0010).  auto_discover=True (default) keeps the
    # existing 中枢-D1 raise behaviour — tested by the tests above.
    forced = [{**_candidate(f"24{i:02d}.0000"), "forced": True} for i in range(6)]

    def discover(topic: str, n: int) -> list[dict]:
        return [dict(c) for c in forced]  # whole list, like 指定列表 discover() returns

    seen: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        seen.append(cand["key"])
        return _ok(cand)

    ledger = FakeLedger()
    run_tick(
        workspace=tmp_path,
        topic="my list",
        n_target=2,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
        auto_discover=False,
    )
    assert len(seen) == 2  # list mode respects n_target=2, does NOT raise to 6


def test_list_mode_tick_processes_only_force_include_paged_and_respects_skipset(
    tmp_path: Path,
) -> None:
    """End-to-end: auto_discover=False list-mode campaign through run_campaign_tick.

    Proves the integrated wiring load_campaign → gate_needed → run_tick is correct
    for 指定列表 mode (ADR-0010).  Four claims verified in one tick:

    1. Only force_include papers are attempted (discovery is not called for new
       candidates — the fake discover returns exactly the forced list).
    2. The hub pages by n_per_tick (=2): a 4-paper list produces exactly 2 done
       results; the hub does NOT raise n_target to cover all 4.
    3. skip_set is respected: one of the 4 is pre-seeded as done, so 3 are eligible
       but still only 2 are processed (paged) — the skipped paper is never attempted.
    4. No re-gate fires (the campaign is already locked).
    """
    # Four force-include papers.  _validate_force_include requires arxiv_id
    # (ingestible + identity).  Keys match the _candidate() helper's arxiv_id field.
    force_include_entries = [
        {"arxiv_id": f"24{i:02d}.0000", "title": f"Paper {i:02d}"} for i in range(4)
    ]
    write_campaign(
        tmp_path,
        CampaignConfig(
            topic="autonomous driving perception",
            n_per_tick=2,
            is_ad_domain=True,
            auto_discover=False,
            force_include=force_include_entries,
        ),
    )

    # Pre-seed "2400.0000" as already done.
    ledger = FakeLedger(skip={"2400.0000"})

    # Track which keys the spoke is called with.
    attempted: list[str] = []

    def spoke(cand: dict) -> SpokeResult:
        k = cand["key"]
        attempted.append(k)
        # Write a minimal ai_package entry so generate_landscapes doesn't fail on
        # an empty corpus.  Pattern mirrors test_run_campaign_tick_runs_and_builds_landscape.
        ara = tmp_path / "ai_package" / f"2026-06-10_{k}" / "ara"
        ara.mkdir(parents=True, exist_ok=True)
        (ara / "PAPER.md").write_text(
            "---\n"
            f"title: T{k}\nyear: 2025\nkey: {k}\nschema_version: 1\n"
            "headline_metric: acc\nheadline_value: 80.0\nparams_million: 30.0\n---\n",
            encoding="utf-8",
        )
        return SpokeResult(
            status="done",
            person_vault_path=f"person_vault/2026-06-10_{k}",
            ai_package_path=f"ai_package/2026-06-10_{k}",
            failure_class=None,
            failure_reason=None,
            source_url=cand.get("source_url"),
            attempted_tier="tier1",
        )

    # In 指定列表 mode the real discover() returns _build_forced(force_include) which
    # emits the whole force_include list tagged forced=True.  Mirror that shape.
    def discover(topic: str, n: int) -> list[dict]:
        return [
            {
                "arxiv_id": e["arxiv_id"],
                "title": e["title"],
                "source_url": f"http://arxiv.org/abs/{e['arxiv_id']}",
                "forced": True,
            }
            for e in force_include_entries
        ]

    res = run_campaign_tick(
        workspace=tmp_path,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
    )

    # Claim 1 + 2: exactly 2 papers processed (n_per_tick=2 caps the list; hub does
    # NOT raise n_target to 3 for all pending-forced papers in list mode).
    assert res.hub.done_count == 2, f"expected 2 done, got {res.hub.done_count}"
    assert len(attempted) == 2, f"expected 2 spoke calls, got {attempted}"

    # Claim 3: the pre-seeded done paper ("2400.0000") was never attempted.
    assert "2400.0000" not in attempted, "pre-done paper must be skipped"

    # Claim 4: no GateRequired was raised (the call above completed without
    # exception — this assertion is redundant but documents the intent).
    assert res.hub.exhausted is False


def test_audit_block_failure_recorded_deferred_without_note(tmp_path: Path):
    """Chunk 3.5 wiring (CR MED-2): an audit-block spoke failure records `deferred`
    (retry_after=None → enters skip_set, waits for revival) and does NOT write a
    _failed/<key>.md note — the spoke already wrote a self-contained scene. Download/
    convert failures still record `failed` + a note."""
    from scripts.paths import FAILURE_AUDIT_BLOCK

    ledger = FakeLedger()
    pool = [_candidate("p0")]

    def spoke(cand: dict) -> SpokeResult:
        return SpokeResult(
            status="failed",
            person_vault_path=None,
            ai_package_path=None,
            failure_class=FAILURE_AUDIT_BLOCK,
            failure_reason="G3 seal hard-block exhausted budget",
            source_url=cand["source_url"],
            attempted_tier="tier2",
        )

    run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=1,
    )

    rows = [r for r in ledger.records if r["key"] == "p0"]
    assert rows, "expected a ledger row for the audit-blocked paper"
    assert rows[-1]["status"] == "deferred"
    assert rows[-1]["retry_after"] is None  # no TTL → permanent skip until revival
    # audit_block does NOT write a _failed/<key>.md note (the scene is the record).
    assert not list((tmp_path / "_failed").glob("p0*.md"))


def test_run_tick_dispatches_papers_concurrently(tmp_path: Path):
    # The parallel dispatch (max_concurrent=3) runs up to 3 spokes at the SAME
    # time — a serial loop would peak at 1. Counts/back-fill are still exact.
    import threading
    import time as _time

    ledger = FakeLedger()
    pool = [_candidate(f"p{i}") for i in range(6)]
    lock = threading.Lock()
    live = {"cur": 0, "peak": 0}

    def spoke(cand: dict) -> SpokeResult:
        with lock:
            live["cur"] += 1
            live["peak"] = max(live["peak"], live["cur"])
        _time.sleep(0.05)  # hold the slot so overlap is observable
        with lock:
            live["cur"] -= 1
        return _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=6,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=3,
    )
    assert res.done_count == 6
    assert live["peak"] >= 2, "spokes ran serially — parallel dispatch is not engaged"
    assert live["peak"] <= 3, "exceeded the max_concurrent cap"


def test_run_tick_concurrency_never_overshoots_target(tmp_path: Path):
    # done + in_flight < n_target gating: with N=1 and a wide cap, only as many
    # papers as needed are dispatched — the extra pool papers are NOT attempted.
    ledger = FakeLedger()
    pool = [_candidate(f"p{i}") for i in range(5)]
    attempted: list[str] = []
    import threading

    lock = threading.Lock()

    def spoke(cand: dict) -> SpokeResult:
        with lock:
            attempted.append(cand["key"])
        return _ok(cand)

    res = run_tick(
        workspace=tmp_path,
        topic="t",
        n_target=1,
        ledger=ledger,
        discover=lambda topic, n_target: pool,
        spoke=spoke,
        max_concurrent=4,
    )
    assert res.done_count == 1
    assert attempted == ["p0"], f"overshot N=1, attempted {attempted}"


def test_run_tick_engine_abort_stops_inflight_promotion(tmp_path: Path):
    # Final-gate regression (Codex R3): under parallel dispatch a fatal EngineAbort
    # in one paper must STOP every other in-flight spoke from promoting — else the
    # executor waits for it on exit and it publishes a product the hub never ledgers.
    import threading
    import time as _time

    from scripts.paths import EngineAbort

    led = FakeLedger()
    pool = [_candidate("p0"), _candidate("p1")]
    promoted: list[str] = []
    p1_running = threading.Event()

    def spoke(cand: dict, *, cancel=None) -> SpokeResult:
        if cand["key"] == "p0":
            p1_running.wait(2)  # ensure p1 is in flight before the fatal abort
            raise EngineAbort("routed provider failed (no fallback)")
        # p1: in flight; only "promotes" (records the side effect) if not cancelled,
        # mirroring produce.py's cancel re-check around the durable vault step.
        p1_running.set()
        _time.sleep(0.1)
        if cancel is not None and cancel.is_set():
            raise RuntimeError("p1 saw the tick abort — does not promote")
        promoted.append(cand["key"])
        return _ok(cand)

    with pytest.raises(EngineAbort):
        run_tick(
            workspace=tmp_path,
            topic="t",
            n_target=2,
            ledger=led,
            discover=lambda topic, n: pool,
            spoke=spoke,
            max_concurrent=2,
        )
    assert promoted == [], "an in-flight spoke promoted after a fatal EngineAbort"


def test_run_tick_engine_abort_in_later_paper_does_not_hang(tmp_path: Path):
    # Final-gate regression (Codex R5): when a LATER-submitted paper aborts while an
    # EARLIER slow paper is still running, run_tick must set the tick abort PROMPTLY
    # (via the future done-callback) so the slow paper is cancelled — not hang
    # waiting on it. Guarded by a thread join timeout so a regression fails, not hangs.
    import threading
    import time as _time

    from scripts.paths import EngineAbort

    led = FakeLedger()
    pool = [_candidate("p0"), _candidate("p1")]
    promoted: list[str] = []

    def spoke(cand: dict, *, cancel=None) -> SpokeResult:
        if cand["key"] == "p1":
            _time.sleep(0.05)  # let p0 (the earlier future) get in flight first
            raise EngineAbort("routed provider failed (no fallback)")
        # p0: earlier + slow; promotes only if it is NEVER cancelled. The later p1
        # abort must flip its cancel so it stops well before this 2s budget elapses.
        for _ in range(200):
            if cancel is not None and cancel.is_set():
                raise RuntimeError("p0 saw the tick abort — does not promote")
            _time.sleep(0.01)
        promoted.append("p0")
        return _ok(cand)

    outcome: dict = {}

    def _run() -> None:
        try:
            run_tick(
                workspace=tmp_path, topic="t", n_target=2, ledger=led,
                discover=lambda topic, n: pool, spoke=spoke, max_concurrent=2,
            )
        except EngineAbort:
            outcome["aborted"] = True
        except BaseException as exc:  # noqa: BLE001
            outcome["error"] = exc

    th = threading.Thread(target=_run, daemon=True)
    th.start()
    th.join(timeout=5)
    assert not th.is_alive(), "run_tick HUNG on a later-paper EngineAbort"
    assert outcome.get("aborted") is True, outcome
    assert promoted == [], "the earlier in-flight spoke promoted after a later abort"
