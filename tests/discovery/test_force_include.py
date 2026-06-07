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


def test_campaign_force_include_requires_an_identifier():
    with pytest.raises(GateError):
        CampaignConfig(
            topic="world models for planning",
            n_per_tick=5,
            is_ad_domain=False,
            force_include=[{"title": "no identifier here"}],
        )
