from __future__ import annotations

from scripts.output.branch1_gate import check_report_faithfulness, unconfirmed_report_numbers


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


def test_arxiv_id_and_doi_in_prose_are_not_data_numbers() -> None:
    # ADR-0012 demo (ORION): the writer echoed the paper's own arXiv id into prose;
    # an id is paper-identity metadata, never a metric, so it must NOT be grounded.
    md = "Our model reaches 28.4 NDS."  # id absent from the source MD
    report = "本文(arXiv:2503.19755,DOI 10.1109/ABC.2025.123456)达到 28.4 NDS。"
    assert unconfirmed_report_numbers(report, md) == []


def test_real_metric_decimal_is_not_mistaken_for_an_arxiv_id() -> None:
    # The identifier shape is 4-int.4–5-decimal; a normal metric (28.4 / 0.61) is
    # unaffected, and a genuinely ungrounded metric still flags.
    md = "Our model reaches 28.4 NDS."
    assert unconfirmed_report_numbers("达到 28.4 NDS,基线 0.61。", md) == ["0.61"]


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


def _ok_judge(report_text, ara_dir):
    return {"faithful": True, "findings": []}


def _drift_judge(report_text, ara_dir):
    return {"faithful": False, "findings": [{"claim": "88.1 是我们的", "issue": "实为 baseline"}]}


def test_gate_passes_faithful_report(tmp_path) -> None:
    md = "Our model reaches 28.4 NDS using 10% data."
    report = "本文达到 28.4 NDS,仅用 10% 数据。"
    hard = check_report_faithfulness(
        report, md, tmp_path, judge=_ok_judge, max_unconfirmed=5, max_unconfirmed_ratio=0.2
    )
    assert hard == []


def test_gate_blocks_systematic_invented_numbers(tmp_path) -> None:
    # 6 ungrounded of 6 → over BOTH the absolute floor (6>5) and the ratio
    # (6 > max(5, 0.2*6=1.2)=5) even in tolerant mode → block.
    md = "Only 28.4 appears."
    report = "凭空: 11.1, 22.2, 33.3, 44.4, 55.5, 66.6 全是编的。"  # 6 ungrounded
    hard = check_report_faithfulness(
        report,
        md,
        tmp_path,
        judge=_ok_judge,
        tolerant=True,
        max_unconfirmed=5,
        max_unconfirmed_ratio=0.2,
    )
    assert hard and all(f.is_hard_block for f in hard)


def test_gate_tolerates_a_single_miss_when_tolerant(tmp_path) -> None:
    # 1 bad of 6 total: within BOTH limits (1<=5 absolute AND 1<=0.2*6=1.2 ratio).
    md = "Real numbers 28.4, 24.6, 1.1, 2.2, 3.3 here."
    report = "28.4、24.6、1.1、2.2、3.3 都对,只有 99.9 手滑。"
    hard = check_report_faithfulness(
        report,
        md,
        tmp_path,
        judge=_ok_judge,
        tolerant=True,
        max_unconfirmed=5,
        max_unconfirmed_ratio=0.2,
    )
    assert hard == []


def test_gate_ratio_loosens_large_reports_but_floor_protects_small(tmp_path) -> None:
    # The ratio limit binds (TIGHTENS/loosens) only for large reports: the absolute
    # `max_unconfirmed` is a FLOOR, and `max(floor, ratio*total)` lets a LARGE report
    # tolerate proportionally MORE misses. 6 ungrounded of 30 (6 <= max(5, 0.2*30=6))
    # is tolerated; the SAME 6 ungrounded standing alone (6 of 6, 6 > max(5, 1.2)=5)
    # blocks — small reports are not over-quarantined, large ones scale by fraction.
    grounded = [f"{i}.5" for i in range(10, 34)]  # 24 grounded values (10.5 … 33.5)
    bad6 = ["88.8", "99.9", "11.1", "22.2", "33.3", "44.4"]  # 6 ungrounded
    md = "Source: " + " ".join(grounded)
    big = "正文:" + "、".join(grounded + bad6) + "。"  # 30 total, 6 bad → tolerated
    small = "正文:" + "、".join(bad6) + "。"  # 6 total, 6 bad → blocked
    ok = check_report_faithfulness(
        big,
        md,
        tmp_path,
        judge=_ok_judge,
        tolerant=True,
        max_unconfirmed=5,
        max_unconfirmed_ratio=0.2,
    )
    blocked = check_report_faithfulness(
        small,
        md,
        tmp_path,
        judge=_ok_judge,
        tolerant=True,
        max_unconfirmed=5,
        max_unconfirmed_ratio=0.2,
    )
    assert ok == []
    assert blocked and all(f.is_hard_block for f in blocked)


def test_gate_strict_blocks_a_single_miss(tmp_path) -> None:
    md = "Real numbers 28.4 and 24.6 here."
    report = "28.4 与 24.6 是真的,只有 99.9 手滑。"
    hard = check_report_faithfulness(
        report, md, tmp_path, judge=_ok_judge
    )  # tolerant=False default
    assert hard and all(f.is_hard_block for f in hard)


def test_gate_blocks_on_judge_drift(tmp_path) -> None:
    md = "Our model reaches 28.4 NDS."
    report = "本文达到 28.4 NDS。"
    hard = check_report_faithfulness(
        report, md, tmp_path, judge=_drift_judge, max_unconfirmed=5, max_unconfirmed_ratio=0.2
    )
    assert hard and any("baseline" in f.observation for f in hard)
