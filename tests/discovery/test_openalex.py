"""OpenAlex source: URL recipe, cursor paging, abstract reconstruction, OA pdf."""

from __future__ import annotations

from scripts.discovery.openalex import OpenAlexSource, reconstruct_abstract


class StubClient:
    """Records query dicts; returns queued JSON pages."""

    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def get_json(self, url, query=None):
        self.calls.append((url, dict(query or {})))
        return self.pages.pop(0)


def _work(**kw):
    base = {
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1/x",
        "title": "Attention Is All You Need",
        "publication_year": 2017,
        "cited_by_count": 134000,
        "open_access": {"is_oa": True, "oa_url": "https://example.org/a.pdf"},
        "authorships": [
            {"institutions": [{"display_name": "Google"}]},
        ],
        "abstract_inverted_index": {"We": [0], "propose": [1]},
    }
    base.update(kw)
    return base


def test_reconstruct_abstract_orders_by_position():
    inv = {"all": [3], "you": [4], "Attention": [0], "is": [1], "need": [5], "All": [2]}
    assert reconstruct_abstract(inv) == "Attention is All all you need"


def test_reconstruct_abstract_handles_none():
    assert reconstruct_abstract(None) == ""


def test_query_uses_default_search_filter_sort_cursor():
    client = StubClient([{"results": [_work()], "meta": {"next_cursor": None}}])
    src = OpenAlexSource(client, polite_email="x@y.z")
    list(src.search("transformer", from_date="2015-01-01", min_cites=0, max_results=200))
    _url, q = client.calls[0]
    flt = q["filter"]
    assert "default.search:transformer" in flt
    assert "from_publication_date:2015-01-01" in flt
    assert "cited_by_count:>-1" in flt  # min_cites=0 -> operator floor min_cites-1
    assert q["sort"] == "cited_by_count:desc"
    assert q["cursor"] == "*"
    assert q["per_page"] == "200"
    assert q["mailto"] == "x@y.z"


def test_cursor_pagination_follows_next_cursor():
    page1 = {"results": [_work(id="W1")], "meta": {"next_cursor": "CUR2"}}
    page2 = {"results": [_work(id="W2")], "meta": {"next_cursor": None}}
    client = StubClient([page1, page2])
    src = OpenAlexSource(client)
    out = list(src.search("t", from_date="2015-01-01", min_cites=0, max_results=200))
    assert len(out) == 2
    assert client.calls[0][1]["cursor"] == "*"
    assert client.calls[1][1]["cursor"] == "CUR2"


def test_search_stops_at_max_results():
    page = {
        "results": [_work(id=f"W{i}") for i in range(5)],
        "meta": {"next_cursor": "MORE"},
    }
    client = StubClient([page])
    src = OpenAlexSource(client)
    out = list(src.search("t", from_date="2015-01-01", min_cites=0, max_results=3))
    assert len(out) == 3


def test_candidate_shape_includes_required_fields():
    client = StubClient([{"results": [_work()], "meta": {"next_cursor": None}}])
    src = OpenAlexSource(client)
    cand = next(iter(src.search("t", from_date="2015-01-01", min_cites=0, max_results=200)))
    assert cand["doi"] == "10.1/x"  # https prefix stripped
    assert cand["cited_by_count"] == 134000
    assert cand["year"] == 2017
    assert cand["oa_pdf_url"] == "https://example.org/a.pdf"
    assert cand["institutions"] == ["Google"]
    assert cand["abstract"].startswith("We propose")
    assert cand["discovery_sources"] == ["openalex"]
