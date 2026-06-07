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

    def fake_write_report(ara_dir: Path) -> dict[str, str]:
        # Vivid prose, numbers kept OUT of sentences (per the writer discipline).
        return {
            "01_导读": "## 一句话总结\n本文提出一种可控世界生成方法,效果出色。",
            "06_实验": "## 实验与对比\n多模态融合在整体质量上领先(详见下方实验表)。",
        }

    write_branch1_llm(person, {"title": "DemoPaper"}, ara, md, fake_write_report, key="k")

    report = (person / "report.md").read_text(encoding="utf-8")
    assert (person / "report.html").exists()
    assert "# DemoPaper — 深度解读" in report
    assert "## 核心结论" in report  # mechanically-anchored claims block
    assert "28.4" in report  # claim number survived + (anchored)
    assert "一句话总结" in report and "实验与对比" in report  # writer sections stitched
    assert "| Ours | 28.4 |" in report  # gated evidence table inlined after 06
    assert "<!--anchor:" in report  # the claim number got a three-layer anchor


def test_write_branch1_llm_blocks_unanchored_perf_claim(tmp_path: Path) -> None:
    ara = _ara(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("Our model reaches a BLEU of 28.4.\n", encoding="utf-8")  # 0.99 NOT here
    person = tmp_path / "person_vault" / "k"

    def bad_write_report(ara_dir: Path) -> dict[str, str]:
        # A loose performance number not in the MD -> cannot anchor -> hard-gate.
        return {"06_实验": "## 实验\n我们在 mAP 上达到 0.99,大幅超过基线。"}

    with pytest.raises(AnchorGateError):
        write_branch1_llm(person, {"title": "X"}, ara, md, bad_write_report, key="k")
