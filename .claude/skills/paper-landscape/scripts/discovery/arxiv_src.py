"""arXiv discovery source (category-restricted).

Net-new (CC-BY-NC repo). Queries the arXiv Atom feed restricted to the domain categories
(D-发现-3): cs.CV / cs.RO / cs.LG / cs.AI / eess.IV. Returns Atom XML, so a
raw-text getter is injected (not the JSON ThrottledClient). Parses the base
arxiv_id + version from the entry id (LS geodesic: identity = base id,
idempotency = id@version).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from typing import Any

ARXIV_CATEGORIES = ("cs.CV", "cs.RO", "cs.LG", "cs.AI", "eess.IV")
_BASE = "http://export.arxiv.org/api/query"
_NS = "{http://www.w3.org/2005/Atom}"
_ID_RE = re.compile(r"abs/(?P<id>\d{4}\.\d{4,5})(?P<ver>v\d+)?")


class ArxivSource:
    """arXiv Atom-feed source. Shares an arXiv-paced text client (3s interval)."""

    def __init__(self, text_client: Any) -> None:
        self._client = text_client

    def search(self, topic: str, max_results: int = 50) -> Iterator[dict[str, Any]]:
        """Yield candidates for *topic* within the allowed categories."""
        cat_clause = "+OR+".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
        search_query = f"all:{topic}+AND+%28{cat_clause}%29"
        query = {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": str(max_results),
        }
        xml_text = self._client.get_text(_BASE, query)
        root = ET.fromstring(xml_text)  # noqa: S314 (arXiv-pinned, non-untrusted)
        emitted = 0
        for entry in root.findall(f"{_NS}entry"):
            if emitted >= max_results:
                return
            cand = self._to_candidate(entry)
            if cand is not None:
                yield cand
                emitted += 1

    @classmethod
    def _to_candidate(cls, entry: ET.Element) -> dict[str, Any] | None:
        id_node = entry.find(f"{_NS}id")
        if id_node is None or not id_node.text:
            return None
        m = _ID_RE.search(id_node.text)
        if not m:
            return None
        title_node = entry.find(f"{_NS}title")
        title = " ".join((title_node.text or "").split()) if title_node is not None else ""
        pub_node = entry.find(f"{_NS}published")
        year = None
        if pub_node is not None and pub_node.text and pub_node.text[:4].isdigit():
            year = int(pub_node.text[:4])
        summary_node = entry.find(f"{_NS}summary")
        abstract = " ".join((summary_node.text or "").split()) if summary_node is not None else ""
        return {
            "openalex_id": None,
            "arxiv_id": m.group("id"),
            "arxiv_version": m.group("ver"),
            "doi": None,
            "title": title,
            "year": year,
            "cited_by_count": 0,
            "influential_citation_count": None,
            "venue": None,
            "institutions": [],
            "github_repo": None,
            "github_stars": None,
            "oa_pdf_url": f"https://arxiv.org/pdf/{m.group('id')}",
            "abstract": abstract,
            "upvotes": None,
            "ai_keywords": [],
            "discovery_sources": ["arxiv"],
        }
