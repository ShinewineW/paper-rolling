"""Three-layer citation anchor lint — HARD gate (吸收-D1)."""

from __future__ import annotations

from scripts.output.anchor_lint import AnchorViolation, lint_text


def test_well_formed_ref_anchor_passes() -> None:
    text = "模型在 nuScenes 上达到 0.61 NDS<!--ref:nds-table--><!--anchor:quote:NDS%200.61-->。"
    assert lint_text(text) == []


def test_ref_without_anchor_is_violation() -> None:
    text = "提升 3.2 个百分点<!--ref:gain-->。"
    v = lint_text(text)
    assert len(v) == 1
    assert "without trailing anchor" in v[0].message


def test_orphan_anchor_is_violation() -> None:
    text = "see<!--anchor:page:7-->."
    v = lint_text(text)
    assert any("orphan anchor" in x.message for x in v)


def test_quote_over_25_words_is_violation() -> None:
    long_quote = "%20".join(["word"] * 26)
    text = f"x<!--ref:s--><!--anchor:quote:{long_quote}-->."
    v = lint_text(text)
    assert any("exceeds 25 words" in x.message for x in v)


def test_quote_raw_double_hyphen_is_violation() -> None:
    text = "x<!--ref:s--><!--anchor:quote:a--b-->."
    v = lint_text(text)
    assert any("raw `--`" in x.message for x in v)


def test_empty_value_on_page_kind_is_violation() -> None:
    text = "x<!--ref:s--><!--anchor:page:-->."
    v = lint_text(text)
    assert any("empty anchor value" in x.message for x in v)


def test_none_kind_may_be_empty() -> None:
    text = "背景综述句无需精确锚点<!--ref:bg--><!--anchor:none:-->。"
    assert lint_text(text) == []


def test_unanchored_empirical_number_no_longer_hard_blocks() -> None:
    # ADR-0012: prose-anchor requirement dropped. An empirical performance number
    # with NO ref marker must NOT be flagged by lint_text — faithfulness is
    # branch1_gate's job, not the anchor lint's.
    text = "我们的方法在 KITTI 上提升了 5.4 个百分点。"
    assert lint_text(text) == []


def test_section_reference_number_is_not_an_assertion() -> None:
    # Guard: "见 Section 3" / years are NOT empirical assertions (no metric cue).
    text = "如 Section 3 与 2017 年的工作所述,本文沿用该设定。"
    assert lint_text(text) == []


def test_illustrative_number_without_metric_cue_is_not_an_assertion() -> None:
    # Guard: a toy-example / list number with no performance cue must NOT fire.
    text = "取 k=2 的截断步数,迭代两步即可收敛。"
    assert lint_text(text) == []


def test_lint_text_returns_typed_violations() -> None:
    v = lint_text("x<!--ref:s-->.")
    assert isinstance(v[0], AnchorViolation)
    assert v[0].line == 1


def test_markdown_table_row_is_not_an_assertion() -> None:
    # A markdown table ROW renders the paper's own gated figures (fidelity gated by
    # G2, not the anchor lint). Metric-name headers ("mAP↑", the `3` in `3D-Bbox`)
    # and data rows must NOT be flagged as unanchored performance assertions, so a
    # report can faithfully inline the evidence tables.
    text = "| Method | 3D-Bbox mAP↑ | Lane mIoU↑ |\n|---|---|---|\n| HDMap+LiDAR | 0.42 | 0.71 |\n"
    assert lint_text(text) == []


def test_prose_performance_claim_no_longer_blocks_outside_tables() -> None:
    # ADR-0012: prose-anchor requirement dropped — lint_text must NOT flag an
    # unanchored performance number in prose (faithfulness is branch1_gate's job).
    text = "融合模型在 mAP 上达到 0.42,显著高于基线。"
    assert lint_text(text) == []


def test_unanchored_prose_number_no_longer_fails_lint() -> None:
    # ADR-0012: prose may carry numbers; lint_text must NOT flag them.
    from scripts.output.anchor_lint import lint_text

    report = "本文模型在 KITTI 上提升了 9.9 个百分点。"  # prose %, no <!--ref-->
    assert lint_text(report) == []


def test_malformed_core_block_anchor_still_fails() -> None:
    # The KEPT checks still guard the engine 核心结论 block's anchors.
    from scripts.output.anchor_lint import lint_text

    assert lint_text("结论 <!--ref:boguskind:x--> 收尾。") != []
