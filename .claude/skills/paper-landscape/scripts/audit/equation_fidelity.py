"""Equation-fidelity check — MECHANICAL, no LLM (audit-D1).

Counts MinerU typed formula blocks in `content_list.json` and matches them
against the count of display-math `$$ ... $$` blocks in the converted MD. A
mismatch means MinerU/HTML conversion dropped or garbled an equation; the
derivation path downstream cannot trust the MD math, so this is a hard block
(the paper's math highlight is later marked UNRELIABLE_SOURCE and the
derivation suppressed — but that decision lives in the illustration author;
here we only emit the fidelity verdict).

Deliberately dumb: a regex count + a JSON type count. No model call, fully
deterministic, fast.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.audit.types import Finding, GateVerdict, Severity

# `$$` on its own — a display-math delimiter. Two delimiters = one block.
# We count delimiters and divide by 2 (floor) so an odd unterminated `$$`
# does not silently inflate the count.
_DISPLAY_DELIM = re.compile(r"(?<![\\$])\$\$(?!\$)")

_FORMULA_TYPES = frozenset({"equation", "formula", "interline_equation"})


def count_display_math_blocks(md_text: str) -> int:
    """Number of `$$ ... $$` display-math blocks in the MD (inline `$x$` ignored)."""
    delimiters = len(_DISPLAY_DELIM.findall(md_text))
    return delimiters // 2


def count_formula_blocks(content_list_path: Path) -> int:
    """Number of typed formula blocks in MinerU's content_list.json.

    MinerU labels display equations with `type` in {equation, formula,
    interline_equation} depending on backend/version; we accept any of them.
    """
    blocks = json.loads(content_list_path.read_text(encoding="utf-8"))
    return sum(1 for b in blocks if isinstance(b, dict) and b.get("type") in _FORMULA_TYPES)


def check_equation_fidelity(md_path: Path, content_list_path: Path) -> GateVerdict:
    """Compare formula-block counts; hard-block on mismatch."""
    md_count = count_display_math_blocks(md_path.read_text(encoding="utf-8"))
    cl_count = count_formula_blocks(content_list_path)

    if md_count == cl_count:
        return GateVerdict(gate="equation-fidelity", findings=())

    finding = Finding(
        finding_id="EQ01",
        severity=Severity.CRITICAL,
        target=str(md_path.name),
        observation=(
            f"equation-block count mismatch: content_list.json has {cl_count} "
            f"typed formula block(s) but MD has {md_count} `$$` display block(s)"
        ),
        is_hard_block=True,
        reasoning=(
            "A drift between MinerU's typed formula blocks and the rendered MD "
            "math means at least one equation was dropped or garbled in "
            "conversion; the MD math is unreliable as a derivation source."
        ),
        suggestion=(
            "Re-convert via the marker fallback (never re-read the PDF); if it "
            "still mismatches, mark the math highlight math:UNRELIABLE_SOURCE "
            "and suppress the derivation."
        ),
    )
    return GateVerdict(gate="equation-fidelity", findings=(finding,))
