from __future__ import annotations

from pathlib import Path

from scripts.audit.gate_runner import run_with_budget
from scripts.audit.types import Finding, GateVerdict, Severity


def _passing() -> GateVerdict:
    return GateVerdict(gate="G3", findings=())


def _blocking() -> GateVerdict:
    return GateVerdict(
        gate="G3",
        findings=(
            Finding(
                finding_id="X01",
                severity=Severity.CRITICAL,
                target="report.md",
                observation="unresolvable anchor",
                is_hard_block=True,
            ),
        ),
    )


def test_run_with_budget_passes_first_round(tmp_path: Path) -> None:
    reemits: list[int] = []
    outcome = run_with_budget(
        _passing,
        max_rounds=3,
        on_reemit=reemits.append,
        failed_dir=tmp_path / "_failed",
        key="2026-06-05_T_170603762",
        paper_meta={"arxiv_id": "1706.03762", "title": "Transformer", "source_url": "u"},
    )
    assert outcome.passed is True
    assert outcome.escalated is False
    assert outcome.rounds_used == 1
    assert reemits == []  # no re-emit needed when round 1 passes


def test_run_with_budget_reemits_then_passes(tmp_path: Path) -> None:
    calls = {"n": 0}

    def gate() -> GateVerdict:
        calls["n"] += 1
        return _blocking() if calls["n"] == 1 else _passing()

    reemits: list[int] = []
    outcome = run_with_budget(
        gate,
        max_rounds=3,
        on_reemit=reemits.append,
        failed_dir=tmp_path / "_failed",
        key="k",
        paper_meta={"arxiv_id": "x", "title": "t", "source_url": "u"},
    )
    assert outcome.passed is True
    assert outcome.rounds_used == 2
    assert reemits == [1]  # one re-emit between round 1 (blocked) and round 2 (pass)


def test_run_with_budget_escalates_after_max_rounds(tmp_path: Path) -> None:
    failed_dir = tmp_path / "_failed"
    reemits: list[int] = []
    outcome = run_with_budget(
        _blocking,
        max_rounds=3,
        on_reemit=reemits.append,
        failed_dir=failed_dir,
        key="2026-06-05_BadPaper_999",
        paper_meta={
            "arxiv_id": "2606.99999",
            "title": "Bad Paper",
            "source_url": "https://arxiv.org/abs/2606.99999",
            "tier": "Tier2",
        },
    )
    assert outcome.passed is False
    assert outcome.escalated is True
    assert outcome.rounds_used == 3
    # exactly max_rounds-1 re-emits attempted before giving up.
    assert reemits == [1, 2]
    # quarantine record written.
    record = failed_dir / "2026-06-05_BadPaper_999.md"
    assert record.exists()
    body = record.read_text(encoding="utf-8")
    assert "2606.99999" in body
    assert "Bad Paper" in body
    assert "G3" in body
    assert "unresolvable anchor" in body
    assert outcome.failed_path == str(record)


def test_run_with_budget_does_not_loop_forever(tmp_path: Path) -> None:
    """A permanently-blocking gate terminates at exactly max_rounds invocations."""
    calls = {"n": 0}

    def gate() -> GateVerdict:
        calls["n"] += 1
        return _blocking()

    run_with_budget(
        gate,
        max_rounds=5,
        on_reemit=lambda _r: None,
        failed_dir=tmp_path / "_failed",
        key="k",
        paper_meta={"arxiv_id": "x", "title": "t", "source_url": "u"},
    )
    assert calls["n"] == 5
