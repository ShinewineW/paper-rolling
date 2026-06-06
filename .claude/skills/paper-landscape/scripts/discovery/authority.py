"""Multi-signal OR authority scorer (ADR-0001).

Net-new (CC-BY-NC repo). The discovery layer has NO citation hard floor (ADR-0001 supersedes
the old >=500 gate). A candidate is authoritative if it fires ANY of four
signals; a composite, recency-weighted score then orders the survivors:

  S1 cite      : high cited_by_count OR strong citation velocity (cites/age)
  S2 venue     : title's venue matches a top-venue allowlist (DBLP-confirmed)
  S3 institution: an authorship institution matches the org whitelist
  S4 heat      : GitHub stars + HF upvotes + recency (the search-index proxy)

Whitelists are split into a GENERAL set (always applied) and an AD/robotics
EXTRA set; the campaign's `is_ad_domain` flag selects whether the AD extra is
added (D-发现-5). `is_ad_domain` flows from the campaign (`CampaignConfig`) into
the discovery `config` dict (production wiring); a campaign config can still
override `venue_allowlist` / `institution_whitelist` outright.
"""

from __future__ import annotations

from typing import Any

# D-发现-5 GENERAL top venues (ML / CV / AI) — applied for every campaign.
GENERAL_VENUE_ALLOWLIST = (
    "NeurIPS",
    "ICML",
    "ICLR",
    "CVPR",
    "ICCV",
    "ECCV",
    "AAAI",
    "TPAMI",
    "IJCV",
)

# Autonomous-driving / robotics venues — added only when is_ad_domain.
AD_VENUE_ALLOWLIST = (
    "ICRA",
    "IROS",
    "CoRL",
    "RSS",
    "RA-L",
    "T-RO",
)

# Full default = general + AD (the historical list; used when is_ad_domain).
DEFAULT_VENUE_ALLOWLIST = GENERAL_VENUE_ALLOWLIST + AD_VENUE_ALLOWLIST

# D-发现-5 GENERAL institution whitelist (big AI/ML labs) — applied for every
# campaign (matched case-insensitively as substrings).
GENERAL_INSTITUTION_WHITELIST = (
    "Google",
    "DeepMind",
    "Meta",
    "FAIR",
    "NVIDIA",
    "Microsoft Research",
    "OpenAI",
    "Apple",
    "Amazon",
    "AI2",
    "SenseTime",
    "Megvii",
    "DAMO",
    "Tencent AI Lab",
    "ByteDance",
    "Noah",
)

# Autonomous-driving / robotics orgs — added only when is_ad_domain.
AD_INSTITUTION_WHITELIST = (
    "Waymo",
    "Tesla",
    "Wayve",
    "Cruise",
    "Nuro",
    "Toyota Research",
    "TRI",
    "Boston Dynamics",
    "Apollo",
    "Horizon",
    "Momenta",
    "Pony.ai",
    "Unitree",
)

# Full default = general + AD (the historical list; used when is_ad_domain).
DEFAULT_INSTITUTION_WHITELIST = GENERAL_INSTITUTION_WHITELIST + AD_INSTITUTION_WHITELIST

# Thresholds (initial; tunable via config per ADR-0001 consequence note).
_S1_CITE_FLOOR = 1000  # "classic high-cite"
_S1_VELOCITY_FLOOR = 100.0  # cites/year — catches fast risers
_S4_STARS_FLOOR = 300
_S4_UPVOTES_FLOOR = 50


def _velocity(cited_by_count: int, year: int | None, current_year: int) -> float:
    if not year:
        return 0.0
    age = max(current_year - year, 1)
    return cited_by_count / age


def _matches(text: str | None, needles: tuple[str, ...]) -> bool:
    if not text:
        return False
    low = text.lower()
    return any(n.lower() in low for n in needles)


def score_authority(
    candidate: dict[str, Any], config: dict[str, Any]
) -> tuple[dict[str, bool], float]:
    """Return (signal-flags, composite recency-weighted score).

    A score of 0.0 means no signal fired (not authoritative). Higher is more
    authoritative; recency lifts equal-evidence recent papers.

    Whitelist selection: an explicit `venue_allowlist` / `institution_whitelist`
    in `config` always wins; otherwise the GENERAL set is used, plus the
    AD/robotics extra when `is_ad_domain` is true. `is_ad_domain` defaults to
    True when absent, so a discovery config that does not carry it keeps the
    historical (general + AD) behaviour.
    """
    current_year = config.get("current_year", 2026)
    is_ad_domain = config.get("is_ad_domain", True)
    if "venue_allowlist" in config:
        venues = tuple(config["venue_allowlist"])
    else:
        venues = DEFAULT_VENUE_ALLOWLIST if is_ad_domain else GENERAL_VENUE_ALLOWLIST
    if "institution_whitelist" in config:
        institutions_wl = tuple(config["institution_whitelist"])
    else:
        institutions_wl = (
            DEFAULT_INSTITUTION_WHITELIST if is_ad_domain else GENERAL_INSTITUTION_WHITELIST
        )

    cites = candidate.get("cited_by_count") or 0
    year = candidate.get("year")
    velocity = _velocity(cites, year, current_year)
    stars = candidate.get("github_stars") or 0
    upvotes = candidate.get("upvotes") or 0

    s1 = cites >= _S1_CITE_FLOOR or velocity >= _S1_VELOCITY_FLOOR
    s2 = _matches(candidate.get("venue"), venues)
    s3 = any(_matches(inst, institutions_wl) for inst in candidate.get("institutions") or [])
    s4 = stars >= _S4_STARS_FLOOR or upvotes >= _S4_UPVOTES_FLOOR

    signals = {"s1_cite": s1, "s2_venue": s2, "s3_institution": s3, "s4_heat": s4}
    if not any(signals.values()):
        return signals, 0.0

    # Composite: each signal contributes evidence; citation velocity adds a
    # continuous component so fast risers outrank stale equal-cite papers.
    score = 0.0
    score += 3.0 if s1 else 0.0
    score += 2.5 if s2 else 0.0
    score += 2.0 if s3 else 0.0
    score += 1.5 if s4 else 0.0
    score += min(velocity / 100.0, 3.0)  # velocity bonus, capped

    # Recency weighting: newer papers get a multiplicative lift so the latest
    # authoritative work is not buried under classics (ADR-0001 "新论文配额").
    if year:
        recency = 1.0 + max(0, year - (current_year - 5)) * 0.05
        score *= recency
    return signals, round(score, 4)
