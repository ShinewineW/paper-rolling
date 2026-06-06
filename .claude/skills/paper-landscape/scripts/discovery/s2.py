"""Semantic Scholar discovery source.

Net-new (CC-BY-NC repo). Uses /paper/search/bulk (token pagination) anonymously
(D-发现-7: no S2 key; S2 only contributes the auxiliary influence signal).
Contributes influentialCitationCount (Tier-B influence tiebreaker), arXiv id
backfill, and OA pdf fallback.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

_BASE = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
_FIELDS = (
    "title,year,citationCount,influentialCitationCount,venue,authors,externalIds,openAccessPdf"
)


class S2Source:
    """Semantic Scholar bulk-search source. Shares one ThrottledClient."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def search(
        self, topic: str, from_year: str, max_results: int = 100
    ) -> Iterator[dict[str, Any]]:
        """Yield candidates for *topic* published in/after *from_year*."""
        token: str | None = None
        emitted = 0
        first = True
        while (first or token) and emitted < max_results:
            first = False
            query = {
                "query": topic,
                "publicationDateOrYear": f"{from_year}:",
                "fields": _FIELDS,
                "sort": "citationCount:desc",
            }
            if token:
                query["token"] = token
            page = self._client.get_json(_BASE, query)
            for paper in page.get("data", []) or []:
                if emitted >= max_results:
                    return
                yield self._to_candidate(paper)
                emitted += 1
            token = page.get("token")

    @staticmethod
    def _to_candidate(paper: dict[str, Any]) -> dict[str, Any]:
        ext = paper.get("externalIds") or {}
        oa = paper.get("openAccessPdf") or {}
        institutions: list[str] = []
        return {
            "openalex_id": None,
            "arxiv_id": ext.get("ArXiv"),
            "arxiv_version": None,
            "doi": ext.get("DOI"),
            "title": paper.get("title") or "",
            "year": paper.get("year"),
            "cited_by_count": paper.get("citationCount", 0),
            "influential_citation_count": paper.get("influentialCitationCount"),
            "venue": paper.get("venue"),
            "institutions": institutions,
            "github_repo": None,
            "github_stars": None,
            "oa_pdf_url": oa.get("url"),
            "abstract": "",
            "upvotes": None,
            "ai_keywords": [],
            "authors": [a.get("name", "") for a in (paper.get("authors") or [])],
            "discovery_sources": ["s2"],
        }
