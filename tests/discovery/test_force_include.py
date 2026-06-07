"""Force-include (中枢-D1): user-specified papers that MUST enter the candidate
pool — bypassing the authority filter, deduped against discovery, prepended to
the front — while still going through ingest + G2 + G3 downstream."""

from __future__ import annotations

import pytest
from scripts.campaign import CampaignConfig, GateError, load_campaign, write_campaign
from scripts.discovery.discover import _build_forced, _identity_tokens, discover


class FakeSource:
    """A discovery source whose .search() yields a fixed list (DBLP shape too)."""

    def __init__(self, results=None):
        self._results = list(results or [])

    def search(self, *_args, **_kwargs):
        yield from self._results

    def venue_for_title(self, _title):  # DBLP enrichment surface
        return None


def _cfg(**override):
    cfg = {
        "topic": "world models for planning",
        "top_k": 5,
        "overfetch_factor": 3,
        "is_ad_domain": False,
        "from_year": 2024,
        "from_date": "2024-01-01",
        "current_year": 2026,
    }
    cfg.update(override)
    return cfg


def _sources(openalex=None):
    return {
        "openalex": FakeSource(openalex),
        "s2": FakeSource(),
        "arxiv": FakeSource(),
        "dblp": FakeSource(),
        "hf_papers": FakeSource(),
    }


def _llm(_prompt):
    return []


# --- discover()-level behavior -------------------------------------------------


def test_force_include_appears_even_with_zero_discovery():
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001", "title": "Forced Paper"}])
    pool = discover(cfg, _sources(), _llm)  # sources return nothing at all
    assert len(pool) == 1
    f = pool[0]
    assert f["forced"] is True
    assert f["discovery_sources"] == ["forced"]
    assert f["arxiv_id"] == "2401.00001"
    assert f["title"] == "Forced Paper"


def test_force_include_is_prepended_to_the_front():
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001", "title": "Forced"}])
    # whatever discovery yields, the forced paper is processed first
    disc = {"arxiv_id": "2402.99999", "title": "Discovered", "venue": "NeurIPS", "year": 2025}
    pool = discover(cfg, _sources(openalex=[disc]), _llm)
    assert pool[0].get("forced") is True


def test_force_include_dedup_no_duplicate_arxiv():
    # discovery also surfaces the same arXiv id -> it must appear ONCE (forced wins)
    same = {"arxiv_id": "2401.00001", "title": "Same", "venue": "NeurIPS", "year": 2025}
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001", "title": "Same (forced)"}])
    pool = discover(cfg, _sources(openalex=[same]), _llm)
    hits = [c for c in pool if c.get("arxiv_id") == "2401.00001"]
    assert len(hits) == 1
    assert hits[0].get("forced") is True


def test_force_include_dedup_by_doi():
    # discovery surfaces the same paper keyed by DOI (no arXiv id) -> match on the
    # doi identity token, so it still appears ONCE with the forced entry winning.
    disc = {"doi": "10.1/abc", "title": "Disc", "venue": "ICML", "year": 2025}
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001", "doi": "10.1/ABC", "title": "Forced"}])
    pool = discover(cfg, _sources(openalex=[disc]), _llm)
    assert len(pool) == 1
    assert pool[0]["forced"] is True


def test_force_include_dedup_by_oa_pdf_url():
    # same direct-PDF URL on both sides -> deduped via the url identity token.
    url = "https://example.org/paper.pdf"
    disc = {"oa_pdf_url": url, "title": "Disc", "venue": "ICLR", "year": 2025}
    cfg = _cfg(force_include=[{"oa_pdf_url": url, "title": "Forced"}])
    pool = discover(cfg, _sources(openalex=[disc]), _llm)
    assert len(pool) == 1
    assert pool[0]["forced"] is True


def test_force_include_dedup_by_title():
    # discovery surfaces the same paper matched by normalized TITLE alone (no shared
    # arXiv id / DOI / URL) -> still deduped to one entry, forced winning.
    disc = {"arxiv_id": "2403.55555", "title": "Shared  Title", "venue": "CVPR", "year": 2025}
    cfg = _cfg(force_include=[{"oa_pdf_url": "https://x/p.pdf", "title": "shared title"}])
    pool = discover(cfg, _sources(openalex=[disc]), _llm)
    assert len(pool) == 1
    assert pool[0]["forced"] is True


