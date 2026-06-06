"""Discovery orchestration — the HUB-facing entry point.

Net-new (CC-BY-NC repo). discover(campaign_config) drives the full discovery slice:
  1. LLM query expansion (D-发现-6) + HF ai_keyword second round.
  2. Fan the shared (HUB-owned, serial) source clients across sources.
  3. Cross-source dedup (D-发现-7).
  4. Multi-signal OR authority scoring (ADR-0001) — drop non-authoritative.
  5. Preprint trust flag (吸收-D2).
  6. Rank by authority score, over-fetch 2-3x top_k for backfill (中枢-D2:
     N = SUCCESSFULLY processed, so discovery must supply spares).

Sources are injected (dict of source objects exposing .search(...)) so the
orchestration is unit-testable without network; production wiring builds the
real sources over shared ThrottledClients in Chunk 5 (the SKILL entry).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from scripts.discovery.authority import score_authority
from scripts.discovery.contamination import preprint_flag
from scripts.discovery.dedup import dedup_candidates
from scripts.discovery.query_expand import expand_queries

# Public interface field set — every returned candidate carries exactly these.
_INTERFACE_FIELDS = (
    "arxiv_id",
    "arxiv_version",
    "doi",
    "title",
    "authors",
    "year",
    "cited_by_count",
    "influential_citation_count",
    "venue",
    "institutions",
    "github_repo",
    "github_stars",
    "oa_pdf_url",
    "authority_signals",
    "authority_score",
    "preprint_flag",
    "discovery_sources",
)


def discover(
    campaign_config: dict[str, Any],
    sources: dict[str, Any],
    llm: Callable[[str], list[str]],
) -> list[dict[str, Any]]:
    """Discover ranked authoritative candidates for a campaign.

    Args:
        campaign_config: campaign params; reads topic, top_k, from_date,
            from_year, current_year, overfetch_factor (default 3),
            venue_allowlist / institution_whitelist (optional overrides).
        sources: dict mapping source name -> source object with .search().
            Expected keys: openalex, s2, arxiv, dblp, hf_papers.
        llm: query-expansion callable (prompt -> list[str]).

    Returns:
        Authoritative candidates, sorted by authority_score descending,
        capped at top_k * overfetch_factor for backfill headroom.
    """
    topic = campaign_config["topic"]
    top_k = campaign_config["top_k"]
    overfetch = campaign_config.get("overfetch_factor", 3)
    cap = top_k * overfetch

    queries = expand_queries(topic, llm=llm)

    raw: list[dict[str, Any]] = []
    raw.extend(_run_openalex(sources.get("openalex"), queries, campaign_config))
    raw.extend(_run_s2(sources.get("s2"), queries, campaign_config))
    raw.extend(_run_arxiv(sources.get("arxiv"), queries, campaign_config))
    raw.extend(_run_hf(sources.get("hf_papers"), queries, campaign_config))

    # second-round expansion from any HF ai_keywords harvested above
    harvested_keywords: list[str] = []
    for c in raw:
        harvested_keywords.extend(c.get("ai_keywords") or [])
    if harvested_keywords:
        extra_queries = [
            q
            for q in expand_queries(topic, llm=llm, ai_keywords=harvested_keywords)
            if q not in queries
        ]
        raw.extend(_run_openalex(sources.get("openalex"), extra_queries, campaign_config))

    merged = dedup_candidates(raw)

    scored: list[dict[str, Any]] = []
    for cand in merged:
        signals, score = score_authority(cand, campaign_config)
        if not any(signals.values()):
            continue  # ADR-0001: no signal fired -> not authoritative
        cand = dict(cand)
        cand["authority_signals"] = signals
        cand["authority_score"] = score
        cand["preprint_flag"] = preprint_flag(cand)
        scored.append(_project(cand))

    scored.sort(key=lambda c: c["authority_score"], reverse=True)
    return scored[:cap]


def _project(cand: dict[str, Any]) -> dict[str, Any]:
    """Reduce a scored candidate to exactly the public interface fields.

    `authors` is normalized to a list so downstream `candidate["authors"]` is
    always safe even for sources that don't supply it (Round 15 #1).
    """
    out = {field: cand.get(field) for field in _INTERFACE_FIELDS}
    out["authors"] = out.get("authors") or []
    return out


def _run_openalex(source, queries, cfg) -> list[dict[str, Any]]:
    if source is None:
        return []
    out: list[dict[str, Any]] = []
    for q in queries:
        out.extend(
            source.search(
                q,
                from_date=cfg["from_date"],
                min_cites=0,
                max_results=cfg.get("openalex_page", 200),
            )
        )
    return out


def _run_s2(source, queries, cfg) -> list[dict[str, Any]]:
    if source is None:
        return []
    out: list[dict[str, Any]] = []
    for q in queries:
        out.extend(
            source.search(q, from_year=cfg["from_year"], max_results=cfg.get("s2_page", 100))
        )
    return out


def _run_arxiv(source, queries, cfg) -> list[dict[str, Any]]:
    if source is None:
        return []
    out: list[dict[str, Any]] = []
    for q in queries:
        out.extend(source.search(q, max_results=cfg.get("arxiv_page", 50)))
    return out


def _run_hf(source, queries, cfg) -> list[dict[str, Any]]:
    if source is None:
        return []
    out: list[dict[str, Any]] = []
    for q in queries:
        out.extend(source.search(q, max_results=cfg.get("hf_page", 50)))
    return out
