"""T2a — offline `arxiv_id -> official repo` lookup for code_ref resolution.

Reads the shipped, gzipped Papers-with-Code `is_official` table
(`data/pwc_official_arxiv2repo.tsv.gz`, built by `scripts/tools/build_pwc_table.py`)
with stdlib only — no duckdb/pyarrow at runtime. The table is lazily loaded into a
dict once per path and cached. Deterministic, zero-network; covers papers up to the
PwC freeze (~2025-09). Post-freeze papers are handled by T2b (HF live) / T4.
"""

from __future__ import annotations

import gzip
import re
from functools import cache
from pathlib import Path

_TABLE = Path(__file__).resolve().parents[2] / "data" / "pwc_official_arxiv2repo.tsv.gz"
_VERSION = re.compile(r"v\d+$")


@cache
def _load(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            aid, _, repo = line.partition("\t")
            repo = repo.rstrip("\n")
            if aid and repo:
                out[aid] = repo
    return out


def official_repo(arxiv_id: str | None, *, table_path: Path | None = None) -> str | None:
    """Return the official repo URL for `arxiv_id`, or None if not in the table.

    The version suffix (e.g. ``v2``) is stripped — table keys are versionless.
    """
    if not arxiv_id:
        return None
    key = _VERSION.sub("", arxiv_id.strip())
    return _load(str(table_path or _TABLE)).get(key)
