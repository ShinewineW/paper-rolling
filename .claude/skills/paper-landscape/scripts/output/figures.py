# .claude/skills/paper-landscape/scripts/output/figures.py
r"""Original-figure inventory for the human report (论文原图导览).

The human report is a "paper guided tour", not just commentary. The selection is
SELECTIVE, not all-figures: the core method / model-structure overview diagram is
MANDATORY (强制,原模原样), plus a FEW representative result/effect figures — the
rest (minor/table-screenshot figures) are skipped. The ingest layer (MinerU
Tier-2 / pandoc Tier-1) extracts the figures to ``corpus/{id}/images/`` and
references them in the frozen MD as ``![](images/HASH.ext)`` with a following
``Figure N: ...`` caption line.

This module extracts that ordered figure list (path + caption), flags the
architecture/method figure(s) via ``is_architecture_caption``, and copies the
selected images into the report's vault dir so report.md / report.html resolve
them. The writer (curate_figures) decides role + inclusion; branch1_llm embeds the
selected figures (deterministic paths — no LLM hash reproduction). ADR-0012 rev: a
missing selected / mandatory architecture figure is NOT a hard gate — branch1 always
publishes and the gap is surfaced as a 配图提示 note in the opening 「评价」.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

_IMG_REF = re.compile(r"!\[[^\]]*\]\((images/[^)\s]+)\)")
_TAG = re.compile(r"</?su[bp]>")  # MinerU wraps caption fragments in <sub>/<sup>
# Caption cues for the MANDATORY core method / model-structure overview figure(s):
# those must appear verbatim in the human report; result/effect figures are
# selected, not all-included.
_ARCH_CUE = re.compile(
    r"(?i)(architecture|overview|framework|pipeline|model\s+structure|the\s+method|"
    r"our\s+(model|method|approach|framework|pipeline)|架构|框架|流程|结构|总览|整体|方法概览)"
)
_CAP_CUE = re.compile(r"(?i)^(figure|fig\.?|table|tab\.?|图|表)\s*\d")


def is_architecture_caption(caption: str) -> bool:
    """True if a figure caption signals the core method / model-structure diagram
    (mandatory in the human report)."""
    return bool(_ARCH_CUE.search(caption or ""))


@dataclass(frozen=True)
class Figure:
    """One original figure: its in-MD ref path + a cleaned caption."""

    ref: str  # e.g. "images/HASH.jpg" (relative, as the report will reference it)
    caption: str  # cleaned caption text (English, verbatim-ish from the paper)


def extract_figures(md_path: Path) -> list[Figure]:
    """Ordered, de-duplicated original figures referenced in the frozen MD.

    Caption: scan the lines after the ref (tag-stripped), SKIPPING blanks and other
    image refs (consecutive grid images carry no caption between them — the group
    caption follows). Prefer a real ``Figure N: …`` caption line; else the first
    text line; else empty.
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
        window: list[str] = []
        for nxt in lines[i + 1 : i + 9]:
            stripped = _TAG.sub("", nxt).strip()
            if not stripped or _IMG_REF.search(stripped):  # skip blanks + adjacent images
                continue
            window.append(stripped)
        caption = next((w for w in window if _CAP_CUE.search(w)), window[0] if window else "")
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
