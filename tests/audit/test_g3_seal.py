from __future__ import annotations

import json
from pathlib import Path

from scripts.audit.g3_seal import run_g3
from scripts.audit.rigor_rubric import DIMENSION_KEYS


def _build_paper(tmp_path: Path, *, good: bool = True):
    md = tmp_path / "src.md"
    md.write_text(
        "# T\n\nThe model achieves a BLEU score of 28.4 on WMT14.\n",
        encoding="utf-8",
    )
    content_list = tmp_path / "content_list.json"
    content_list.write_text(json.dumps([{"type": "text", "text": "T"}]), encoding="utf-8")

    person = tmp_path / "person_vault" / "2026-06-05_T_170603762"
    person.mkdir(parents=True)
    quote = "BLEU%20score%20of%2028.4" if good else "BLEU%20score%20of%2099.9"
    (person / "report.md").write_text(
        f"取得 28.4 BLEU<!--ref:bleu--><!--anchor:quote:{quote}-->。\n",
        encoding="utf-8",
    )

    ai = tmp_path / "ai_package" / "2026-06-05_T_170603762"
    ara = ai / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text(
        "## C01: Improves over baseline\n\n"
        "**Statement**: Our model improves BLEU to 28.4 over the baseline.\n"
        "**Proof**: E01\n",
        encoding="utf-8",
    )
    (ara / "logic" / "experiments.md").write_text(
        "## E01: Baseline comparison\n\nWe compare against the RNN baseline.\n",
        encoding="utf-8",
    )
    return md, content_list, person, ai


def _good_rigor(ara_bundle):
    return {
        "dimensions": {
            k: {"score": 4, "strengths": [], "weaknesses": [], "suggestions": []}
            for k in DIMENSION_KEYS
        },
        "findings": [],
    }


def _entailed(claim, exp_text):
    return (True, "baseline present")


def test_run_g3_passes_and_writes_level2_report(tmp_path: Path) -> None:
    md, cl, person, ai = _build_paper(tmp_path, good=True)
    verdict = run_g3(person, ai, md, cl, rigor_scores=_good_rigor, entailment_judge=_entailed)
    assert verdict.blocked is False
    report_path = ai / "ara" / "level2_report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["overall"]["grade"] == "Accept"


def test_run_g3_blocks_on_unresolvable_branch1_anchor(tmp_path: Path) -> None:
    md, cl, person, ai = _build_paper(tmp_path, good=False)
    verdict = run_g3(person, ai, md, cl, rigor_scores=_good_rigor, entailment_judge=_entailed)
    assert verdict.blocked is True
    assert any("does not resolve" in f.observation for f in verdict.hard_findings)


def test_run_g3_blocks_on_low_rigor_grade(tmp_path: Path) -> None:
    md, cl, person, ai = _build_paper(tmp_path, good=True)

    def low_rigor(ara_bundle):
        return {
            "dimensions": {
                k: {"score": 1, "strengths": [], "weaknesses": [], "suggestions": []}
                for k in DIMENSION_KEYS
            },
            "findings": [],
        }

    verdict = run_g3(person, ai, md, cl, rigor_scores=low_rigor, entailment_judge=_entailed)
    assert verdict.blocked is True
    # report is still written (the grade is the evidence for the block).
    assert (ai / "ara" / "level2_report.json").exists()
    assert any("Seal Level 2" in f.observation for f in verdict.hard_findings)


def test_run_g3_blocks_on_entailment_failure(tmp_path: Path) -> None:
    md, cl, person, ai = _build_paper(tmp_path, good=True)

    def not_entailed(claim, exp_text):
        return (False, "no baseline numbers shown")

    verdict = run_g3(person, ai, md, cl, rigor_scores=_good_rigor, entailment_judge=not_entailed)
    assert verdict.blocked is True
    assert any("baseline" in f.observation for f in verdict.hard_findings)


def test_run_g3_hard_blocks_when_branch1_report_missing(tmp_path: Path) -> None:
    # A person_vault entry with NO report.md must HARD-block (cannot seal an empty
    # human branch); previously the anchor check was skipped silently and passed.
    md, cl, person, ai = _build_paper(tmp_path, good=True)
    (person / "report.md").unlink()  # remove branch1 report

    verdict = run_g3(person, ai, md, cl, rigor_scores=_good_rigor, entailment_judge=_entailed)
    assert verdict.blocked is True
    assert any(
        f.finding_id == "G3R0" and "missing branch1 report.md" in f.observation
        for f in verdict.hard_findings
    )
