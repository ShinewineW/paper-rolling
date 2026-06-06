from __future__ import annotations

from scripts.audit.entailment import (
    REQUIRED_DESIGN,
    check_entailment,
    required_design_for,
)
from scripts.audit.types import ClaimRecord, ClaimType


def test_required_design_table_covers_all_typed_claims() -> None:
    for ct in (
        ClaimType.CAUSAL,
        ClaimType.GENERALIZATION,
        ClaimType.IMPROVEMENT,
        ClaimType.DESCRIPTIVE,
        ClaimType.SCOPING,
    ):
        assert ct in REQUIRED_DESIGN
    assert required_design_for(ClaimType.CAUSAL) == "ablation"
    assert required_design_for(ClaimType.IMPROVEMENT) == "baseline"


def test_check_entailment_passes_when_judge_confirms() -> None:
    claim = ClaimRecord(
        claim_id="C01",
        statement="Component A causes the gain.",
        claim_type=ClaimType.CAUSAL,
        proof_experiment_ids=("E01",),
    )
    experiments = {"E01": "Ablation removing A drops accuracy by 4 points."}

    def judge(c, exp_text):
        return (True, "ablation present")

    verdict = check_entailment((claim,), experiments, judge=judge)
    assert verdict.blocked is False


def test_check_entailment_blocks_causal_claim_without_ablation() -> None:
    claim = ClaimRecord(
        claim_id="C01",
        statement="Component A causes the gain.",
        claim_type=ClaimType.CAUSAL,
        proof_experiment_ids=("E01",),
    )
    experiments = {"E01": "We observe A and the gain are correlated."}

    def judge(c, exp_text):
        return (False, "no isolating ablation; only correlation")

    verdict = check_entailment((claim,), experiments, judge=judge)
    # Type-mismatch entailment failures are MAJOR + hard-block per audit-D1.
    finding = verdict.hard_findings[0]
    assert finding.severity.value == "major"
    assert "ablation" in finding.observation
    assert verdict.blocked is True


def test_check_entailment_skips_claims_with_no_proof_experiment() -> None:
    claim = ClaimRecord(
        claim_id="C02",
        statement="The approach is elegant.",
        claim_type=ClaimType.DESCRIPTIVE,
        proof_experiment_ids=(),
    )

    def judge(c, exp_text):  # should never be called
        raise AssertionError("judge called for a claim with no proof")

    verdict = check_entailment((claim,), {}, judge=judge)
    assert verdict.blocked is False
    assert verdict.findings == ()


def test_check_entailment_blocks_when_proof_id_missing_from_experiments() -> None:
    claim = ClaimRecord(
        claim_id="C03",
        statement="Our model outperforms the baseline.",
        claim_type=ClaimType.IMPROVEMENT,
        proof_experiment_ids=("E99",),
    )

    def judge(c, exp_text):
        return (True, "")

    verdict = check_entailment((claim,), {"E01": "..."}, judge=judge)
    assert verdict.blocked is True
    assert "E99" in verdict.hard_findings[0].observation
