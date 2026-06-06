"""Bibliographic export (ROADMAP B2): BibTeX + CSL-JSON for the corpus.

Scans every sealed `ai_package/<key>/ara/PAPER.md` frontmatter (title / authors /
year / venue / doi) and writes `references.bib` + `references.csl.json` at the
workspace root, so the discovered corpus is reusable in reference managers
(Zotero, etc.). Read-only over the vaults; a pure aggregator like landscapes.

Source: academic-research-skills CSL-JSON `literature_corpus`; scientific-agent-
skills pyzotero integration.

CLI: `python -m scripts.bibliography --topic-dir <dir>`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

# A BibTeX cite key is alphanumeric only.
_CITEKEY = re.compile(r"[^A-Za-z0-9]+")


@dataclass(frozen=True)
class BibliographyResult:
    count: int
    bib_path: Path
    csl_path: Path


def _read_frontmatter(paper_md: Path) -> dict:
    """Parse the leading `---` YAML frontmatter of a PAPER.md, or {} if absent."""
    text = paper_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def _cite_key(fm: dict) -> str:
    raw = str(fm.get("key") or fm.get("doi") or fm.get("title") or "ref")
    return _CITEKEY.sub("", raw) or "ref"


def _bibtex_entry(fm: dict) -> str:
    fields = {
        "title": fm.get("title") or "",
        "author": " and ".join(fm.get("authors") or []) or "Unknown",
        "year": fm.get("year") or "",
        "journal": fm.get("venue") or "",
        "doi": fm.get("doi") or "",
    }
    lines = [f"@article{{{_cite_key(fm)},"]
    lines += [f"  {k} = {{{v}}}," for k, v in fields.items() if v]
    lines.append("}")
    return "\n".join(lines)


def _csl_record(fm: dict) -> dict:
    rec: dict = {"id": _cite_key(fm), "type": "article-journal", "title": fm.get("title") or ""}
    if fm.get("authors"):
        rec["author"] = [{"literal": a} for a in fm["authors"]]
    if fm.get("year"):
        rec["issued"] = {"date-parts": [[fm["year"]]]}
    if fm.get("venue"):
        rec["container-title"] = fm["venue"]
    if fm.get("doi"):
        rec["DOI"] = fm["doi"]
    return rec


def generate_bibliography(workspace: Path) -> BibliographyResult:
    """Write references.bib + references.csl.json for every sealed ai_package."""
    workspace = Path(workspace)
    ai_dir = workspace / "ai_package"
    frontmatters = []
    if ai_dir.exists():
        for paper_md in sorted(ai_dir.glob("*/ara/PAPER.md")):
            fm = _read_frontmatter(paper_md)
            if fm.get("title"):  # skip entries missing the minimum bib field
                frontmatters.append(fm)

    bib_path = workspace / "references.bib"
    csl_path = workspace / "references.csl.json"
    bib_path.write_text(
        "\n\n".join(_bibtex_entry(fm) for fm in frontmatters) + ("\n" if frontmatters else ""),
        encoding="utf-8",
    )
    csl_path.write_text(
        json.dumps([_csl_record(fm) for fm in frontmatters], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return BibliographyResult(count=len(frontmatters), bib_path=bib_path, csl_path=csl_path)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog="paper-landscape-bibliography")
    parser.add_argument("--topic-dir", type=Path, required=True, help="workspace root")
    args = parser.parse_args()
    result = generate_bibliography(args.topic_dir)
    print(f"wrote {result.count} references -> {result.bib_path} + {result.csl_path}")
    sys.exit(0)
