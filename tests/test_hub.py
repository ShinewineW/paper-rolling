# tests/test_hub.py
from pathlib import Path

from scripts.hub import HubResult, SpokeResult, run_tick


class FakeLedger:
    """In-memory stand-in for the real corpus-ledger (single-writer)."""

    def __init__(self, skip: set[str] | None = None) -> None:
        self._skip = set(skip or set())
        self.records: list[dict] = []

    def skip_set(self) -> set[str]:
        return set(self._skip)

    def record(
        self, key, *, status, failure_class=None, person_vault_path=None, ai_package_path=None
    ) -> None:
        self.records.append(
            {
                "key": key,
                "status": status,
                "failure_class": failure_class,
                "person_vault_path": person_vault_path,
                "ai_package_path": ai_package_path,
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
