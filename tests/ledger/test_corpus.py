"""corpus.jsonl round-trip + extended schema (§3.1)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_CORPUS = (
    Path(__file__).resolve().parents[2] / ".claude/skills/paper-landscape/scripts/ledger/corpus.py"
)
_spec = importlib.util.spec_from_file_location("corpus", _CORPUS)
corpus = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(corpus)


def _record():
    return corpus.CorpusRecord(
        citation_key="vaswani2017attention",
        arxiv_id="1706.03762",
        arxiv_version="v5",
        doi="10.5555/3295222.3295349",
        title="Attention Is All You Need",
        year=2017,
        cited_by_count=134000,
        influential_citation_count=8200,
        discovery_tier="A",
        pdf_path="corpus/1706.03762v5/1706.03762v5.pdf",
        md_path="corpus/1706.03762v5/1706.03762v5.md",
        obtained_via="openalex",
        obtained_at="2026-06-05T10:00:00Z",
    )


def test_append_and_load_roundtrip(tmp_path):
    p = tmp_path / "corpus.jsonl"
    rec = _record()
    corpus.append_record(p, rec)
    loaded = corpus.load_records(p)
    assert len(loaded) == 1
    assert loaded[0] == rec


def test_append_is_one_line_per_record(tmp_path):
    p = tmp_path / "corpus.jsonl"
    corpus.append_record(p, _record())
    corpus.append_record(p, _record())
    assert len(p.read_text(encoding="utf-8").splitlines()) == 2


def test_load_missing_file_returns_empty(tmp_path):
    assert corpus.load_records(tmp_path / "nope.jsonl") == []


def test_record_carries_extended_fields(tmp_path):
    rec = _record()
    # Fields ADDED over the upstream schema (§3.1).
    assert rec.cited_by_count == 134000
    assert rec.arxiv_version == "v5"
    assert rec.discovery_tier == "A"
    assert rec.pdf_path.endswith(".pdf")
    assert rec.md_path.endswith(".md")


def test_load_skips_blank_lines(tmp_path):
    p = tmp_path / "corpus.jsonl"
    corpus.append_record(p, _record())
    with p.open("a", encoding="utf-8") as f:
        f.write("\n")  # trailing blank line tolerated
    assert len(corpus.load_records(p)) == 1
