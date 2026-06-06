"""branch1 report derives from branch2, anchored to MD, passes the hard gate."""

from __future__ import annotations

import pytest
from scripts.output.anchor_lint import lint_text
from scripts.output.branch1_report import AnchorGateError, write_branch1
from scripts.output.branch2_ara import write_branch2


def test_report_passes_anchor_lint(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, analysis)
    report = (person / "report.md").read_text(encoding="utf-8")
    assert lint_text(report) == []


def test_report_uses_unified_classdef_palette(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, analysis)
    report = (person / "report.md").read_text(encoding="utf-8")
    # The cherry-picked palette stroke colors (Mermaid style guide).
    assert "classDef" in report
    assert "stroke:#2563eb" in report
    # No inline style / no init directive (hard rule, 双输出-D1).
    assert "%%{init" not in report
    assert "\nstyle " not in report


def test_math_section_has_human_review_banner(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, analysis)
    report = (person / "report.md").read_text(encoding="utf-8")
    assert "AI 推导,需人工复核" in report
    assert "直觉辅助,非严格对应" in report  # labeled analogy
    assert "玩具例子" in report


def test_loss_section_has_four_parts(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, analysis)
    report = (person / "report.md").read_text(encoding="utf-8")
    for part in ("修复方向", "机制", "对比基线", "证据"):
        assert part in report


def test_evidence_pointer_targets_ai_package(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, analysis)
    report = (person / "report.md").read_text(encoding="utf-8")
    # Cross-vault pointer back to ai_package evidence (双输出-D5).
    assert "../ai_package/" in report or "../../ai_package/" in report


def test_unanchored_claim_raises_gate_error(tmp_path, candidate, analysis, md_path):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    # Force the producer to emit a performance number with no MD anchor -> the
    # producer must raise rather than silently ship an unanchored claim.
    with pytest.raises(AnchorGateError):
        write_branch1(person, candidate, ara, md_path, analysis, _force_unanchored=True)
