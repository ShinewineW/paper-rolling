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

import re
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
        if cand.get("is_retracted"):
            continue  # ROADMAP B1: drop retracted work (OpenAlex/Crossref flag)
        signals, score = score_authority(cand, campaign_config)
        if not any(signals.values()):
            continue  # ADR-0001: no signal fired -> not authoritative
        cand = dict(cand)
        cand["authority_signals"] = signals
        cand["authority_score"] = score
        cand["preprint_flag"] = preprint_flag(cand)
        scored.append(_project(cand))

    scored.sort(key=lambda c: c["authority_score"], reverse=True)

    forced = _build_forced(campaign_config.get("force_include") or [])
    if not forced:
        return scored[:cap]
    # Force-include (中枢-D1): mandatory papers sit at the FRONT of the pool
    # (processed first) and BYPASS the authority filter — force-include is
    # mandatory, not signal-authoritative. They still go through ingest + G2/G3.
    # If discovery ALSO found a forced paper, MERGE discovery's ingest-enabling
    # metadata (oa_pdf_url / version / real title / venue) into the forced entry —
    # then drop the discovered duplicate so the enriched forced version wins once.
    kept: list[dict[str, Any]] = []
    for c in scored:
        c_tokens = _identity_tokens(c)
        match = next((f for f in forced if _identity_tokens(f) & c_tokens), None)
        if match is None:
            kept.append(c)
            continue
        for k in ("oa_pdf_url", "arxiv_id", "arxiv_version", "doi", "title", "venue", "year"):
            if not match.get(k) and c.get(k):
                match[k] = c[k]
    return forced + kept[:cap]


def _project(cand: dict[str, Any]) -> dict[str, Any]:
    """Reduce a scored candidate to exactly the public interface fields.

    `authors` is normalized to a list so downstream `candidate["authors"]` is
    always safe even for sources that don't supply it (Round 15 #1).
    """
    out = {field: cand.get(field) for field in _INTERFACE_FIELDS}
    out["authors"] = out.get("authors") or []
    return out


def _identity_tokens(cand: dict[str, Any]) -> set[tuple[str, str]]:
    """Identity tokens for force-include dedup: version-stripped arXiv id,
    lowercased DOI, whitespace-normalized lowercased title. A non-empty
    intersection between two candidates means they are the same paper."""
    toks: set[tuple[str, str]] = set()
    aid = cand.get("arxiv_id")
    if aid:
        toks.add(("arxiv", re.sub(r"v\d+$", "", str(aid))))
    doi = cand.get("doi")
    if doi:
        toks.add(("doi", str(doi).strip().lower()))
    url = cand.get("oa_pdf_url")
    if url:
        toks.add(("url", str(url).strip()))
    title = cand.get("title")
    if title:
        toks.add(("title", " ".join(str(title).lower().split())))
    return toks


def _build_forced(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Project force-included papers into pool candidates (中枢-D1).

    Each is marked `forced` + `discovery_sources=["forced"]`, carries the
    identifiers the user supplied (arxiv_id / oa_pdf_url / doi / title), and is
    prepended to the pool. They skip the authority filter but NOT the downstream
    quality gates (ingest + G2 + G3). `title` defaults to an identifier so the
    naming / ingest path never KeyErrors on a title-less entry.
    """
    forced: list[dict[str, Any]] = []
    for e in entries:
        cand = _project(dict(e))
        cand["discovery_sources"] = ["forced"]
        cand["forced"] = True
        cand["authority_signals"] = {"forced": True}
        cand["authority_score"] = 0.0
        if not cand.get("title"):
            # Validation requires an identity (arxiv_id / doi / title); fall back
            # to a UNIQUE id (never a shared sentinel) so two title-less entries
            # cannot collapse into one identity / corpus dir / ledger key.
            cand["title"] = cand.get("arxiv_id") or cand.get("doi") or cand.get("oa_pdf_url")
        forced.append(cand)
    return forced


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
# under. See docs/guides/EXTENDING.md.
#
# DBLP is intentionally NOT here: it is a venue-ENRICHMENT source (queried per
# candidate by title after dedup), not a query fan-out source.
_SEARCH_SOURCES: tuple[tuple[str, Callable[..., list[dict[str, Any]]]], ...] = (
    ("openalex", _run_openalex),
    ("s2", _run_s2),
    ("arxiv", _run_arxiv),
    ("hf_papers", _run_hf),
)
