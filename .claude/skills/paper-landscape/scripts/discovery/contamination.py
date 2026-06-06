"""Preprint / unreviewed trust flag (吸收-D2).

Net-new paper-rolling module (own signals: explicit preprint venue, arxiv_id
with no reviewed venue, or an OA-pdf URL on a preprint host). NON-BLOCKING:
annotates trust level only; preprint_policy decides corpus entry. The
PREPRINT_VENUES 10-venue list is shared factual data (also appears in ARS
contamination_signals.py); the matching logic here is our own — ARS's
compute_preprint_signal has different semantics (year>=2024 + source_pointer).
"""

from __future__ import annotations

from typing import Any

PREPRINT_VENUES = frozenset(
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

_PREPRINT_URL_HINTS = (
    "arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "ssrn.com",
    "researchsquare.com",
    "preprints.org",
    "chemrxiv.org",
    "eartharxiv.org",
    "osf.io/preprints",
    "techrxiv.org",
)


def preprint_flag(candidate: dict[str, Any]) -> bool:
    """Return True iff the candidate looks like an unreviewed preprint.

    Signals (any one suffices): explicit preprint venue; an arxiv_id with no
    reviewed venue; an OA pdf URL hosted on a known preprint server.
    """
    venue = candidate.get("venue")
    if venue in PREPRINT_VENUES:
        return True
    if isinstance(venue, str) and venue:
        return False  # a non-empty, non-preprint venue means reviewed
    if candidate.get("arxiv_id"):
        return True
    oa_url = (candidate.get("oa_pdf_url") or "").lower()
    return any(hint in oa_url for hint in _PREPRINT_URL_HINTS)
