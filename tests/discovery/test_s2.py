"""Semantic Scholar source: /paper/search/bulk recipe + candidate mapping."""

from __future__ import annotations

from scripts.discovery.s2 import S2Source


class StubClient:
    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def get_json(self, url, query=None):
        self.calls.append((url, dict(query or {})))
        return self.pages.pop(0)


def _paper(**kw):
    base = {
        "title": "DiffusionDrive",
        "year": 2026,
        "citationCount": 12,
        "influentialCitationCount": 3,
        "venue": "CVPR",
        "externalIds": {"ArXiv": "2601.01234", "DOI": "10.1/dd"},
        "openAccessPdf": {"url": "https://example.org/dd.pdf"},
    }
    base.update(kw)
    return base


def test_bulk_query_recipe():
    client = StubClient([{"data": [_paper()], "token": None}])
    src = S2Source(client)
    list(src.search("end-to-end driving", from_year="2024", max_results=100))
    url, q = client.calls[0]
    assert url.endswith("/paper/search/bulk")
    assert q["query"] == "end-to-end driving"
    assert q["publicationDateOrYear"] == "2024:"
    assert "influentialCitationCount" in q["fields"]
    assert q["sort"] == "citationCount:desc"


def test_token_pagination():
    p1 = {"data": [_paper(title="A")], "token": "TOK2"}
    p2 = {"data": [_paper(title="B")], "token": None}
    client = StubClient([p1, p2])
    src = S2Source(client)
    out = list(src.search("q", from_year="2024", max_results=100))
    assert [c["title"] for c in out] == ["A", "B"]
    assert client.calls[1][1]["token"] == "TOK2"


def test_candidate_extracts_arxiv_doi_influence_pdf():
    client = StubClient([{"data": [_paper()], "token": None}])
    src = S2Source(client)
    cand = next(iter(src.search("q", from_year="2024", max_results=100)))
    assert cand["arxiv_id"] == "2601.01234"
    assert cand["doi"] == "10.1/dd"
    assert cand["influential_citation_count"] == 3
    assert cand["cited_by_count"] == 12
    assert cand["venue"] == "CVPR"
    assert cand["oa_pdf_url"] == "https://example.org/dd.pdf"
    assert cand["discovery_sources"] == ["s2"]


def test_stops_at_max_results():
    page = {"data": [_paper(title=f"P{i}") for i in range(5)], "token": "MORE"}
    client = StubClient([page])
    src = S2Source(client)
    assert len(list(src.search("q", from_year="2024", max_results=2))) == 2
