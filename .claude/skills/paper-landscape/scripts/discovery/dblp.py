"""DBLP venue-authority source.

Net-new (CC-BY-NC repo). DBLP gives canonical venue metadata (no citations, no abstract):
used purely to confirm a paper appeared at a top venue (D-发现-3, signal S2).
Title-matched against the discovered title via the shared 0.70 similarity.
"""

from __future__ import annotations

from typing import Any

from scripts.discovery._text import THRESHOLD, similarity

_BASE = "https://dblp.org/search/publ/api"


class DblpSource:
    """DBLP publ search. Shares one ThrottledClient (polite pacing)."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def venue_for_title(self, title: str) -> str | None:
        """Return the DBLP venue for the best title match, or None.

        Picks the hit whose title clears the 0.70 similarity bar with the
        highest score.
        """
        page = self._client.get_json(_BASE, {"q": title, "format": "json", "h": "10"})
        hits = (((page.get("result") or {}).get("hits") or {}).get("hit")) or []
        best_venue: str | None = None
        best_score = THRESHOLD
        for hit in hits:
            info = hit.get("info") or {}
            cand_title = info.get("title") or ""
            score = similarity(cand_title, title)
            if score >= best_score:
                best_score = score
                best_venue = info.get("venue")
        return best_venue
