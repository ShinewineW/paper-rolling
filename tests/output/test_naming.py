"""Deterministic naming, vault key, and per-identity overwrite glob (OT-1/2/3)."""

from __future__ import annotations

import datetime

import pytest
from scripts.output.naming import (
    derive_name,
    find_existing_entries,
    identity_base,
    resolve_paper_paths,
    vault_key,
)


def _scaffold(ws, idbase, *, corpus_slug, vault_key_name, html=False):
    """Build the on-disk product layout for one paper (two divergent key schemes)."""
    cdir = ws / "corpus" / f"{idbase}_{corpus_slug}"
    cdir.mkdir(parents=True)
    (cdir / f"{idbase}_{corpus_slug}.md").write_text("md", encoding="utf-8")
    pv = ws / "person_vault" / vault_key_name
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("r", encoding="utf-8")
    if html:
        (pv / "report.html").write_text("<html>", encoding="utf-8")
    (ws / "ai_package" / vault_key_name / "ara").mkdir(parents=True)


def test_resolve_paper_paths_spans_two_key_schemes(tmp_path):
    # the whole point: corpus Slug ('...ForPhy') != vault Name ('...PhysicalAI'),
    # neither is bare idbase — resolution must still find both from one idbase.
    idb = "2501.03575"
    _scaffold(
        tmp_path,
        idb,
        corpus_slug="CosmosWorldFoundationModelPlatformForPhy",
        vault_key_name=f"2026-06-08_CosmosWorldFoundationModelPlatformForPhysicalAI_{idb}",
    )
    pp = resolve_paper_paths(tmp_path, idb)
    assert pp.corpus_md is not None and pp.corpus_md.name.endswith(".md")
    assert pp.corpus_md.read_text() == "md"
    assert pp.report_md is not None and pp.report_md.exists()
    assert pp.ara_dir is not None and pp.ara_dir.is_dir()
    # report_html path is BUILT even though the file is absent (writer/REVISE target)
    assert pp.report_html is not None and pp.report_html.name == "report.html"
    assert not pp.report_html.exists()


def test_resolve_paper_paths_missing_paper_all_none(tmp_path):
    (tmp_path / "corpus").mkdir()
    pp = resolve_paper_paths(tmp_path, "9999.99999")
    assert pp.corpus_dir is None and pp.corpus_md is None
    assert pp.person_vault_dir is None and pp.report_md is None and pp.report_html is None
    assert pp.ai_package_dir is None and pp.ara_dir is None


def test_resolve_paper_paths_doi_identity(tmp_path):
    idb = "doi-abcd1234"  # DOI-only papers key the same way (_{idbase} / {idbase}_)
    _scaffold(
        tmp_path, idb, corpus_slug="SomeVenuePaper", vault_key_name=f"2026-06-08_SomeVenue_{idb}"
    )
    pp = resolve_paper_paths(tmp_path, idb)
    assert pp.corpus_md is not None and pp.ara_dir is not None and pp.report_md is not None


def test_resolve_paper_paths_does_not_match_idbase_substring(tmp_path):
    # '_{idbase}' suffix / '{idbase}_' prefix must not match a longer idbase that merely
    # contains the query (e.g. querying 2501.0357 must not return 2501.03575's dirs).
    _scaffold(
        tmp_path, "2501.03575", corpus_slug="Real", vault_key_name="2026-06-08_Real_2501.03575"
    )
    pp = resolve_paper_paths(tmp_path, "2501.0357")
    assert pp.corpus_dir is None and pp.person_vault_dir is None and pp.ai_package_dir is None


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("DiffusionDrive: Truncated Diffusion for Planning", "DiffusionDrive"),
        ("Attention Is All You Need", "AttentionIsAllYouNeed"),
        ("BEVFormer: Learning Bird's-Eye-View", "BEVFormer"),
        ("   spaced   out  ", "SpacedOut"),
        ("3D Gaussian Splatting!!!", "3DGaussianSplatting"),
    ],
)
def test_derive_name_is_deterministic_camelcase(title: str, expected: str) -> None:
    assert derive_name(title) == expected
    # Idempotent / stable across calls.
    assert derive_name(title) == derive_name(title)


def test_derive_name_truncates_long_titles_to_60_chars() -> None:
    long_title = "A " * 80 + "Method"
    name = derive_name(long_title)
    assert len(name) <= 60
    assert name  # never empty


def test_derive_name_empty_title_raises() -> None:
    with pytest.raises(ValueError, match="empty"):
        derive_name("   ")


def test_identity_base_prefers_arxiv_then_doi() -> None:
    assert identity_base(arxiv_id="2403.12345", doi="10.1/x") == "2403.12345"
    # DOI fallback -> 8-char hex short hash, stable.
    h = identity_base(arxiv_id=None, doi="10.1145/3592979.3593412")
    assert h.startswith("doi-")
    assert len(h) == len("doi-") + 8
    assert identity_base(arxiv_id=None, doi="10.1145/3592979.3593412") == h


def test_identity_base_strips_only_trailing_version() -> None:
    # Modern IDs: a trailing vN is stripped.
    assert identity_base(arxiv_id="2403.12345v2", doi=None) == "2403.12345"
    # Old-style IDs with a 'v' INSIDE the category must NOT be split at the first
    # 'v' (Codex R16 — a naive split("v") gave "sol"); strip only the trailing vN.
    assert identity_base(arxiv_id="solv-int/9901001v1", doi=None) == "solv-int/9901001"
    assert identity_base(arxiv_id="solv-int/9901001", doi=None) == "solv-int/9901001"


def test_vault_key_is_date_name_idbase() -> None:
    key = vault_key(
        intake=datetime.date(2026, 6, 5),
        title="DiffusionDrive: Truncated Diffusion",
        arxiv_id="2411.15139",
        doi=None,
    )
    assert key == "2026-06-05_DiffusionDrive_2411.15139"


def test_find_existing_entries_ignores_date_prefix(tmp_path) -> None:
    vault = tmp_path / "person_vault"
    vault.mkdir()
    (vault / "2026-05-01_DiffusionDrive_2411.15139").mkdir()
    (vault / "2026-05-01_OtherPaper_1234.56789").mkdir()
    hits = find_existing_entries(vault, arxiv_id="2411.15139", doi=None)
    assert [p.name for p in hits] == ["2026-05-01_DiffusionDrive_2411.15139"]
