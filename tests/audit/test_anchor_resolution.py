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


def test_check_hard_blocks_empirical_sentence_with_no_anchor(tmp_path: Path) -> None:
    """吸收-D1 lint = hard gate: an empirical sentence (carries a number) with
    NO ref/anchor marker is a block — forces full anchoring."""
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text("本模型取得了 28.4 的 BLEU 分数，但没有任何锚点。\n", encoding="utf-8")
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is True
    assert any("no anchor" in f.observation.lower() for f in verdict.hard_findings)


def test_check_ignores_non_empirical_prose(tmp_path: Path) -> None:
    md = tmp_path / "src.md"
    md.write_text(_MD, encoding="utf-8")
    report = tmp_path / "report.md"
    report.write_text("本文提出了一种全新的注意力机制，思路非常优雅。\n", encoding="utf-8")
    verdict = check_branch1_md_anchors(report, md)
    assert verdict.blocked is False
