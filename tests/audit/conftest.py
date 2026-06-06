from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def paper_md(tmp_path: Path) -> Path:
    """A minimal MD with two display-math blocks and one inline span."""
    md = tmp_path / "1706.03762v5_Transformer.md"
    md.write_text(
        "# Attention Is All You Need\n\n"
        "We define attention as\n\n"
        "$$\n"
        "\\mathrm{Attention}(Q,K,V)=\\mathrm{softmax}(QK^T/\\sqrt{d})V\n"
        "$$\n\n"
        "and the per-head projection\n\n"
        "$$\n"
        "\\mathrm{head}_i = \\mathrm{Attention}(QW_i^Q, KW_i^K, VW_i^V)\n"
        "$$\n\n"
        "The model achieves a BLEU score of 28.4 on WMT14 En-De.\n",
        encoding="utf-8",
    )
    return md


@pytest.fixture
def content_list(tmp_path: Path) -> Path:
    """MinerU content_list.json with two typed formula blocks (matches paper_md)."""
    path = tmp_path / "content_list.json"
    blocks = [
        {"type": "text", "text": "Attention Is All You Need"},
        {"type": "equation", "text": "\\mathrm{Attention}(Q,K,V)=..."},
        {"type": "text", "text": "and the per-head projection"},
        {"type": "equation", "text": "\\mathrm{head}_i = ..."},
        {"type": "text", "text": "The model achieves a BLEU score of 28.4"},
    ]
    path.write_text(json.dumps(blocks), encoding="utf-8")
    return path
