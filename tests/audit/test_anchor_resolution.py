from __future__ import annotations

from pathlib import Path

from scripts.audit.anchor_resolution import (
    check_branch1_md_anchors,
    iter_ref_anchor_markers,
    resolves_in_md,
)

_MD = (
    "# Attention Is All You Need\n\n"
    "The model achieves a BLEU score of 28.4 on WMT14 En-De.\n\n"
    "It trains in 12 hours on 8 GPUs.\n"
)


def test_iter_ref_anchor_markers_finds_pairs() -> None:
    report = (
        "本模型取得 28.4 的 BLEU 分数"
        "<!--ref:bleu--><!--anchor:quote:BLEU%20score%20of%2028.4-->。\n"
    )
    markers = list(iter_ref_anchor_markers(report))
    assert len(markers) == 1
    assert markers[0].kind == "quote"
    assert markers[0].value == "BLEU score of 28.4"


def test_resolves_in_md_true_when_quote_substring_present() -> None:
    assert resolves_in_md("quote", "BLEU score of 28.4", _MD) is True


def test_resolves_in_md_false_when_quote_absent() -> None:
    assert resolves_in_md("quote", "BLEU score of 99.9", _MD) is False


def test_check_passes_when_every_anchor_resolves(tmp_path: Path) -> None:
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text(
        "取得 28.4 BLEU<!--ref:bleu--><!--anchor:quote:BLEU%20score%20of%2028.4-->。\n"
        "训练耗时<!--ref:train--><!--anchor:quote:trains%20in%2012%20hours-->。\n",
        encoding="utf-8",
    )
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is False


def test_check_hard_blocks_unresolvable_anchor(tmp_path: Path) -> None:
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text(
        "取得 99.9 BLEU<!--ref:bogus--><!--anchor:quote:BLEU%20score%20of%2099.9-->。\n",
        encoding="utf-8",
    )
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is True
    hard = verdict.hard_findings[0]
    assert "99.9" in hard.observation
    assert hard.is_hard_block is True


def test_check_does_not_block_empirical_sentence_with_no_anchor(tmp_path: Path) -> None:
    """ADR-0012: prose-anchor requirement dropped. An empirical sentence with NO
    ref/anchor marker must NOT be blocked by check_branch1_md_anchors — only
    present anchors that fail to resolve are blocked."""
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text("本模型取得了 28.4 的 BLEU 分数，但没有任何锚点。\n", encoding="utf-8")
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is False


def test_check_ignores_non_empirical_prose(tmp_path: Path) -> None:
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text("本文提出了一种全新的注意力机制，思路非常优雅。\n", encoding="utf-8")
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is False


def test_anchor_check_ignores_numbers_in_prose_no_anchors(tmp_path):
    """ADR-0012: prose-anchor requirement dropped. A number-bearing sentence
    with no ref/anchor markers must not be blocked by check_branch1_md_anchors,
    regardless of whether numbers look empirical."""
    from scripts.audit.anchor_resolution import check_branch1_md_anchors

    report = tmp_path / "report.md"
    # A number-bearing sentence with no anchor markers at all.
    report.write_text("The system processed 42 documents overnight.\n", encoding="utf-8")
    md = tmp_path / "src.md"
    md.write_text("Unrelated source text.\n", encoding="utf-8")

    # No anchors present -> nothing to resolve -> gate passes.
    assert check_branch1_md_anchors(report, md).blocked is False


def test_g3_skips_table_rows_regression(tmp_path: Path) -> None:
    """Regression: a markdown evidence-table row with a metric cue (F1, 0.889)
    must NOT be flagged as an unanchored empirical sentence — branch1's lint skips
    table rows (gated by G2), and G3 must agree. This blocked every dense paper."""
    md = tmp_path / "src.md"
    md.write_text("On BBC the F1 score is 0.889 in the paper.", encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text(
        "## 实验\n\n| 数据集 | 指标 | 值 |\n|---|---|---|\n| BBC | F1 ↑ | 0.889 |\n",
        encoding="utf-8",
    )
    verdict = check_branch1_md_anchors(report, md)
    assert not verdict.findings  # table row not flagged (was the G3 false-positive)


def test_unanchored_empirical_lines_still_detects_but_lint_text_does_not_block() -> None:
    """ADR-0012: unanchored_empirical_lines still detects performance lines (it
    remains defined as a future classifier hook / C4 roadmap entry), but lint_text
    no longer uses it — prose numbers are not blocked by the anchor lint gate."""
    from scripts.output.anchor_lint import lint_text, unanchored_empirical_lines

    text = "本节小结。\n模型在 mAP 上达到 0.99，大幅超过基线。\n"  # 2nd line empirical, no ref
    # The detector still correctly identifies the empirical line.
    detected = {ln for ln, _ in unanchored_empirical_lines(text)}
    assert detected == {2}
    # But lint_text (check 4 removed per ADR-0012) does NOT flag it.
    empirical_violations = [v for v in lint_text(text) if "unanchored empirical" in v.message]
    assert empirical_violations == []
