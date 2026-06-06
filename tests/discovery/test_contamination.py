"""Preprint trust flag (吸收-D2): non-blocking; shares the PREPRINT_VENUES list."""

from __future__ import annotations

from scripts.discovery.contamination import PREPRINT_VENUES, preprint_flag


def test_preprint_venues_match_ars_closed_list():
    # Same 10-venue closed list as academic-research-skills
    # contamination_signals.PREPRINT_VENUES (shared factual data, not vendored code).
    assert PREPRINT_VENUES == frozenset(
        {
            "arXiv",
            "bioRxiv",
            "medRxiv",
            "SSRN",
            "Research Square",
            "Preprints.org",
            "ChemRxiv",
            "EarthArXiv",
            "OSF Preprints",
            "TechRxiv",
        }
    )


def test_explicit_preprint_venue_flags_true():
    assert preprint_flag({"venue": "arXiv", "year": 2026}) is True


def test_published_venue_flags_false():
    assert preprint_flag({"venue": "CVPR", "year": 2026}) is False


def test_arxiv_only_candidate_flags_true():
    # arxiv source with no venue but an arxiv_id -> preprint.
    assert (
        preprint_flag({"venue": None, "arxiv_id": "2601.01234", "doi": None, "year": 2026}) is True
    )


def test_doi_no_arxiv_no_venue_flags_false():
    assert preprint_flag({"venue": None, "arxiv_id": None, "doi": "10.1/x", "year": 2024}) is False


def test_oa_pdf_arxiv_url_infers_preprint():
    assert (
        preprint_flag(
            {
                "venue": None,
                "arxiv_id": None,
                "doi": None,
                "oa_pdf_url": "https://arxiv.org/pdf/2601.1",
            }
        )
        is True
    )
