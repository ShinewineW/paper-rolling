from __future__ import annotations

from scripts.output.branch1_gate import (
    check_report_faithfulness,
    prose_numbers,
    ungrounded_report_numbers,
)


def test_prose_numbers_extracts_data_numbers() -> None:
    # prose_numbers 抽取正文里的数据数字(语义上"是否落源"交给 ungrounded_report_numbers)。
    assert prose_numbers("本文模型达到 28.4 NDS,仅用 10% 数据训练。") == ["28.4", "10"]


def test_anchor_comment_payloads_are_not_parsed_as_numbers() -> None:
    # The 核心结论 block's <!--ref:quote:...%20...--> anchors must be stripped before
    # extraction, else %20-encoded payloads become bogus tokens (201/20/2028.4).
    report = "结论:本文达到 28.4 NDS。<!--ref:quote:Table%201%20reports%2028.4-->"
    assert prose_numbers(report) == ["28.4"]


def test_list_index_and_locators_are_not_data_numbers() -> None:
    # numbered 核心结论 ("1. …") and figure/section locators (图2 / §3) are structure,
    # not data — must be stripped before extraction.
    report = "1. 本文达到 28.4 NDS。\n见 图2 与 §3 的对比。"
    assert prose_numbers(report) == ["28.4"]


def test_invented_prose_number_is_extracted() -> None:
    # prose_numbers 只负责抽取;"99.9 凭空"的拦/标语义在 ungrounded/评价 层。
    assert prose_numbers("本文模型达到 99.9 NDS(凭空数字)。") == ["99.9"]


def test_arxiv_id_and_doi_in_prose_are_not_data_numbers() -> None:
    # ADR-0012 demo (ORION): the writer echoed the paper's own arXiv id into prose;
    # an id is paper-identity metadata, never a metric → stripped, not extracted.
    report = "本文(arXiv:2503.19755,DOI 10.1109/ABC.2025.123456)达到 28.4 NDS。"
    assert prose_numbers(report) == ["28.4"]


def test_inline_code_vault_path_is_not_a_data_number() -> None:
    # ADR-0012 demo (ORION): the report's intro backticks a vault-key path
    # `ai_package/2026-06-12_..._2503.19755/ara/`; inline code is infra, not data.
    report = "事实源见 `ai_package/2026-06-12_ORION_2503.19755/ara/`,本文达到 28.4 NDS。"
    assert prose_numbers(report) == ["28.4"]


def test_real_metric_decimal_is_not_mistaken_for_an_arxiv_id() -> None:
    # The identifier shape is 4-int.4–5-decimal; normal metrics (28.4 / 0.61) are
    # unaffected and ARE extracted.
    assert prose_numbers("达到 28.4 NDS,基线 0.61。") == ["28.4", "0.61"]


def test_table_rows_and_code_fences_are_skipped() -> None:
    report = "\n".join(
        [
            "| Model | Score |",
            "| Ours | 77.7 |",  # table cell — skipped (paper's own figure, G2-gated)
            "```",
            "x = 88.8",  # code fence — skipped
            "```",
            "正文里 28.4 是真的。",  # prose number → extracted
        ]
    )
    assert prose_numbers(report) == ["28.4"]


def test_ungrounded_vs_ara_uses_ara_not_md(tmp_path) -> None:
    # 真值参照 = ARA(不是源 MD)。报告里 28.4 在 ARA、99.9 不在 → 只 99.9 算未落源。
    # 最小 ARA,覆盖 load_ara_bundle 读取的 PAPER.md + logic/claims.md。
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text("**Statement**: reaches 28.4 NDS", encoding="utf-8")
    (ara / "PAPER.md").write_text("headline_value: 28.4", encoding="utf-8")
    report = "本文达到 28.4 NDS,另有 99.9 凭空数字。"
    assert ungrounded_report_numbers(report, ara) == ["99.9"]


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
