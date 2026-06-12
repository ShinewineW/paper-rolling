# tests/llm/test_seams.py
from __future__ import annotations


def test_build_seams_includes_faithfulness_judge() -> None:
    # ADR-0012: branch1 忠实门 (c) is the 7th routed seam.
    from scripts.llm.config import SEAMS
    from scripts.llm.seams import build_seams

    assert "faithfulness" in SEAMS
    assert "faithfulness_judge" in build_seams()
