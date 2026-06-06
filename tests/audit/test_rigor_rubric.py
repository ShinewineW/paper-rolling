from __future__ import annotations

from scripts.audit.rigor_rubric import (
    DIMENSION_KEYS,
    compute_grade,
    score_rigor,
)


def test_dimension_keys_are_the_six_seal2_dimensions() -> None:
    assert DIMENSION_KEYS == (
        "D1_evidence_relevance",
        "D2_falsifiability",
        "D3_scope_calibration",
        "D4_argument_coherence",
        "D5_exploration_integrity",
        "D6_methodological_rigor",
    )


def test_compute_grade_strong_accept() -> None:
    assert compute_grade([5, 5, 4, 5, 4, 5]) == "Strong Accept"


def test_compute_grade_accept() -> None:
    assert compute_grade([4, 4, 4, 4, 3, 4]) == "Accept"


def test_compute_grade_weak_accept() -> None:
    assert compute_grade([3, 3, 3, 3, 3, 3]) == "Weak Accept"


def test_compute_grade_weak_reject_when_any_dim_below_two() -> None:
    # mean is high but one dimension = 1 forces Reject (any dim==1).
    assert compute_grade([5, 5, 5, 5, 5, 1]) == "Reject"


def test_compute_grade_reject_on_low_mean() -> None:
    assert compute_grade([2, 2, 1, 2, 2, 2]) == "Reject"


def test_score_rigor_builds_level2_report_shape() -> None:
    def fake_rigor(ara_bundle):
        return {
            "dimensions": {
                "D1_evidence_relevance": {
                    "score": 4,
                    "strengths": ["s"],
                    "weaknesses": [],
                    "suggestions": [],
                },  # noqa: E501
                "D2_falsifiability": {
                    "score": 4,
                    "strengths": [],
                    "weaknesses": ["w"],
                    "suggestions": ["fix"],
                },  # noqa: E501
                "D3_scope_calibration": {
                    "score": 4,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": [],
                },  # noqa: E501
                "D4_argument_coherence": {
                    "score": 4,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": [],
                },  # noqa: E501
                "D5_exploration_integrity": {
                    "score": 3,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": [],
                },  # noqa: E501
                "D6_methodological_rigor": {
                    "score": 4,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": [],
                },  # noqa: E501
            },
            "findings": [
                {
                    "finding_id": "F01",
                    "dimension": "D6_methodological_rigor",
                    "severity": "major",
                    "target_file": "logic/experiments.md",
                    "target_entity": "E03",
                    "evidence_span": "No baseline reported",
                    "observation": "no non-LLM baseline",
                    "reasoning": "cannot tell if above chance",
                    "suggestion": "add retrieval baseline",
                }
            ],
        }

    report = score_rigor({"PAPER.md": "..."}, artifact_name="Transformer", rigor_scores=fake_rigor)
    assert report["overall"]["grade"] == "Accept"
    assert abs(report["overall"]["mean_score"] - 3.83) < 0.01
    assert set(report["dimensions"]) == set(DIMENSION_KEYS)
    assert report["findings"][0]["severity"] == "major"
    assert report["review_version"] == "3.0.0"


def test_score_rigor_grade_drives_hard_block_below_weak_accept() -> None:
    def low_rigor(ara_bundle):
        return {
            "dimensions": {
                k: {"score": 2, "strengths": [], "weaknesses": [], "suggestions": []}
                for k in DIMENSION_KEYS
            },
            "findings": [],
        }

    report = score_rigor({}, artifact_name="x", rigor_scores=low_rigor)
    assert report["overall"]["grade"] in {"Weak Reject", "Reject"}
    assert report["overall"]["passes_seal2"] is False
