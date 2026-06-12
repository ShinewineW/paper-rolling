"""branch1 report derives from branch2, anchored to MD, passes the hard gate."""

from __future__ import annotations

from scripts.output.anchor_lint import lint_text
from scripts.output.branch1_report import write_branch1
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


def test_unanchored_prose_number_no_longer_raises_gate_error(
    tmp_path, candidate, analysis, md_path
):
    # ADR-0012: prose-anchor requirement dropped. write_branch1 with
    # _force_unanchored=True (injects an unanchored prose performance sentence)
    # must NO LONGER raise AnchorGateError — lint_text check 4 was removed.
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"
    # Should succeed without raising.
    write_branch1(person, candidate, ara, md_path, analysis, _force_unanchored=True)
    assert (person / "report.md").exists()


def test_branch1_prose_is_domain_agnostic_no_hardcoded_diffusion(
    tmp_path, candidate, analysis, md_path
):
    """Foundation review: the producer holds STRUCTURE only — math intuition,
    loss highlight, trend, and the branch2 domain stamp come from the per-paper
    analyzer, so an off-domain (non-diffusion) paper never inherits a hardcoded
    diffusion/AD narrative. Pins that the previously-hardcoded strings are gone.
    """
    nlp = {
        **analysis,
        "domain": "natural language processing",
        "math_intuition": "像逐词修订一段译文,每次替换都更贴合原意(直觉辅助,非严格对应)。",
        "math_toy_example": "取一句短文本,按上式逐步重排,目标困惑度随步数下降(示意,非性能结论)。",
        "loss_highlight": {
            "direction": "该损失针对检索片段与生成答案不一致这一弱点设计。",
            "mechanism": "用对齐目标约束生成,使答案落在检索证据内(链 数学方法 推导)。",
            "baseline": "相比无约束生成,该设计更契合忠实性目标。",
        },
        "trend": "该工作把检索增强生成推向更长上下文的方向。",
    }
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, nlp)
    person = tmp_path / "person"
    write_branch1(person, candidate, ara, md_path, nlp)
    report = (person / "report.md").read_text(encoding="utf-8")

    # Analyzer-supplied (NLP) narrative flows through to the report...
    assert "检索增强生成推向更长上下文" in report
    assert "检索片段与生成答案不一致" in report
    assert "逐词修订一段译文" in report
    # ...and the previously-HARDCODED diffusion/AD strings are gone from the code.
    assert "冲洗一张欠曝照片" not in report
    assert "将扩散式规划推向实时区间" not in report
    assert "标准回归损失会把多个合理未来平均成一个模糊解" not in report
    # branch2's domain stamp is analyzer-sourced too (no fixed "deep learning").
    paper_md = (ara / "PAPER.md").read_text(encoding="utf-8")
    assert "domain: natural language processing" in paper_md
    assert "domain: deep learning" not in paper_md
    # The report still passes its own three-layer anchor gate.
    assert lint_text(report) == []
