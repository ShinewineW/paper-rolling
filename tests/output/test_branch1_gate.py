from __future__ import annotations

from scripts.output.branch1_gate import (
    build_assessment,
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


def _mk_ara(tmp_path, *values: str):
    """A minimal ARA whose claims.md carries `values`, so ara_value_set grounds them."""
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text(
        "**Statement**: " + " ".join(f"reaches {v}" for v in values), encoding="utf-8"
    )
    (ara / "PAPER.md").write_text("\n".join(f"value: {v}" for v in values), encoding="utf-8")
    return ara


def _note_judge(report_text, ara_dir, *, ungrounded=None):
    # ADR-0012 rev: the (c) seam writes a Chinese prose 评价 note (str), never a verdict.
    return "整体与知识包一致,叙述忠实。"


def test_assessment_is_never_a_gate_and_starts_with_heading(tmp_path) -> None:
    # ADR-0012 rev: build_assessment NEVER raises and ALWAYS returns a `## 评价` block.
    ara = _mk_ara(tmp_path, "28.4")
    report = "本文达到 28.4 NDS,仅用 10% 数据。"
    note = build_assessment(report, ara, judge=_note_judge)
    assert note.startswith("## 评价")
    assert "叙述忠实" in note  # the judge's prose note is embedded


def test_assessment_surfaces_ungrounded_numbers_as_facts(tmp_path) -> None:
    # A report number absent from the ARA is SURFACED as a reader caveat — not blocked.
    ara = _mk_ara(tmp_path, "28.4")
    report = "本文达到 28.4 NDS,另有 99.9 凭空数字。"
    note = build_assessment(report, ara, judge=_note_judge)
    assert "99.9" in note and "未在已验证知识包" in note


def test_assessment_clears_when_all_numbers_grounded(tmp_path) -> None:
    ara = _mk_ara(tmp_path, "28.4", "24.6")
    report = "本文达到 28.4 NDS,基线 24.6。"
    note = build_assessment(report, ara, judge=_note_judge)
    assert "均可在已验证知识包" in note


def test_assessment_facts_only_when_no_judge(tmp_path) -> None:
    # judge=None (deterministic fallback path) → facts-only 评价, still a valid block.
    ara = _mk_ara(tmp_path, "28.4")
    report = "本文达到 28.4 NDS,另有 99.9 凭空数字。"
    note = build_assessment(report, ara, judge=None)
    assert note.startswith("## 评价") and "99.9" in note


def test_assessment_fails_soft_when_judge_raises(tmp_path) -> None:
    # A judge seam error NEVER propagates — the 评价 drops the note but still publishes facts.
    ara = _mk_ara(tmp_path, "28.4")

    def _boom(report_text, ara_dir, *, ungrounded=None):
        raise RuntimeError("seam down")

    report = "本文达到 28.4 NDS,另有 99.9 凭空数字。"
    note = build_assessment(report, ara, judge=_boom)
    assert note.startswith("## 评价") and "99.9" in note


def test_assessment_never_raises_on_unreadable_ara(tmp_path, monkeypatch) -> None:
    # ADR-0012 rev: build_assessment NEVER raises — even a corrupt/unreadable ARA
    # (the (b) reader throwing) must degrade to a valid 评价, not fail the report.
    import scripts.output.branch1_gate as bg

    def _boom(*_a, **_k):
        raise RuntimeError("corrupt ARA")

    monkeypatch.setattr(bg, "ungrounded_report_numbers", _boom)
    note = build_assessment("本文达到 28.4 NDS。", tmp_path / "ara", judge=None)
    assert note.startswith("## 评价")


def test_assessment_includes_ara_audit_flags_when_present(tmp_path) -> None:
    ara = _mk_ara(tmp_path, "28.4")
    (ara / "AUDIT_FLAGS.md").write_text("- **[major] G2X** — unconfirmed 77.7", encoding="utf-8")
    note = build_assessment("本文达到 28.4 NDS。", ara, judge=_note_judge)
    # The actual flag BODY must be carried inline, not just a pointer to the file.
    assert "G2X" in note and "77.7" in note
