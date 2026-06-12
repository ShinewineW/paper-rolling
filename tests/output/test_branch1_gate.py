from __future__ import annotations

from scripts.output.branch1_gate import unconfirmed_report_numbers


def test_grounded_prose_numbers_pass() -> None:
    md = "Our model reaches 28.4 NDS and uses 10% of the data."
    report = "本文模型达到 28.4 NDS,仅用 10% 数据训练。"
    assert unconfirmed_report_numbers(report, md) == []


def test_anchor_comment_payloads_are_not_parsed_as_numbers() -> None:
    # The 核心结论 block's <!--ref:quote:...%20...--> anchors must be stripped before
    # extraction, else %20-encoded payloads become bogus ungrounded numbers.
    md = "Table 1 reports 28.4 NDS."
    report = "结论:本文达到 28.4 NDS。<!--ref:quote:Table%201%20reports%2028.4-->"
    assert unconfirmed_report_numbers(report, md) == []


def test_list_index_and_locators_are_not_data_numbers() -> None:
    # numbered 核心结论 ("1. …") and figure/section locators (图2 / §3) are structure,
    # not data — must not be flagged just because their digit is absent from source.
    md = "Our model reaches 28.4 NDS."
    report = "1. 本文达到 28.4 NDS。\n见 图2 与 §3 的对比。"
    assert unconfirmed_report_numbers(report, md) == []


def test_invented_prose_number_is_flagged() -> None:
    md = "Our model reaches 28.4 NDS."
    report = "本文模型达到 99.9 NDS(凭空数字)。"
    assert unconfirmed_report_numbers(report, md) == ["99.9"]


def test_table_rows_and_code_fences_are_skipped() -> None:
    md = "Only 28.4 appears in source."
    report = "\n".join(
        [
            "| Model | Score |",
            "| Ours | 77.7 |",  # table cell — skipped (paper's own figure, G2-gated)
            "```",
            "x = 88.8",  # code fence — skipped
            "```",
            "正文里 28.4 是真的。",  # grounded prose number → ok
        ]
    )
    assert unconfirmed_report_numbers(report, md) == []
