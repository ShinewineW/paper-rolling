from __future__ import annotations

from pathlib import Path

import pytest
from scripts.output.branch1_llm import write_branch1_llm
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
    assert "## 核心结论" in report  # mechanically-anchored claims block
    assert "28.4" in report
    assert "一句话总结" in report and "实验与对比" in report
    assert "| Ours | 28.4 |" in report  # gated evidence table inlined after 06
    assert "<!--anchor:" in report


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
            "sections": {"04_方法": "## 方法与架构\n本文方法概述。"},
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
    assert "## 论文图解导览(原图)" in report
    assert "![](images/aaa.jpg)" in report  # mandatory architecture figure
    assert "![](images/bbb.jpg)" in report  # selected result figure
    assert "images/ccc.jpg" not in report  # NOT selected -> not embedded
    assert "图1说明了整体架构。" in report
    assert (person / "images" / "aaa.jpg").exists() and (person / "images" / "bbb.jpg").exists()
    assert not (person / "images" / "ccc.jpg").exists()  # not copied


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


def test_write_branch1_llm_blocks_unanchored_perf_claim(tmp_path: Path) -> None:
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Our model reaches a BLEU of 28.4.\n", encoding="utf-8")  # 0.99 NOT here
    person = tmp_path / "person_vault" / "k"

    def bad_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {
            "sections": {"06_实验": "## 实验\n我们在 mAP 上达到 0.99,大幅超过基线。"},
            "figures": [],
        }

    with pytest.raises(AnchorGateError):
        write_branch1_llm(person, {"title": "X"}, ara, md, bad_write_report, key="k")
