"""Deterministic naming, vault key, and per-identity overwrite glob (OT-1/2/3)."""

from __future__ import annotations

import datetime

import pytest
from scripts.output.naming import (
    derive_name,
    find_existing_entries,
    identity_base,
    vault_key,
)


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
