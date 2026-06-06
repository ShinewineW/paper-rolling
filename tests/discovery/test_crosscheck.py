"""Self-contained smoke test for the NET-NEW DOI cross-check (no ARS fixture)."""

from __future__ import annotations

from scripts.discovery.crosscheck import doi_title_crosscheck


def test_matching_title_accepts():
    rec = doi_title_crosscheck("10.1/x", "Attention Is All You Need", "Attention is all you need!")
    assert rec is not None and rec["doi"] == "10.1/x"


def test_mismatched_title_rejects_as_doi_mismatch():
    assert (
        doi_title_crosscheck("10.1/y", "Some Other Paper Entirely", "Attention Is All You Need")
        is None
    )
