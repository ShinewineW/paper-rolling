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
