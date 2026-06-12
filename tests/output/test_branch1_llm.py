from __future__ import annotations

from pathlib import Path

import pytest
from scripts.output.branch1_llm import (
    _quote_mermaid_labels,
    _strip_emoji,
    write_branch1_llm,
)
from scripts.output.branch1_report import AnchorGateError


def _ara(tmp_path: Path) -> Path:
    ara = tmp_path / "ai_package" / "k" / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "evidence" / "tables").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text(
        "## C1: x\n- **Statement**: 模型在 BLEU 上达到 28.4。\n", encoding="utf-8"
    )
    (ara / "evidence" / "tables" / "main.md").write_text(
        "# 主表\n- **Source**: Table 1\n\n| Model | BLEU |\n|---|---|\n| Ours | 28.4 |\n",
        encoding="utf-8",
    )
    return ara


def test_write_branch1_llm_assembles_grounded_report(tmp_path: Path) -> None:
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Our model reaches a BLEU of 28.4 on the benchmark.\n", encoding="utf-8")
    person = tmp_path / "person_vault" / "k"

    def fake_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {
            "sections": {
                "01_导读": "## 一句话总结\n本文提出一种可控世界生成方法,效果出色。",
                "06_实验": "## 实验与对比\n多模态融合在整体质量上领先(详见下方实验表)。",
            },
            "figures": [],
        }

    write_branch1_llm(person, {"title": "DemoPaper"}, ara, md, fake_write_report, key="k")

    report = (person / "report.md").read_text(encoding="utf-8")
    assert (person / "report.html").exists()
    assert "# DemoPaper — 深度解读" in report
    assert "## 核心结论" in report  # verified claims block (no anchors, ADR-0012 rev)
    assert "28.4" in report
    assert "一句话总结" in report and "实验与对比" in report
    assert "| Ours | 28.4 |" in report  # gated evidence table inlined after 06
    assert "<!--anchor:" not in report  # ADR-0012 rev: anchor machinery retired
    assert "## 评价" in report  # opening faithfulness note prepended


def test_write_branch1_llm_embeds_selected_figures(tmp_path: Path) -> None:
    """Selective tour: mandatory architecture figure + a chosen result; skip the rest."""
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Method overview; BLEU of 28.4. See figures.\n", encoding="utf-8")
    (md.parent / "images").mkdir()
    for name in ("aaa.jpg", "bbb.jpg", "ccc.jpg"):
        (md.parent / "images" / name).write_bytes(b"\xff\xd8\xff\xe0fake-jpeg")
    person = tmp_path / "person_vault" / "k"

    def fake_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {
            "sections": {
                "01_导读": "## 导读\n本文方法概述。",
                "04_方法与架构": "## 方法与架构\n核心流程如下。",
                "06_实验与对比": "## 实验与对比\n定性领先(详见下方实验表)。",
            },
            "figures": [
                {  # mandatory core structure diagram
                    "ref": "images/aaa.jpg",
                    "caption": "Figure 1: architecture overview",
                    "role": "architecture",
                    "include": True,
                    "zh": "图1说明了整体架构。",
                },
                {  # one selected representative result
                    "ref": "images/bbb.jpg",
                    "caption": "Figure 4: qualitative results",
                    "role": "result",
                    "include": True,
                    "zh": "图4展示了代表性结果。",
                },
                {  # a minor result figure NOT selected
                    "ref": "images/ccc.jpg",
                    "caption": "Figure 9: extra ablation",
                    "role": "result",
                    "include": False,
                    "zh": "",
                },
            ],
        }

    write_branch1_llm(person, {"title": "P"}, ara, md, fake_write_report, key="k")

    report = (person / "report.md").read_text(encoding="utf-8")
    assert "![](images/aaa.jpg)" in report  # mandatory architecture figure
    assert "![](images/bbb.jpg)" in report  # selected result figure
    assert "images/ccc.jpg" not in report  # NOT selected -> not embedded
    assert "图1说明了整体架构。" in report  # zh caption under the figure
    # section-aware placement: architecture by the intro, results after experiments
    assert "论文总体架构" in report and "效果示例" in report
    assert report.index("论文总体架构") < report.index("效果示例")  # intro before results
    assert (person / "images" / "aaa.jpg").exists() and (person / "images" / "bbb.jpg").exists()
    assert not (person / "images" / "ccc.jpg").exists()  # not copied

    # HTML is self-contained: original figures inlined as base64 (no broken links)
    html = (person / "report.html").read_text(encoding="utf-8")
    assert "data:image/jpeg;base64," in html
    assert "background:#ffffff" in html  # light theme
    assert "mathjax" in html.lower()  # math engine loaded so $$..$$ renders


def test_strip_emoji_removes_emoji_keeps_text_and_arrows() -> None:
    assert _strip_emoji("## 🧠 算法目标与推导") == "## 算法目标与推导"
    assert _strip_emoji("结果 ✅ 很好") == "结果 很好"
    assert _strip_emoji("A → B 的流程") == "A → B 的流程"  # plain arrow (U+2192) kept
    assert _strip_emoji("普通中文文本无表情") == "普通中文文本无表情"


def test_quote_mermaid_labels_only_inside_blocks() -> None:
    md = (
        "前文 [一个链接](http://x)\n\n"
        "```mermaid\nflowchart TB\n  a[叠加激活 和>1归一化] --> b[正常]\n```\n"
        "后文 [另一个链接](http://y)\n"
    )
    out = _quote_mermaid_labels(md)
    assert 'a["叠加激活 和>1归一化"]' in out  # special-char label quoted
    assert 'b["正常"]' in out
    assert "[一个链接](http://x)" in out  # prose markdown links untouched
    assert "[另一个链接](http://y)" in out


def test_write_branch1_llm_requires_architecture_figure(tmp_path: Path) -> None:
    """If the paper has an architecture figure, it MUST be embedded (mandatory)."""
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Method overview; BLEU of 28.4.\n", encoding="utf-8")
    (md.parent / "images").mkdir()
    (md.parent / "images" / "arch.jpg").write_bytes(b"\xff\xd8\xff\xe0fake-jpeg")
    person = tmp_path / "person_vault" / "k"

    def fake_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        # An architecture-caption figure exists but the curator failed to include it.
        return {
            "sections": {"04_方法": "## 方法与架构\n概述。"},
            "figures": [
                {
                    "ref": "images/arch.jpg",
                    "caption": "Figure 1: model architecture",
                    "role": "architecture",
                    "include": False,
                    "zh": "",
                }
            ],
        }

    with pytest.raises(AnchorGateError, match="core method/model-structure figure"):
        write_branch1_llm(person, {"title": "P"}, ara, md, fake_write_report, key="k")


def test_write_branch1_llm_prose_perf_number_no_longer_blocked(tmp_path: Path) -> None:
    # ADR-0012: prose-anchor requirement dropped. An LLM section with a prose
    # performance number not present in the source MD must NOT raise AnchorGateError
    # — lint_text check 4 was removed; faithfulness is branch1_gate's job.
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Our model reaches a BLEU of 28.4.\n", encoding="utf-8")  # 0.99 NOT here
    person = tmp_path / "person_vault" / "k"

    def prose_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {
            "sections": {"06_实验": "## 实验\n我们在 mAP 上达到 0.99,大幅超过基线。"},
            "figures": [],
        }

    # Should succeed without raising.
    write_branch1_llm(person, {"title": "X"}, ara, md, prose_write_report, key="k")
    assert (person / "report.md").exists()
