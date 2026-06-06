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


# --- is_ad_domain whitelist selection (foundation review: the flag must be a
#     real consumer, not a dead config knob). No explicit override is given, so
#     the flag itself selects the general vs general+AD whitelist set.


def _bare(institutions=None, venue=None):
    return {
        "cited_by_count": 0,
        "year": 2026,
        "venue": venue,
        "institutions": institutions or [],
        "github_stars": None,
        "upvotes": None,
    }


def test_is_ad_domain_false_drops_ad_only_institution_keeps_general():
    waymo, google = _bare(institutions=["Waymo"]), _bare(institutions=["Google DeepMind"])
    off = {"current_year": 2026, "is_ad_domain": False}
    on = {"current_year": 2026, "is_ad_domain": True}
    assert score_authority(waymo, off)[0]["s3_institution"] is False  # AD org dropped
    assert score_authority(waymo, on)[0]["s3_institution"] is True  # AD org kept when AD
    assert score_authority(google, off)[0]["s3_institution"] is True  # general lab always


def test_is_ad_domain_false_drops_ad_only_venue_keeps_general():
    off = {"current_year": 2026, "is_ad_domain": False}
    assert score_authority(_bare(venue="CoRL"), off)[0]["s2_venue"] is False  # robotics dropped
    assert score_authority(_bare(venue="CVPR"), off)[0]["s2_venue"] is True  # general kept


def test_absent_is_ad_domain_preserves_full_default():
    # A discovery config that does not carry is_ad_domain keeps the historical
    # general+AD set (backward-compatible default).
    assert score_authority(_bare(institutions=["Waymo"]), {"current_year": 2026})[0][
        "s3_institution"
    ]
