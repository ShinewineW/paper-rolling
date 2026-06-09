"""HF Papers source: search recipe, candidate mapping, .env token contract."""

from __future__ import annotations

from scripts.discovery import hf_papers
from scripts.discovery.hf_papers import HFPapersSource


class StubClient:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def get_json(self, url, query=None, headers=None):
        self.calls.append((url, dict(query or {}), dict(headers or {})))
        return self.payloads.pop(0)


HF_RESULTS = [
    {
        "paper": {
            "id": "2601.01234",
            "title": "DiffusionDrive",
            "githubRepo": "https://github.com/x/diffusiondrive",
            "githubStars": 512,
            "ai_keywords": ["diffusion", "planning"],
            "upvotes": 88,
            "publishedAt": "2026-01-09T00:00:00.000Z",
        }
    }
]


def test_search_sends_bearer_from_env_token(monkeypatch):
    # HF_TOKEN in the gitignored .env (surfaced into os.environ) is sent as the
    # bearer (D-发现-4). The search recipe (endpoint + query) is unchanged.
    monkeypatch.setenv("HF_TOKEN", "hf_env_token_abc")
    client = StubClient([HF_RESULTS])
    src = HFPapersSource(client)
    list(src.search("end-to-end driving", max_results=10))
    url, q, headers = client.calls[0]
    assert url.endswith("/api/papers/search")
    assert q["q"] == "end-to-end driving"
    assert headers.get("Authorization") == "Bearer hf_env_token_abc"


def test_search_is_anonymous_when_env_token_unset(monkeypatch):
    # No HF_TOKEN set -> the request goes out ANONYMOUSLY (no Authorization
    # header). Nothing is hardcoded, so there is no token to fall back to.
    monkeypatch.delenv("HF_TOKEN", raising=False)
    client = StubClient([HF_RESULTS])
    src = HFPapersSource(client)
    list(src.search("q", max_results=10))
    _url, _q, headers = client.calls[0]
    assert "Authorization" not in headers


def test_candidate_extracts_github_keywords_upvotes():
    client = StubClient([HF_RESULTS])
    src = HFPapersSource(client)
    cand = next(iter(src.search("q", max_results=10)))
    assert cand["arxiv_id"] == "2601.01234"
    assert cand["github_repo"] == "https://github.com/x/diffusiondrive"
    assert cand["github_stars"] == 512
    assert cand["ai_keywords"] == ["diffusion", "planning"]
    assert cand["upvotes"] == 88
    assert cand["year"] == 2026
    assert cand["discovery_sources"] == ["hf_papers"]


def test_source_documents_env_token_and_anonymous_fallback():
    import inspect

    src_text = inspect.getsource(hf_papers).lower()
    assert ".env" in src_text  # the token is read from the gitignored .env
    assert "read-only" in src_text  # the token's scope
    assert "anonymous" in src_text  # unset HF_TOKEN -> anonymous
