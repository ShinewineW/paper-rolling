"""OpenAlex discovery source.

Net-new (CC-BY-NC repo). Implements the OpenAlex /works recipe cited at
scientific-agent-skills paper-lookup/references/openalex.md (MIT recipe,
reusable + attributed):
  filter=default.search:{topic},cited_by_count:>{floor},from_publication_date:{date}
  sort=cited_by_count:desc & per_page=200 & cursor=* (deep pagination via
  meta.next_cursor; never page= which caps at 10k).

Per ADR-0001 there is NO citation hard gate here: `min_cites` only bounds the
page breadth for over-fetch; the multi-signal OR authority decision lives in
authority.py. default.search (not title.search) so authoritative papers whose
titles lack the domain phrase are still recalled.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

_BASE = "https://api.openalex.org/works"


def reconstruct_abstract(inverted_index: dict[str, list[int]] | None) -> str:
    """Rebuild abstract text from OpenAlex abstract_inverted_index {word:[pos]}."""
    if not inverted_index:
        return ""
    positions: dict[int, str] = {}
    for word, idxs in inverted_index.items():
        for idx in idxs:
            positions[idx] = word
    return " ".join(positions[i] for i in sorted(positions))


def _strip_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    return doi.replace("https://doi.org/", "").replace("http://doi.org/", "")


def _institutions(work: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for authorship in work.get("authorships", []):
        for inst in authorship.get("institutions", []):
            name = inst.get("display_name")
            if name and name not in names:
                names.append(name)
    return names


class OpenAlexSource:
    """OpenAlex /works source. Shares one ThrottledClient (HUB-owned)."""

    def __init__(self, client: Any, polite_email: str | None = None) -> None:
        self._client = client
        self._polite_email = polite_email

    def search(
        self,
        topic: str,
        from_date: str,
        min_cites: int = 0,
        max_results: int = 200,
        concept_id: str | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Yield candidate dicts for *topic* published on/after *from_date*.

        Args:
            topic: free-text query for default.search.
            from_date: ISO date (YYYY-MM-DD) lower bound.
            min_cites: page-breadth floor only (>min_cites-1 ==  >=min_cites);
                NOT an authority gate (ADR-0001).
            max_results: hard stop across all cursor pages.
            concept_id: optional OpenAlex topics/concepts id for anchoring.
        """
        filters = [
            f"default.search:{topic}",
            f"cited_by_count:>{min_cites - 1}",
            f"from_publication_date:{from_date}",
        ]
        if concept_id:
            filters.append(f"topics.id:{concept_id}")
        cursor = "*"
        emitted = 0
        while cursor is not None and emitted < max_results:
            query = {
                "filter": ",".join(filters),
                "sort": "cited_by_count:desc",
                "per_page": "200",
                "cursor": cursor,
            }
            if self._polite_email:
                query["mailto"] = self._polite_email
            page = self._client.get_json(_BASE, query)
            for work in page.get("results", []):
                if emitted >= max_results:
                    return
                yield self._to_candidate(work)
                emitted += 1
            cursor = page.get("meta", {}).get("next_cursor")

    @staticmethod
    def _to_candidate(work: dict[str, Any]) -> dict[str, Any]:
        oa = work.get("open_access") or {}
        return {
            "openalex_id": work.get("id"),
            "arxiv_id": None,
            "arxiv_version": None,
            "doi": _strip_doi(work.get("doi")),
            "title": work.get("title") or "",
            "year": work.get("publication_year"),
            "cited_by_count": work.get("cited_by_count", 0),
            "influential_citation_count": None,
            "venue": ((work.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "institutions": _institutions(work),
            "github_repo": None,
            "github_stars": None,
            "oa_pdf_url": oa.get("oa_url"),
            "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
            "upvotes": None,
            "ai_keywords": [],
            "authors": [
                a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])
            ],
            "discovery_sources": ["openalex"],
        }
