# .claude/skills/paper-landscape/scripts/output/figures.py
r"""Original-figure inventory for the human report (论文原图导览).

The human report is a "paper guided tour", not just commentary: every ORIGINAL
figure the paper shows MUST appear in it (强制要求 — as many as the paper has).
The ingest layer (MinerU Tier-2 / pandoc Tier-1) already extracts the figures to
``corpus/{id}/images/`` and references them in the frozen MD as
``![](images/HASH.ext)`` with a following ``Figure N: ...`` caption line.

This module extracts that ordered figure list (path + caption) and copies the
referenced images into the report's vault dir so report.md / report.html resolve
them. branch1_llm then embeds EVERY figure (deterministic paths — no LLM hash
reproduction) with an LLM science-pop narration, and hard-gates on completeness.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

_IMG_REF = re.compile(r"!\[[^\]]*\]\((images/[^)\s]+)\)")
_TAG = re.compile(r"</?su[bp]>")  # MinerU wraps caption fragments in <sub>/<sup>


@dataclass(frozen=True)
class Figure:
    """One original figure: its in-MD ref path + a cleaned caption."""

    ref: str  # e.g. "images/HASH.jpg" (relative, as the report will reference it)
    caption: str  # cleaned caption text (English, verbatim-ish from the paper)


def extract_figures(md_path: Path) -> list[Figure]:
    """Ordered, de-duplicated original figures referenced in the frozen MD.

    Caption = the first non-empty line after the image ref, tag-stripped (MinerU
    puts ``Figure N: …`` there); empty if none.
    """
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    figs: list[Figure] = []
    seen: set[str] = set()
    for i, line in enumerate(lines):
        m = _IMG_REF.search(line)
        if not m:
            continue
        ref = m.group(1)
        if ref in seen:
            continue
        seen.add(ref)
        caption = ""
        for nxt in lines[i + 1 : i + 4]:
            stripped = _TAG.sub("", nxt).strip()
            if stripped:
                caption = stripped
                break
        figs.append(Figure(ref=ref, caption=caption[:300]))
    return figs


def copy_figures(figures: list[Figure], src_md_dir: Path, dst_dir: Path) -> list[Figure]:
    """Copy each referenced image from the corpus into ``dst_dir`` (the vault
    entry). Returns the figures that were successfully copied (so the report only
    embeds images it actually has)."""
    out: list[Figure] = []
    for fig in figures:
        src = Path(src_md_dir) / fig.ref
        if src.is_file():
            dst = Path(dst_dir) / fig.ref
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            out.append(fig)
    return out
