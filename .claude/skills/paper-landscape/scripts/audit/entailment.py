"""Type-aware entailment table check (吸收-D8, from review-dimensions.md D1).

For each claim, its type dictates the experiment design that can substantively
support it:

    causal          -> isolating ablation
    generalization  -> heterogeneous test conditions
    improvement     -> baseline comparison
    descriptive     -> representative sampling
    scoping         -> declared bounds

The actual semantic judgement (does the linked experiment exhibit the required
design?) is delegated to an injected EntailmentJudgeFn seam — production wires
it to an LLM invocation that holds the rubric privately (ground-truth
isolation); tests pass a deterministic fake. A type-mismatch (claim asserts a
type whose linked experiment lacks the required design) is a MAJOR hard block
per audit-D1.
"""

from __future__ import annotations

from collections.abc import Mapping

from scripts.audit.types import (
    ClaimRecord,
    ClaimType,
    EntailmentJudgeFn,
    Finding,
    GateVerdict,
    Severity,
)

REQUIRED_DESIGN: dict[ClaimType, str] = {
    ClaimType.CAUSAL: "ablation",
    ClaimType.GENERALIZATION: "heterogeneous test conditions",
    ClaimType.IMPROVEMENT: "baseline",
    ClaimType.DESCRIPTIVE: "representative sampling",
    ClaimType.SCOPING: "declared bounds",
}


def required_design_for(claim_type: ClaimType) -> str:
    """The experiment design a claim of this type needs (empty for UNKNOWN)."""
    return REQUIRED_DESIGN.get(claim_type, "")


def check_entailment(
    claims: tuple[ClaimRecord, ...],
    experiments: Mapping[str, str],
    *,
    judge: EntailmentJudgeFn,
) -> GateVerdict:
    """Run the type-aware entailment check over claims with proof experiments."""
    findings: list[Finding] = []
    counter = 0
    for claim in claims:
        if not claim.proof_experiment_ids:
            continue  # un-proven claims are a scope/coverage matter, not entailment
        required = required_design_for(claim.claim_type)
        if not required:
            continue  # UNKNOWN type — no design requirement to enforce here
        for exp_id in claim.proof_experiment_ids:
            counter += 1
            exp_text = experiments.get(exp_id)
            if exp_text is None:
                findings.append(
                    Finding(
                        finding_id=f"EN{counter:02d}",
                        severity=Severity.MAJOR,
                        target=f"logic/claims.md:{claim.claim_id}",
                        observation=(
                            f"{claim.claim_id} cites experiment {exp_id} which "
                            f"does not exist in experiments.md"
                        ),
                        is_hard_block=True,
                        reasoning="A dangling Proof reference cannot ground the claim.",
                        suggestion=f"Add {exp_id} to experiments.md or fix the Proof reference.",
                    )
                )
                continue
            entailed, reason = judge(claim, exp_text)
            if not entailed:
                findings.append(
                    Finding(
                        finding_id=f"EN{counter:02d}",
                        severity=Severity.MAJOR,
                        target=f"logic/claims.md:{claim.claim_id}",
                        observation=(
                            f"{claim.claim_id} is a {claim.claim_type.value} claim "
                            f"but its experiment {exp_id} lacks the required "
                            f"{required!r} design"
                        ),
                        is_hard_block=True,
                        reasoning=reason or "experiment design does not match claim type",
                        suggestion=(
                            f"Add an experiment with {required!r} design for {claim.claim_id}."
                        ),
                    )
                )
    return GateVerdict(gate="G3-entailment", findings=tuple(findings))
