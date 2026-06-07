"""Hugging Face Papers discovery source.

Net-new (CC-BY-NC repo). Role = recall supplement + code enrichment (D-发现-3): pulls
githubRepo / githubStars / ai_keywords / upvotes — NOT a citation gate.
Returned arxiv_id is fed back through OpenAlex before entering the authority
set.

# ===========================================================================
# HF API TOKEN (D-发现-4). The shipped source HARDCODES a fine-grained READ-ONLY
# Hugging Face token — an explicit, owner-granted exemption to the security.md
# "no hardcoded secrets" rule, for self-contained distribution. Scope is
# READ-ONLY (blast radius = public-metadata reads); it lands in git history by
# design. Resolution: HF_TOKEN env var first (override without editing source),
# else this constant. If the constant is ever reset to the placeholder sentinel,
# requests go out ANONYMOUSLY (no Authorization header) — HF search still works
# at a lower rate. Rotate at huggingface.co if exposed beyond this repo's audience.
# ===========================================================================
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

# ===========================================================================
# HF API TOKEN (D-发现-4) — see the module docstring. Hardcoded READ-ONLY token
# (owner-granted exemption); HF_TOKEN env overrides without editing source. If
# reset to the placeholder sentinel, no Authorization header is sent (anonymous).
# ===========================================================================
_PLACEHOLDER_TOKEN = "hf_REPLACE_WITH_READONLY_TOKEN"  # sentinel: "unconfigured" -> anonymous
HF_READONLY_TOKEN = (
    "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"  # owner-forced READ-ONLY hardcode (D-发现-4)
)

# OpenAlex polite-pool email (non-secret, D-发现-2).
OPENALEX_POLITE_EMAIL = "ahhssxlcwjz@163.com"

_BASE = "https://huggingface.co/api/papers/search"


def _hf_token() -> str:
    """Resolve the HF token: the HF_TOKEN env var first (override without editing
    source), else the hardcoded read-only constant."""
    return os.environ.get("HF_TOKEN") or HF_READONLY_TOKEN


def _hf_headers() -> dict[str, str]:
    """Authorization header when a real token is present (the hardcoded constant
    or an HF_TOKEN override). If the token is the placeholder sentinel, return {}
    so the request goes out anonymously — the placeholder must never be sent as a
    bearer (it would 401 instead of falling back to anonymous)."""
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