def test_force_include_enriched_by_discovery():
    # STRUCTURAL fix: when discovery also finds a forced paper, its ingest-enabling
    # metadata (oa_pdf_url / venue / year) is MERGED into the forced entry instead
    # of being discarded — the forced entry keeps its identity but gains the PDF URL.
    disc = {
        "arxiv_id": "2401.00001",
        "title": "Disc",
        "venue": "NeurIPS",
        "year": 2025,
        "oa_pdf_url": "https://example.org/found.pdf",
    }
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001", "title": "Forced"}])
    pool = discover(cfg, _sources(openalex=[disc]), _llm)
    assert len(pool) == 1
    f = pool[0]
    assert f["forced"] is True
    assert f["title"] == "Forced"  # forced identity wins
    assert f["oa_pdf_url"] == "https://example.org/found.pdf"  # discovery merged in
    assert f["venue"] == "NeurIPS"
    assert f["year"] == 2025


def test_distinct_forced_papers_do_not_collapse():
    # Two title-less forced entries with DIFFERENT arXiv ids must stay TWO papers
    # (the title fallback is a unique id, never a shared sentinel that would
    # collapse them into one corpus dir / ledger key).
    cfg = _cfg(force_include=[{"arxiv_id": "2401.00001"}, {"arxiv_id": "2402.00002"}])
    pool = discover(cfg, _sources(), _llm)
    assert len(pool) == 2
    assert {c["title"] for c in pool} == {"2401.00001", "2402.00002"}


def test_no_force_include_returns_plain_pool():
    pool = discover(_cfg(), _sources(), _llm)  # no force_include key at all
    assert pool == []


def test_identity_tokens_strip_arxiv_version():
    assert _identity_tokens({"arxiv_id": "2401.00001v3"}) == {("arxiv", "2401.00001")}


def test_build_forced_defaults_title_and_marks():
    forced = _build_forced([{"arxiv_id": "2401.00001"}])
    assert forced[0]["title"] == "2401.00001"  # title-less entry won't KeyError on ingest
    assert forced[0]["forced"] is True
    assert forced[0]["discovery_sources"] == ["forced"]


# --- campaign-config persistence + validation ---------------------------------


def test_campaign_force_include_roundtrip(tmp_path):
    cfg = CampaignConfig(
        topic="world models for planning",
        n_per_tick=5,
        is_ad_domain=False,
        force_include=[{"arxiv_id": "2401.00001", "title": "X"}],
    )
    write_campaign(tmp_path, cfg)
    loaded = load_campaign(tmp_path)
    assert loaded.force_include == [{"arxiv_id": "2401.00001", "title": "X"}]


def test_campaign_force_include_defaults_empty():
    cfg = CampaignConfig(topic="world models for planning", n_per_tick=5, is_ad_domain=False)
    assert cfg.force_include == []


def _force_cfg(force_include):
    return CampaignConfig(
        topic="world models for planning",
        n_per_tick=5,
        is_ad_domain=False,
        force_include=force_include,
    )


def test_force_include_title_only_rejected_no_ingestible_source():
    # A title alone gives identity but NO ingestible source (no arXiv id / PDF URL)
    # — the engine cannot fetch it, so the Hard Gate rejects it rather than letting
    # it silently quarantine every tick.
    with pytest.raises(GateError, match="ingestible source"):
        _force_cfg([{"title": "no fetchable source here"}])


def test_force_include_doi_only_rejected_no_ingestible_source():
    # A bare DOI is NOT ingestible (there is no DOI->PDF resolver in the pipeline),
    # so a doi-only entry is rejected at the gate — not accepted then quarantined.
    with pytest.raises(GateError, match="ingestible source"):
        _force_cfg([{"doi": "10.1/abc"}])


def test_force_include_url_only_rejected_no_identity():
    # An oa_pdf_url is ingestible but carries no stable identity; without a title
    # two url-only entries could collide into one corpus dir / ledger key, so a
    # url-only entry must add a title.
    with pytest.raises(GateError, match="distinct identity"):
        _force_cfg([{"oa_pdf_url": "https://example.org/p.pdf"}])


def test_force_include_url_with_title_accepted():
    cfg = _force_cfg([{"oa_pdf_url": "https://example.org/p.pdf", "title": "T"}])
    assert cfg.force_include == [{"oa_pdf_url": "https://example.org/p.pdf", "title": "T"}]
