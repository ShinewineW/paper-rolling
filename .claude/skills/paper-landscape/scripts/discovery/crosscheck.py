"""DOI cross-check (NET-NEW; Round 5 F1 — ARS has no crosscheck.py).

Our own small module implementing the documented DOI-with-title contract: a
DOI-keyed lookup is accepted only when the returned title clears the 0.70 bar
(via the vendored `_text.similarity`); otherwise it is a DOI_MISMATCH and
rejected. Not vendored, not parity-tested (the parity subsystem was deleted).
"""

from __future__ import annotations

from typing import Any

from scripts.discovery._text import THRESHOLD, similarity


def doi_title_crosscheck(
    doi: str, fetched_title: str, expected_title: str
) -> dict[str, Any] | None:
    """Return a minimal match record iff the fetched title matches, else None.

    Args:
        doi: the DOI that was looked up (echoed into the match record).
        fetched_title: the title returned by the resolver for that DOI.
        expected_title: the title we expected (from the originating source).

    Returns:
        {"doi", "title", "similarity"} when the title clears 0.70; None on
        DOI_MISMATCH.
    """
    sim = similarity(fetched_title, expected_title)
    if sim >= THRESHOLD:
        return {"doi": doi, "title": fetched_title, "similarity": sim}
    return None
