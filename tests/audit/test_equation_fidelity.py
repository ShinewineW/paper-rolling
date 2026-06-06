from __future__ import annotations

import json
from pathlib import Path

from scripts.audit.equation_fidelity import (
    check_equation_fidelity,
    count_display_math_blocks,
    count_formula_blocks,
)


def test_count_display_math_blocks_counts_dollar_pairs(paper_md: Path) -> None:
    assert count_display_math_blocks(paper_md.read_text(encoding="utf-8")) == 2


def test_count_formula_blocks_counts_typed_equation_entries(content_list: Path) -> None:
    assert count_formula_blocks(content_list) == 2


def test_check_equation_fidelity_passes_when_counts_match(
    paper_md: Path, content_list: Path
) -> None:
    verdict = check_equation_fidelity(paper_md, content_list)
    assert verdict.blocked is False
    assert verdict.findings == ()


def test_check_equation_fidelity_blocks_on_count_mismatch(tmp_path: Path, paper_md: Path) -> None:
    # content_list claims 3 equations but MD has only 2 $$ blocks.
    cl = tmp_path / "content_list.json"
    cl.write_text(
        json.dumps(
            [
                {"type": "equation", "text": "a"},
                {"type": "equation", "text": "b"},
                {"type": "equation", "text": "c"},
            ]
        ),
        encoding="utf-8",
    )
    verdict = check_equation_fidelity(paper_md, cl)
    assert verdict.blocked is True
    finding = verdict.hard_findings[0]
    assert "3" in finding.observation and "2" in finding.observation
    assert finding.is_hard_block is True


def test_check_equation_fidelity_ignores_inline_dollar_math(tmp_path: Path) -> None:
    md = tmp_path / "p.md"
    md.write_text(
        "Inline $x = y$ should not count. Display:\n\n$$\nE=mc^2\n$$\n",
        encoding="utf-8",
    )
    assert count_display_math_blocks(md.read_text(encoding="utf-8")) == 1


def test_check_equation_fidelity_handles_zero_equation_paper(tmp_path: Path) -> None:
    md = tmp_path / "p.md"
    md.write_text("No math here at all.\n", encoding="utf-8")
    cl = tmp_path / "cl.json"
    cl.write_text(json.dumps([{"type": "text", "text": "x"}]), encoding="utf-8")
    verdict = check_equation_fidelity(md, cl)
    assert verdict.blocked is False
