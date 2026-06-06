"""Bibliographic export (ROADMAP B2): BibTeX + CSL-JSON for the corpus."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from scripts.bibliography import generate_bibliography


def _write_paper(workspace: Path, entry_name: str, **fm) -> None:
    ara = workspace / "ai_package" / entry_name / "ara"
    ara.mkdir(parents=True)
    front = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    (ara / "PAPER.md").write_text(f"---\n{front}\n---\n\n# {fm['title']}\n", encoding="utf-8")


def test_generate_bibliography_writes_bibtex_and_csl(tmp_path):
    _write_paper(
        tmp_path,
        "2026-06-05_Attn_1706.03762",
        key="1706.03762",
        title="Attention Is All You Need",
        authors=["Vaswani, Ashish", "Shazeer, Noam"],
        year=2017,
        venue="NeurIPS",
        doi="10.5555/x",
    )
    _write_paper(
        tmp_path,
        "2026-06-05_Diff_2411.15139",
        key="2411.15139",
        title="DiffusionDrive",
        authors=["Liao et al."],
        year=2026,
        venue="CVPR",
        doi=None,
    )

    res = generate_bibliography(tmp_path)
    assert res.count == 2

    bib = res.bib_path.read_text(encoding="utf-8")
    assert "@article{170603762," in bib  # cite key = alnum-only of the key
    assert "title = {Attention Is All You Need}," in bib
    assert "author = {Vaswani, Ashish and Shazeer, Noam}," in bib
    assert "journal = {NeurIPS}," in bib

    csl = json.loads(res.csl_path.read_text(encoding="utf-8"))
    assert len(csl) == 2
    attn = next(r for r in csl if r["title"] == "Attention Is All You Need")
    assert attn["type"] == "article-journal"
    assert attn["issued"]["date-parts"] == [[2017]]
    assert attn["container-title"] == "NeurIPS"
    assert attn["DOI"] == "10.5555/x"
    assert attn["author"] == [{"literal": "Vaswani, Ashish"}, {"literal": "Shazeer, Noam"}]


def test_generate_bibliography_empty_corpus_is_safe(tmp_path):
    res = generate_bibliography(tmp_path)
    assert res.count == 0
    assert res.bib_path.read_text(encoding="utf-8") == ""
    assert json.loads(res.csl_path.read_text(encoding="utf-8")) == []
