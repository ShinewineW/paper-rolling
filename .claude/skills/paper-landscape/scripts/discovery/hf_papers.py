"""Hugging Face Papers discovery source.

Net-new (CC-BY-NC repo). Role = recall supplement + code enrichment (D-发现-3): pulls
githubRepo / githubStars / ai_keywords / upvotes — NOT a citation gate.
Returned arxiv_id is fed back through OpenAlex before entering the authority
set.

# ===========================================================================
# HF API TOKEN (D-发现-4). The shipped source carries a PLACEHOLDER, not a live
# token. Resolution: HF_TOKEN env var first (see .env.example), else the source
# constant. While it is the placeholder, requests go out ANONYMOUSLY (no
# Authorization header) — HF Papers search works anonymously at a lower rate.
# Replace the placeholder with a fine-grained READ-ONLY token (or set HF_TOKEN)
# to raise the rate; a real token committed here would land in git history.
# ===========================================================================
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

# ===========================================================================
# HF API TOKEN (D-发现-4) — see the module docstring. Default is a placeholder;
# real token via HF_TOKEN env (first) or by replacing the constant below. While
# it is the placeholder, no Authorization header is sent (anonymous access).
# ===========================================================================
_PLACEHOLDER_TOKEN = "hf_REPLACE_WITH_READONLY_TOKEN"
HF_READONLY_TOKEN = _PLACEHOLDER_TOKEN  # replace with a real read-only token, or set HF_TOKEN

# OpenAlex polite-pool email (non-secret, D-发现-2).
OPENALEX_POLITE_EMAIL = "ahhssxlcwjz@163.com"

_BASE = "https://huggingface.co/api/papers/search"


def _hf_token() -> str:
    """Resolve the HF token: the HF_TOKEN env var first (honoring .env.example),
    else the source constant (a placeholder by default)."""
    return os.environ.get("HF_TOKEN") or HF_READONLY_TOKEN


def _hf_headers() -> dict[str, str]:
    """Authorization header ONLY when a REAL token is present. While the token is
    the shipped placeholder, return {} so the request goes out anonymously — the
    placeholder must not be sent as a bearer (it would 401 instead of falling
    back to anonymous; Codex Round-23)."""
    token = _hf_token()
    if token and token != _PLACEHOLDER_TOKEN:
        return {"Authorization": f"Bearer {token}"}
    return {}


class HFPapersSource:
    """HF Papers search source. Injected client must accept a headers kwarg."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def search(self, topic: str, max_results: int = 50) -> Iterator[dict[str, Any]]:
        """Yield candidates for *topic* with code + heat enrichment."""
        results = self._client.get_json(_BASE, {"q": topic}, headers=_hf_headers())
        emitted = 0
        for item in results or []:
            if emitted >= max_results:
                return
            paper = item.get("paper") or item
            yield self._to_candidate(paper)
            emitted += 1

    @staticmethod
    def _to_candidate(paper: dict[str, Any]) -> dict[str, Any]:
        published = paper.get("publishedAt") or ""
        year = int(published[:4]) if published[:4].isdigit() else None
        return {
            "openalex_id": None,
            "arxiv_id": paper.get("id"),
            "arxiv_version": None,
            "doi": None,
            "title": paper.get("title") or "",
            "year": year,
            "cited_by_count": 0,
            "influential_citation_count": None,
            "venue": None,
            "institutions": [],
            "github_repo": paper.get("githubRepo"),
            "github_stars": paper.get("githubStars"),
            "oa_pdf_url": None,
            "abstract": "",
            "upvotes": paper.get("upvotes"),
            "ai_keywords": paper.get("ai_keywords") or [],
            "discovery_sources": ["hf_papers"],
        }
