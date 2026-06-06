"""6-dim rigor-reviewer rubric — ARA Seal Level 2 (吸收-D7).

Ports the grade map + report shape from
`AI-Research-SKILLs/22-agent-native-research-artifact/rigor-reviewer` (MIT).
The six dimensions are scored 1-5 by an injected RigorScoreFn seam (the rubric
text is held privately by the seam — ground-truth isolation, never in any
generator prompt). This module:
  - owns the deterministic grade map (mean + per-dimension floor),
  - assembles the `level2_report.json` shape,
  - sets `passes_seal2` (>= Weak Accept) which G3 turns into a hard block when
    false (audit-D1: rigor-reviewer is the cognitive terminal seal).
"""

from __future__ import annotations

from statistics import mean

from scripts.audit.types import RigorScoreFn

DIMENSION_KEYS: tuple[str, ...] = (
    "D1_evidence_relevance",
    "D2_falsifiability",
    "D3_scope_calibration",
    "D4_argument_coherence",
    "D5_exploration_integrity",
    "D6_methodological_rigor",
)

_PASSING_GRADES = frozenset({"Strong Accept", "Accept", "Weak Accept"})


def compute_grade(scores: list[int]) -> str:
    """Grade map verbatim from review-dimensions.md.

    | Strong Accept | mean >= 4.5 AND no dimension < 3 |
    | Accept        | mean >= 3.8 AND no dimension < 2 |
    | Weak Accept   | mean >= 3.0 AND no dimension < 2 |
    | Weak Reject   | mean >= 2.0 AND (mean < 3.0 OR any dimension < 2) |
    | Reject        | mean < 2.0 OR any dimension = 1 |
    """
    m = mean(scores)
    lo = min(scores)
    if m < 2.0 or lo == 1:
        return "Reject"
    if m >= 4.5 and lo >= 3:
        return "Strong Accept"
    if m >= 3.8 and lo >= 2:
        return "Accept"
    if m >= 3.0 and lo >= 2:
        return "Weak Accept"
    return "Weak Reject"


def score_rigor(
    ara_bundle: dict[str, str],
    *,
    artifact_name: str,
    rigor_scores: RigorScoreFn,
) -> dict[str, object]:
    """Run the 6-dim reviewer seam and assemble the level2_report.json dict."""
    raw = rigor_scores(ara_bundle)
    dimensions = raw["dimensions"]
    scores = [int(dimensions[k]["score"]) for k in DIMENSION_KEYS]
    grade = compute_grade(scores)
    mean_score = round(mean(scores), 2)

    return {
        "artifact": artifact_name,
        "review_version": "3.0.0",
        "prerequisite": "Level 1 passed",
        "overall": {
            "grade": grade,
            "mean_score": mean_score,
            "passes_seal2": grade in _PASSING_GRADES,
        },
        "dimensions": {k: dimensions[k] for k in DIMENSION_KEYS},
        "findings": list(raw.get("findings", [])),
    }
