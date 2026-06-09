"""T2a: offline PwC `is_official` arxiv->repo lookup (code_ref repo resolution)."""

from __future__ import annotations

import gzip
from pathlib import Path

from scripts.output.pwc_lookup import official_repo


def _write_table(tmp_path: Path, rows: list[tuple[str, str]]) -> Path:
    p = tmp_path / "t.tsv.gz"
    with gzip.open(p, "wt", encoding="utf-8") as f:
        for aid, repo in rows:
            f.write(f"{aid}\t{repo}\n")
    return p


def test_official_repo_hits_and_misses(tmp_path: Path) -> None:
    tbl = _write_table(tmp_path, [("2411.15139", "https://github.com/hustvl/diffusiondrive")])
    assert official_repo("2411.15139", table_path=tbl) == "https://github.com/hustvl/diffusiondrive"
    assert official_repo("9999.99999", table_path=tbl) is None
    assert official_repo(None, table_path=tbl) is None


def test_official_repo_strips_arxiv_version(tmp_path: Path) -> None:
    # candidates may carry a version suffix; the table keys are versionless.
    tbl = _write_table(
        tmp_path, [("2407.01392", "https://github.com/buoyancy99/diffusion-forcing")]
    )
    assert official_repo("2407.01392v2", table_path=tbl) == (
        "https://github.com/buoyancy99/diffusion-forcing"
    )


def test_shipped_table_resolves_known_papers() -> None:
    # Smoke test against the real shipped table: the case that beat HF-live/websearch.
    assert official_repo("2407.01392") == "https://github.com/buoyancy99/diffusion-forcing"
    assert official_repo("2411.15139") == "https://github.com/hustvl/diffusiondrive"
