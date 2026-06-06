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
from scripts.discovery.http_client import HttpUnavailable
from scripts.discovery.query_expand import expand_queries


def _safe_source(fn: Callable[..., list], *args: Any) -> list:
    """LS-5: a degraded source (HttpUnavailable) is treated as MISSING, not fatal.

    One source going down must NOT abort multi-source discovery (and the tick);
    the other sources still contribute (Codex Round-14). ``HttpUnavailable`` is
    the documented "this source is unavailable for this query" signal.
    """
    try:
        return fn(*args)
    except HttpUnavailable:
        return []


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
    for key, adapter in _SEARCH_SOURCES:
        raw.extend(_safe_source(adapter, sources.get(key), queries, campaign_config))

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
        raw.extend(
            _safe_source(_run_openalex, sources.get("openalex"), extra_queries, campaign_config)
        )

    merged = dedup_candidates(raw)

    # DBLP venue ENRICHMENT (D-发现-3, signal S2): for candidates that arrived
    # without a usable venue, ask DBLP to confirm one by title match. A
    # DBLP-confirmed top venue then lets authority.score_authority's S2 signal
    # fire, so the candidate can survive the ADR-0001 any-signal filter below.
    dblp = sources.get("dblp")
    if dblp is not None:
        for cand in merged:
            if cand.get("venue"):
                continue
            try:
                venue = dblp.venue_for_title(cand["title"])
            except HttpUnavailable:
                # LS-5: DBLP is down this tick — skip venue enrichment for the
                # rest rather than abort discovery (Codex Round-15).
                break
            if venue:
                cand["venue"] = venue
                srcs = cand.setdefault("discovery_sources", [])
                if "dblp" not in srcs:
                    srcs.append("dblp")

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


# Discovery-source registry — the extension seam (ADR-0002). discover() fans the
# expanded queries across these in order; each adapter owns its source's search
# params (date floor, page size), so discover()'s body stays source-agnostic.
#
# ADD A SOURCE (drop-in, no discover()-body edit): write a source class exposing
# `.search(topic, ...) -> Iterable[candidate-dict]`, add a `_run_<name>(source,
# queries, cfg)` adapter above, and append one `("<key>", _run_<name>)` entry
# here. The `<key>` is the dict key the production wiring registers the source
# under. See docs/EXTENDING.md.
#
# DBLP is intentionally NOT here: it is a venue-ENRICHMENT source (queried per
# candidate by title after dedup), not a query fan-out source.
_SEARCH_SOURCES: tuple[tuple[str, Callable[..., list[dict[str, Any]]]], ...] = (
    ("openalex", _run_openalex),
    ("s2", _run_s2),
    ("arxiv", _run_arxiv),
    ("hf_papers", _run_hf),
)
