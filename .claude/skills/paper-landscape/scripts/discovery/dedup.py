"""Cross-source dedup + field merge (D-发现-7).

Net-new (CC-BY-NC repo). Dedup key priority: DOI -> arxiv_id@version -> normalized
title-similarity >= 0.70 (+year bonus). Merge takes best-of-each-source:
citations from OpenAlex, influence from S2, code from HF, venue from DBLP,
pdf from arXiv/OA. Identity vs idempotency: the *version* is part of the
dedup key so v1 and v2 stay distinct (revision triggers reprocess, Chunk 3).
"""

from __future__ import annotations

from typing import Any

from scripts.discovery._text import THRESHOLD, similarity

# Numeric fields keep the larger value on merge (more-cited / more-starred wins).
_MAX_FIELDS = ("cited_by_count", "influential_citation_count", "github_stars", "upvotes")
# Scalar fields take the first non-null value on merge.
_FIRST_FIELDS = (
    "openalex_id",
    "arxiv_id",
    "arxiv_version",
    "doi",
    "title",
    "year",
    "venue",
    "github_repo",
    "oa_pdf_url",
    "abstract",
)


def _doi_key(c: dict[str, Any]) -> str | None:
    doi = c.get("doi")
    return f"doi:{doi.lower()}" if doi else None


def _arxiv_key(c: dict[str, Any]) -> str | None:
    aid = c.get("arxiv_id")
    if not aid:
        return None
    ver = c.get("arxiv_version") or ""
    return f"arxiv:{aid}{ver}"


def merge_pair(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Merge two candidates judged to be the same paper (best-of-each-source)."""
    out = dict(a)
    for field in _FIRST_FIELDS:
        if not out.get(field):
            out[field] = b.get(field)
    for field in _MAX_FIELDS:
        out[field] = max(a.get(field) or 0, b.get(field) or 0)
    # union institutions, ai_keywords, discovery_sources (order-stable)
    for field in ("institutions", "ai_keywords", "discovery_sources"):
        merged = list(a.get(field) or [])
        for item in b.get(field) or []:
            if item not in merged:
                merged.append(item)
        out[field] = merged
    return out


def dedup_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse duplicate candidates across sources into one record each.

    Two passes: (1) exact-key folding on DOI then arxiv_id@version; (2) a
    title-similarity consolidation over ALL survivors + keyless records that
    merges same-paper records exact-key folding missed — notably a DOI-only
    record (OpenAlex) and an arXiv-only record (arXiv/HF) of the same paper,
    which carry DIFFERENT key types and so never collide in pass 1 (Codex R21).
    Two survivors are merged only when their titles match AND they share no
    CONFLICTING hard identifier (same-typed but different DOI / arxiv id ⇒ kept
    apart, since those are genuinely different papers or versions).
    """
    by_key: dict[str, dict[str, Any]] = {}
    no_key: list[dict[str, Any]] = []

    for cand in candidates:
        key = _doi_key(cand) or _arxiv_key(cand)
        if key is None:
            no_key.append(cand)
        elif key in by_key:
            by_key[key] = merge_pair(by_key[key], cand)
        else:
            by_key[key] = dict(cand)

    # Title-similarity consolidation over the keyed survivors + keyless records.
    consolidated: list[dict[str, Any]] = []
    for cand in list(by_key.values()) + no_key:
        match = None
        for existing in consolidated:
            if _keys_compatible(cand, existing) and _titles_match(cand, existing):
                match = existing
                break
        if match is not None:
            consolidated[consolidated.index(match)] = merge_pair(match, cand)
        else:
            consolidated.append(dict(cand))

    return consolidated


def _keys_compatible(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """True unless a and b carry a CONFLICTING hard identifier of the same type.

    A DOI-only record and an arXiv-only record can be the same paper (compatible);
    two different DOIs — or two different arxiv ids INCLUDING version — cannot, so
    they are never title-merged. Comparing the versioned arxiv id preserves the
    v1≠v2 distinctness the dedup key relies on (a revision must stay separate).
    """
    ad, bd = (a.get("doi") or "").lower(), (b.get("doi") or "").lower()
    if ad and bd and ad != bd:
        return False
    aa = (a.get("arxiv_id") or "") + (a.get("arxiv_version") or "")
    ba = (b.get("arxiv_id") or "") + (b.get("arxiv_version") or "")
    return not (aa and ba and aa != ba)


def _titles_match(a: dict[str, Any], b: dict[str, Any]) -> bool:
    sim = similarity(a.get("title") or "", b.get("title") or "")
    bonus = 0.05 if (a.get("year") and a.get("year") == b.get("year")) else 0.0
    return (sim + bonus) >= THRESHOLD
