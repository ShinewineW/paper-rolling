"""corpus.jsonl — the discovered-paper known set (§3.1).

One JSON object per line, append-only. Extends the upstream
literature_corpus_entry schema with citation count, arxiv version, pdf/md
paths, and discovery tier (verified-absent upstream fields).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CorpusRecord:
    """One discovered paper.

    Bold fields in §3.1 are the additions over the upstream schema:
    cited_by_count, influential_citation_count, arxiv_version, discovery_tier,
    pdf_path, md_path.
    """

    citation_key: str
    arxiv_id: str | None
    arxiv_version: str | None
    doi: str | None
    title: str
    year: int | None
    cited_by_count: int | None
    influential_citation_count: int | None
    discovery_tier: str  # "A" | "B" | "C"
    pdf_path: str | None
    md_path: str | None
    obtained_via: str
    obtained_at: str


def append_record(path: Path, record: CorpusRecord) -> None:
    """Append one record as a single JSON line (creates parent dir + file)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_records(path: Path) -> list[CorpusRecord]:
    """Load all records; missing file → empty list; blank lines ignored."""
    if not path.exists():
        return []
    out: list[CorpusRecord] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(CorpusRecord(**json.loads(line)))
    return out
