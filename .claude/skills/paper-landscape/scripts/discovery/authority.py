"""Multi-signal OR authority scorer (ADR-0001).

Net-new (CC-BY-NC repo). The discovery layer has NO citation hard floor (ADR-0001 supersedes
the old >=500 gate). A candidate is authoritative if it fires ANY of four
signals; a composite, recency-weighted score then orders the survivors:

  S1 cite      : high cited_by_count OR strong citation velocity (cites/age)
  S2 venue     : title's venue matches a top-venue allowlist (DBLP-confirmed)
  S3 institution: an authorship institution matches the org whitelist
  S4 heat      : GitHub stars + HF upvotes + recency (the search-index proxy)

Whitelists default to the D-发现-5 initial lists; campaign config can override.
"""

from __future__ import annotations

from typing import Any

# D-发现-5 initial top-venue allowlist (matched case-insensitively as substrings).
DEFAULT_VENUE_ALLOWLIST = (
    "NeurIPS",
    "ICML",
    "ICLR",
    "CVPR",
    "ICCV",
    "ECCV",
    "AAAI",
    "ICRA",
    "IROS",
    "CoRL",
    "RSS",
    "TPAMI",
    "IJCV",
    "RA-L",
    "T-RO",
)

# D-发现-5 initial institution whitelist (matched case-insensitively as substrings).
DEFAULT_INSTITUTION_WHITELIST = (
    "Google",
    "DeepMind",
    "Meta",
    "FAIR",
    "NVIDIA",
    "Microsoft Research",
    "OpenAI",
    "Apple",
    "Amazon",
    "Waymo",
    "Tesla",
    "Wayve",
    "Cruise",
    "Nuro",
    "Toyota Research",
    "TRI",
    "Boston Dynamics",
    "AI2",
    "SenseTime",
    "Megvii",
    "Apollo",
    "Noah",
    "Horizon",
    "DAMO",
    "Tencent AI Lab",
    "ByteDance",
    "Momenta",
    "Pony.ai",
    "Unitree",
)

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
    """
    current_year = config.get("current_year", 2026)
    venues = tuple(config.get("venue_allowlist", DEFAULT_VENUE_ALLOWLIST))
    institutions_wl = tuple(config.get("institution_whitelist", DEFAULT_INSTITUTION_WHITELIST))

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
