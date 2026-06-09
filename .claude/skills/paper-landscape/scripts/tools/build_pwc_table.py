# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb"]
# ///
"""Build the shipped offline `arxiv_id -> official repo` lookup (code_ref T2a).

OFFLINE BUILD TOOL — not runtime. Downloads the Papers with Code frozen dump
(`pwc-archive/links-between-paper-and-code` on HF), keeps only `is_official=true`
rows with an arxiv_id, and writes a gzipped TSV the engine reads with stdlib only
(no duckdb/pyarrow at runtime).

PwC was sunset ~2025-09 and the dump is effectively static, so this is a rare
manual refresh; post-freeze papers are covered at runtime by T2b (HF live) / T4.

Usage:
    uv run .claude/skills/paper-landscape/scripts/tools/build_pwc_table.py \
        [--parquet <local.parquet>] [--out <data/pwc_official_arxiv2repo.tsv.gz>]

`--parquet` reuses an already-downloaded dump (avoids HF range-request 429s);
omit it to download via the HF parquet API (set HF_TOKEN for a higher rate).
"""

from __future__ import annotations

import argparse
import gzip
import os
from pathlib import Path

import duckdb

_DUMP_URL = (
    "https://huggingface.co/api/datasets/pwc-archive/"
    "links-between-paper-and-code/parquet/default/train/0.parquet"
)
_DEFAULT_OUT = Path(__file__).resolve().parents[2] / "data" / "pwc_official_arxiv2repo.tsv.gz"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parquet", help="local parquet path; omit to read the HF URL")
    ap.add_argument("--out", type=Path, default=_DEFAULT_OUT)
    args = ap.parse_args()

    src = args.parquet or _DUMP_URL
    con = duckdb.connect()
    if not args.parquet:
        token = os.environ.get("HF_TOKEN")
        con.execute("INSTALL httpfs; LOAD httpfs;")
        if token:
            con.execute(f"SET http_headers={{'Authorization': 'Bearer {token}'}};")

    # One official repo per arxiv_id (dedupe; prefer the lexicographically first
    # repo_url for determinism — official links are rarely ambiguous per paper).
    rows = con.execute(
        f"""
        SELECT paper_arxiv_id, min(repo_url) AS repo_url
        FROM read_parquet('{src}')
        WHERE is_official
          AND paper_arxiv_id IS NOT NULL AND paper_arxiv_id <> ''
          AND repo_url IS NOT NULL AND repo_url <> ''
        GROUP BY paper_arxiv_id
        ORDER BY paper_arxiv_id
        """
    ).fetchall()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(args.out, "wt", encoding="utf-8") as f:
        for arxiv_id, repo_url in rows:
            f.write(f"{arxiv_id}\t{repo_url}\n")

    size_kb = round(args.out.stat().st_size / 1024, 1)
    print(f"wrote {len(rows)} official arxiv->repo rows to {args.out} ({size_kb} KB)")


if __name__ == "__main__":
    main()
