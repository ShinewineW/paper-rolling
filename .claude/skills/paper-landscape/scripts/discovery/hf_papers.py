"""Hugging Face Papers discovery source.

Net-new (CC-BY-NC repo). Role = recall supplement + code enrichment (D-发现-3): pulls
githubRepo / githubStars / ai_keywords / upvotes — NOT a citation gate.
Returned arxiv_id is fed back through OpenAlex before entering the authority
set.

# ===========================================================================
# HF API TOKEN (D-发现-4). The READ-ONLY token is read solely from the gitignored
# ``.env`` (``HF_TOKEN``), surfaced into os.environ by ``llm.load_dotenv`` at
# composition time. NOTHING is hardcoded — an earlier shipped constant was auto-revoked by
# Hugging Face the moment it hit public git history, so the secret now lives only
# in ``.env`` (security.md compliant). Unset ``HF_TOKEN`` -> requests go out
# ANONYMOUSLY (no Authorization header); HF search still works at a lower rate.
# ===========================================================================
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

# OpenAlex polite-pool email (non-secret, D-发现-2).
OPENALEX_POLITE_EMAIL = "ahhssxlcwjz@163.com"

_BASE = "https://huggingface.co/api/papers/search"


def _hf_token() -> str | None:
    """Read the HF token from the gitignored .env (HF_TOKEN); None -> anonymous."""
    return os.environ.get("HF_TOKEN") or None


def _hf_headers() -> dict[str, str]:
    """Authorization header when HF_TOKEN is set; otherwise {} (anonymous)."""
    token = _hf_token()
    return {"Authorization": f"Bearer {token}"} if token else {}


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
