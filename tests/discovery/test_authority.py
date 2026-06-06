"""Multi-signal OR authority scorer (ADR-0001): no citation hard floor."""

from __future__ import annotations

from scripts.discovery.authority import (
    DEFAULT_INSTITUTION_WHITELIST,
    DEFAULT_VENUE_ALLOWLIST,
    score_authority,
)

CFG = {
    "current_year": 2026,
    "venue_allowlist": DEFAULT_VENUE_ALLOWLIST,
    "institution_whitelist": DEFAULT_INSTITUTION_WHITELIST,
}


def test_high_citation_triggers_s1():
    c = {
        "cited_by_count": 5000,
        "year": 2017,
        "venue": None,
        "institutions": [],
        "github_stars": None,
        "upvotes": None,
    }
    sig, _ = score_authority(c, CFG)
    assert sig["s1_cite"] is True


def test_recent_zero_cite_top_venue_triggers_s2_not_s1():
    # ADR-0001 core case: CVPR 2026, 0 citations — must still be authoritative.
    c = {
        "cited_by_count": 0,
        "year": 2026,
        "venue": "CVPR",
        "institutions": [],
        "github_stars": None,
        "upvotes": None,
    }
    sig, score = score_authority(c, CFG)
    assert sig["s1_cite"] is False
    assert sig["s2_venue"] is True
    assert score > 0  # authoritative despite zero citations


def test_institution_whitelist_triggers_s3():
    c = {
        "cited_by_count": 0,
        "year": 2026,
        "venue": None,
        "institutions": ["Google DeepMind"],
        "github_stars": None,
        "upvotes": None,
    }
    sig, _ = score_authority(c, CFG)
    assert sig["s3_institution"] is True


def test_github_and_hf_heat_triggers_s4():
    c = {
        "cited_by_count": 0,
        "year": 2026,
        "venue": None,
        "institutions": [],
        "github_stars": 800,
        "upvotes": 120,
    }
    sig, _ = score_authority(c, CFG)
    assert sig["s4_heat"] is True


def test_no_signal_scores_zero_and_is_not_authoritative():
    c = {
        "cited_by_count": 0,
        "year": 2026,
        "venue": "RandomWorkshop",
        "institutions": ["Unknown U"],
        "github_stars": 1,
        "upvotes": 0,
    }
    sig, score = score_authority(c, CFG)
    assert not any(sig.values())
    assert score == 0.0


def test_citation_velocity_lifts_recent_paper():
    # 300 cites in 1 year (velocity) beats 300 cites in 9 years on the S1 axis.
    fast = {
        "cited_by_count": 300,
        "year": 2025,
        "venue": None,
        "institutions": [],
        "github_stars": None,
        "upvotes": None,
    }
    slow = {
        "cited_by_count": 300,
        "year": 2017,
        "venue": None,
        "institutions": [],
        "github_stars": None,
        "upvotes": None,
    }
    _, fast_score = score_authority(fast, CFG)
    _, slow_score = score_authority(slow, CFG)
    assert fast_score > slow_score


def test_venue_match_is_substring_case_insensitive():
    c = {
        "cited_by_count": 0,
        "year": 2026,
        "venue": "Proceedings of CVPR 2026",
        "institutions": [],
        "github_stars": None,
        "upvotes": None,
    }
    sig, _ = score_authority(c, CFG)
    assert sig["s2_venue"] is True
