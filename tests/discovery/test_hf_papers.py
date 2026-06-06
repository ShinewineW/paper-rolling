"""HF Papers source: search recipe, candidate mapping, token constant present."""

from __future__ import annotations

from scripts.discovery import hf_papers
from scripts.discovery.hf_papers import HF_READONLY_TOKEN, HFPapersSource


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


def test_token_constant_is_readonly_labeled():
    # The token is a hard-coded read-only constant (D-发现-4). It must exist
    # and be a non-empty string; the source file carries the user-forced
    # read-only-scope label.
    assert isinstance(HF_READONLY_TOKEN, str)
    assert HF_READONLY_TOKEN  # non-empty


def test_search_uses_q_param_and_auth_header(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)  # pin the hardcoded fallback path
    client = StubClient([HF_RESULTS])
    src = HFPapersSource(client)
    list(src.search("end-to-end driving", max_results=10))
    url, q, headers = client.calls[0]
    assert url.endswith("/api/papers/search")
    assert q["q"] == "end-to-end driving"
    assert headers.get("Authorization") == f"Bearer {HF_READONLY_TOKEN}"


def test_search_prefers_env_token_over_hardcoded(monkeypatch):
    # Codex R17: .env.example promises an HF_TOKEN override — the code must
    # actually read it (env first, hardcoded constant as fallback).
    monkeypatch.setenv("HF_TOKEN", "hf_env_override_xyz")
    client = StubClient([HF_RESULTS])
    src = HFPapersSource(client)
    list(src.search("q", max_results=10))
    _url, _q, headers = client.calls[0]
    assert headers.get("Authorization") == "Bearer hf_env_override_xyz"


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


def test_source_constant_file_labels_token_readonly():
    import inspect

    src_text = inspect.getsource(hf_papers)
    assert "read-only" in src_text.lower()
    assert "user-forced" in src_text.lower()
