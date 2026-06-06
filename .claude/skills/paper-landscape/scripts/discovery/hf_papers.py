"""Hugging Face Papers discovery source.

Net-new (CC-BY-NC repo). Role = recall supplement + code enrichment (D-发现-3): pulls
githubRepo / githubStars / ai_keywords / upvotes — NOT a citation gate.
Returned arxiv_id is fed back through OpenAlex before entering the authority
set.

# ===========================================================================
# HF API TOKEN — user-forced hardcode, READ-ONLY scope (D-发现-4).
# User granted an explicit exemption to security.md secrets MUST after being
# warned twice that git sync pushes this into GitHub history. The token is a
# fine-grained READ-ONLY credential; leak blast radius = public-metadata read.
# Single source of truth; never logged, never duplicated. Replace at deploy.
# ===========================================================================
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

# ===========================================================================
# HF API TOKEN — user-forced hardcode, READ-ONLY scope (D-发现-4).
# User granted an explicit exemption to security.md secrets MUST after being
# warned twice that git sync pushes this into GitHub history. The token is a
# fine-grained READ-ONLY credential; leak blast radius = public-metadata read.
# Single source of truth; never logged, never duplicated. Replace at deploy, OR
# set HF_TOKEN in the environment (read FIRST — see .env.example).
# ===========================================================================
HF_READONLY_TOKEN = "hf_REPLACE_WITH_READONLY_TOKEN"  # user-forced fallback, read-only scope

# OpenAlex polite-pool email (non-secret, D-发现-2).
OPENALEX_POLITE_EMAIL = "ahhssxlcwjz@163.com"

_BASE = "https://huggingface.co/api/papers/search"


def _hf_token() -> str:
    """Resolve the HF token: the HF_TOKEN env var first (honoring .env.example),
    the hardcoded read-only constant as the self-contained fallback. Codex R17:
    the code now actually reads the env override the docs promised."""
    return os.environ.get("HF_TOKEN") or HF_READONLY_TOKEN


class HFPapersSource:
    """HF Papers search source. Injected client must accept a headers kwarg."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def search(self, topic: str, max_results: int = 50) -> Iterator[dict[str, Any]]:
        """Yield candidates for *topic* with code + heat enrichment."""
        headers = {"Authorization": f"Bearer {_hf_token()}"}
        results = self._client.get_json(_BASE, {"q": topic}, headers=headers)
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
