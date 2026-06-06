"""arXiv category-restricted feed + DBLP venue-authority source."""

from __future__ import annotations

from scripts.discovery.arxiv_src import ARXIV_CATEGORIES, ArxivSource
from scripts.discovery.dblp import DblpSource

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2601.01234v2</id>
    <title>End to End Driving</title>
    <published>2026-01-09T00:00:00Z</published>
    <summary>We drive.</summary>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2601.05678v1</id>
    <title>Vision Transformers</title>
    <published>2026-01-10T00:00:00Z</published>
    <summary>We see.</summary>
  </entry>
</feed>
"""


class StubText:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def get_text(self, url, query=None):
        self.calls.append((url, dict(query or {})))
        return self.payloads.pop(0)


def test_arxiv_category_filter_in_query():
    client = StubText([ATOM])
    src = ArxivSource(client)
    list(src.search("driving", max_results=10))
    _url, q = client.calls[0]
    for cat in ARXIV_CATEGORIES:
        assert cat in q["search_query"]
    assert "driving" in q["search_query"]


def test_arxiv_parses_id_version_year():
    client = StubText([ATOM])
    src = ArxivSource(client)
    out = list(src.search("driving", max_results=10))
    assert out[0]["arxiv_id"] == "2601.01234"
    assert out[0]["arxiv_version"] == "v2"
    assert out[0]["year"] == 2026
    assert out[0]["title"] == "End to End Driving"
    assert out[0]["discovery_sources"] == ["arxiv"]


def test_arxiv_stops_at_max_results():
    client = StubText([ATOM])
    src = ArxivSource(client)
    assert len(list(src.search("driving", max_results=1))) == 1


DBLP_JSON = {
    "result": {
        "hits": {
            "hit": [
                {"info": {"title": "End-to-End Driving.", "venue": "CVPR", "year": "2026"}},
                {"info": {"title": "Some Workshop Paper", "venue": "CoRR", "year": "2026"}},
            ]
        }
    }
}


class StubJson:
    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def get_json(self, url, query=None):
        self.calls.append((url, dict(query or {})))
        return self.pages.pop(0)


def test_dblp_query_and_venue_lookup():
    client = StubJson([DBLP_JSON])
    src = DblpSource(client)
    venue = src.venue_for_title("End to End Driving")
    assert venue == "CVPR"
    url, q = client.calls[0]
    assert url.endswith("/search/publ/api")
    assert q["format"] == "json"


def test_dblp_returns_none_when_no_title_match():
    client = StubJson([DBLP_JSON])
    src = DblpSource(client)
    assert src.venue_for_title("Completely Unrelated Title About Cooking") is None
