from __future__ import annotations

import pytest
from scripts.audit.types import (
    ClaimRecord,
    ClaimType,
    Finding,
    GateOutcome,
    GateVerdict,
    Severity,
)


def test_severity_ordering_critical_is_highest() -> None:
    assert Severity.CRITICAL.rank > Severity.MAJOR.rank
    assert Severity.MAJOR.rank > Severity.MINOR.rank
    assert Severity.MINOR.rank > Severity.SUGGESTION.rank


def test_gate_verdict_blocked_requires_at_least_one_hard_finding() -> None:
    hard = Finding(
        finding_id="F01",
        severity=Severity.CRITICAL,
        target="evidence/tables/main.md",
        observation="fabricated number",
        is_hard_block=True,
    )
    verdict = GateVerdict(gate="G2", findings=(hard,))
    assert verdict.blocked is True
    assert verdict.hard_findings == (hard,)


def test_gate_verdict_soft_findings_do_not_block() -> None:
    soft = Finding(
        finding_id="F02",
        severity=Severity.MINOR,
        target="logic/claims.md",
        observation="missing generalization boundary",
        is_hard_block=False,
    )
    verdict = GateVerdict(gate="G3", findings=(soft,))
    assert verdict.blocked is False
    assert verdict.hard_findings == ()


def test_gate_verdict_is_frozen() -> None:
    verdict = GateVerdict(gate="G2", findings=())
    with pytest.raises(AttributeError):
        verdict.gate = "G3"  # type: ignore[misc]


def test_claim_record_roundtrips_through_dict() -> None:
    rec = ClaimRecord(
        claim_id="C01",
        statement="Our model outperforms the baseline by 3 points.",
        claim_type=ClaimType.IMPROVEMENT,
        numbers=("3",),
        proof_experiment_ids=("E01",),
    )
    d = rec.as_dict()
    assert d["claim_id"] == "C01"
    assert d["claim_type"] == "improvement"
    assert d["numbers"] == ["3"]


def test_gate_outcome_escalated_carries_failed_path() -> None:
    out = GateOutcome(passed=False, escalated=True, rounds_used=4, failed_path="_failed/k.md")
    assert out.escalated is True
    assert out.failed_path == "_failed/k.md"
