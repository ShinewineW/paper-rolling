"""discover() orchestration: expand -> sources -> dedup -> authority -> rank."""

from __future__ import annotations

from scripts.discovery.discover import discover


def _c(**kw):
    base = {
        "openalex_id": None,
        "arxiv_id": None,
        "arxiv_version": None,
        "doi": None,
        "title": "",
        "year": 2026,
        "cited_by_count": 0,
        "influential_citation_count": None,
        "venue": None,
        "institutions": [],
        "github_repo": None,
        "github_stars": None,
        "oa_pdf_url": None,
        "abstract": "",
        "upvotes": None,
        "ai_keywords": [],
        "discovery_sources": [],
    }
    base.update(kw)
    return base


class FakeSource:
    def __init__(self, candidates):
        self._candidates = candidates

    def search(self, *args, **kwargs):
        return iter(self._candidates)


class FakeDblp:
    """Venue-enrichment source: maps a title -> a confirmed venue (or None)."""

    def __init__(self, venues: dict[str, str] | None = None):
        self._venues = venues or {}

    def venue_for_title(self, title: str) -> str | None:
        return self._venues.get(title)


def fake_llm(prompt):
    return ["topic", "MethodX"]


def make_sources():
    oa = FakeSource(
        [
            _c(
                doi="10.1/a",
                title="Authoritative Classic",
                cited_by_count=9000,
                year=2018,
                discovery_sources=["openalex"],
            ),
            _c(
                doi="10.1/b",
                title="CVPR New Work",
                year=2026,
                venue="CVPR",
                discovery_sources=["openalex"],
            ),
            _c(
                doi="10.1/c",
                title="Obscure Unranked Paper",
                year=2026,
                venue="RandomWorkshop",
                discovery_sources=["openalex"],
            ),
        ]
    )
    s2 = FakeSource(
        [
            _c(
                doi="10.1/a",
                title="Authoritative Classic",
                influential_citation_count=400,
                discovery_sources=["s2"],
            ),
        ]
    )
    arxiv = FakeSource([])
    dblp = FakeDblp()  # no venue confirmations by default (preserves prior behavior)
    hf = FakeSource(
        [
            _c(
                arxiv_id="2601.99999",
                title="Hot Repo Paper",
                year=2026,
                github_stars=900,
                upvotes=200,
                github_repo="https://github.com/x/h",
                discovery_sources=["hf_papers"],
            ),
        ]
    )
    return {"openalex": oa, "s2": s2, "arxiv": arxiv, "dblp": dblp, "hf_papers": hf}


def base_config():
    return {
        "topic": "end-to-end driving",
        "top_k": 2,
        "from_date": "2015-01-01",
        "from_year": "2015",
        "current_year": 2026,
        "overfetch_factor": 3,
    }


def test_discover_returns_authoritative_only_ranked():
    out = discover(base_config(), sources=make_sources(), llm=fake_llm)
    titles = [c["title"] for c in out]
    # Obscure paper fires no signal -> dropped (ADR-0001 OR scorer).
    assert "Obscure Unranked Paper" not in titles
    # The three authoritative ones survive.
    assert set(titles) == {"Authoritative Classic", "CVPR New Work", "Hot Repo Paper"}


def test_discover_sorts_by_authority_score_desc():
    out = discover(base_config(), sources=make_sources(), llm=fake_llm)
    scores = [c["authority_score"] for c in out]
    assert scores == sorted(scores, reverse=True)


def test_discover_merges_doi_across_openalex_and_s2():
    out = discover(base_config(), sources=make_sources(), llm=fake_llm)
    classic = next(c for c in out if c["title"] == "Authoritative Classic")
    assert classic["cited_by_count"] == 9000
    assert classic["influential_citation_count"] == 400
    assert set(classic["discovery_sources"]) == {"openalex", "s2"}


def test_discover_overfetches_but_caps_at_factor_times_topk():
    cfg = base_config()  # top_k=2, factor=3 -> cap 6; only 3 authoritative exist
    out = discover(cfg, sources=make_sources(), llm=fake_llm)
    assert len(out) <= cfg["top_k"] * cfg["overfetch_factor"]
    assert len(out) == 3  # all authoritative survivors, under the cap


def test_discover_tags_preprint_flag_and_signals():
    out = discover(base_config(), sources=make_sources(), llm=fake_llm)
    hot = next(c for c in out if c["title"] == "Hot Repo Paper")
    assert hot["preprint_flag"] is True  # arxiv_id, no reviewed venue
    assert hot["authority_signals"]["s4_heat"] is True
    assert "authority_score" in hot


def test_discover_dblp_enriches_venue_and_fires_s2_signal():
    # A candidate with NO venue would normally fire no signal and be dropped by
    # the ADR-0001 any-signal filter. DBLP confirms its venue is "CVPR" -> the
    # S2 venue signal fires, so it survives, AND its venue is the DBLP venue.
    oa = FakeSource(
        [
            _c(
                arxiv_id="2601.00001",
                title="Venueless Authoritative Work",
                year=2026,
                venue=None,  # no venue from the search sources
                discovery_sources=["openalex"],
            ),
        ]
    )
    dblp = FakeDblp({"Venueless Authoritative Work": "CVPR"})
    sources = {
        "openalex": oa,
        "s2": FakeSource([]),
        "arxiv": FakeSource([]),
        "dblp": dblp,
        "hf_papers": FakeSource([]),
    }
    out = discover(base_config(), sources=sources, llm=fake_llm)

    enriched = next(c for c in out if c["title"] == "Venueless Authoritative Work")
    # DBLP wrote the confirmed venue back onto the candidate...
    assert enriched["venue"] == "CVPR"
    # ...the S2 venue signal fired (so it survived the any-signal filter)...
    assert enriched["authority_signals"]["s2_venue"] is True
    # ...and "dblp" was appended to the candidate's discovery sources (deduped).
    assert "dblp" in enriched["discovery_sources"]
    assert enriched["discovery_sources"].count("dblp") == 1


def test_discover_dblp_does_not_overwrite_existing_venue():
    # A candidate that ALREADY has a usable venue is not re-queried against DBLP.
    oa = FakeSource(
        [
            _c(
                arxiv_id="2601.00002",
                title="Already Has Venue",
                year=2026,
                venue="CVPR",
                discovery_sources=["openalex"],
            ),
        ]
    )
    dblp = FakeDblp({"Already Has Venue": "ICCV"})  # would differ if it ran
    sources = {
        "openalex": oa,
        "s2": FakeSource([]),
        "arxiv": FakeSource([]),
        "dblp": dblp,
        "hf_papers": FakeSource([]),
    }
    out = discover(base_config(), sources=sources, llm=fake_llm)

    cand = next(c for c in out if c["title"] == "Already Has Venue")
    assert cand["venue"] == "CVPR"  # untouched
    assert "dblp" not in cand["discovery_sources"]


def test_discover_each_candidate_has_full_interface_shape():
    out = discover(base_config(), sources=make_sources(), llm=fake_llm)
    required = {
        "arxiv_id",
        "arxiv_version",
        "doi",
        "title",
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
    }
    for cand in out:
        assert required.issubset(cand.keys())


def test_discover_survives_a_source_outage():
    # Codex Round-14 / LS-5: one source raising HttpUnavailable must NOT abort
    # multi-source discovery (and the tick) — the surviving sources still
    # contribute. Before the fix, discover() propagated the exception and crashed.
    from scripts.discovery.http_client import HttpUnavailable

    class _DownSource:
        def search(self, *args, **kwargs):
            raise HttpUnavailable("openalex is down this tick")

    sources = {
        "openalex": _DownSource(),  # primary source is down
        "s2": FakeSource(
            [
                _c(
                    arxiv_id="2601.09999",
                    title="Survivor",
                    year=2026,
                    venue="CVPR",  # fires the S2 venue signal -> authoritative
                    cited_by_count=100,
                    discovery_sources=["s2"],
                )
            ]
        ),
        "arxiv": FakeSource([]),
        "dblp": FakeDblp({}),
        "hf_papers": FakeSource([]),
    }
    out = discover(base_config(), sources=sources, llm=fake_llm)

    # No crash, and the surviving s2 candidate came through.
    assert any(c["title"] == "Survivor" for c in out)


def test_discover_drops_retracted_papers():
    # ROADMAP B1: a paper flagged is_retracted (OpenAlex/Crossref) is excluded
    # even when it would otherwise be authoritative (high cites + top venue).
    oa = FakeSource(
        [
            _c(
                doi="10.1/retracted",
                title="Retracted But Famous",
                year=2024,
                cited_by_count=5000,
                venue="CVPR",
                is_retracted=True,
                discovery_sources=["openalex"],
            ),
            _c(
                doi="10.1/ok",
                title="Clean Authoritative Work",
                year=2026,
                venue="CVPR",
                cited_by_count=100,
                discovery_sources=["openalex"],
            ),
        ]
    )
    sources = {
        "openalex": oa,
        "s2": FakeSource([]),
        "arxiv": FakeSource([]),
        "dblp": FakeDblp({}),
        "hf_papers": FakeSource([]),
    }
    titles = [c["title"] for c in discover(base_config(), sources=sources, llm=fake_llm)]
    assert "Retracted But Famous" not in titles
    assert "Clean Authoritative Work" in titles


def test_search_source_registry_lists_the_fanout_sources():
    """The fan-out is driven by the _SEARCH_SOURCES registry (ADR-0002 seam),
    not a hardcoded body. DBLP is absent — it is venue-enrichment, not fan-out.
    """
    from scripts.discovery import discover as disc

    assert [k for k, _ in disc._SEARCH_SOURCES] == ["openalex", "s2", "arxiv", "hf_papers"]


def test_discover_list_mode_returns_only_forced_without_touching_sources():
    from scripts.discovery.discover import discover

    def boom_llm(*a, **k):
        raise AssertionError("LLM query-expansion must NOT run in list mode")

    class BoomSource:
        def search(self, *a, **k):
            raise AssertionError("sources must NOT be queried in list mode")

    sources = {"openalex": BoomSource(), "s2": BoomSource(), "arxiv": BoomSource()}
    cfg = {
        "topic": "my world-model list",
        "top_k": 5,
        "auto_discover": False,
        "force_include": [
            {"arxiv_id": "2407.01392", "title": "DiffusionForcing"},
            {"arxiv_id": "1803.10122", "title": "WorldModels"},
        ],
    }

    out = discover(cfg, sources, boom_llm)

    assert [c["arxiv_id"] for c in out] == ["2407.01392", "1803.10122"]
    assert all(c.get("forced") for c in out)  # _build_forced marked them


def test_registering_a_new_source_is_drop_in(monkeypatch):
    """Appending one entry to _SEARCH_SOURCES fans a new source in — no edit to
    discover()'s body. Proves the source seam is genuinely drop-in (ADR-0002)."""
    from scripts.discovery import discover as disc

    extra = FakeSource(
        [
            _c(
                arxiv_id="2601.07777",
                title="Registered Source Paper",
                year=2026,
                venue="CVPR",  # fires S2 → authoritative
                discovery_sources=["extra"],
            )
        ]
    )

    def _run_extra(source, queries, cfg):
        out = []
        for q in queries:
            out.extend(source.search(q))
        return out

    monkeypatch.setattr(disc, "_SEARCH_SOURCES", disc._SEARCH_SOURCES + (("extra", _run_extra),))
    sources = {**make_sources(), "extra": extra}
    out = discover(base_config(), sources=sources, llm=fake_llm)
    assert any(c["title"] == "Registered Source Paper" for c in out)


def test_discover_survives_dblp_outage_during_enrichment():
    # Codex Round-15 / LS-5: a DBLP HttpUnavailable during venue enrichment must
    # NOT abort discovery. A venue-less but otherwise-authoritative candidate
    # (whitelisted institution -> S3 signal) triggers the DBLP call; the outage is
    # swallowed and the candidate still survives.
    from scripts.discovery.http_client import HttpUnavailable

    class _DownDblp:
        def venue_for_title(self, title):
            raise HttpUnavailable("dblp is down this tick")

    sources = {
        "openalex": FakeSource(
            [
                _c(
                    arxiv_id="2601.08888",
                    title="NoVenueButFamous",
                    year=2026,
                    venue=None,  # venue-less -> triggers DBLP enrichment
                    cited_by_count=500,
                    institutions=["Google"],  # S3 institution signal -> authoritative
                    discovery_sources=["openalex"],
                )
            ]
        ),
        "s2": FakeSource([]),
        "arxiv": FakeSource([]),
        "dblp": _DownDblp(),
        "hf_papers": FakeSource([]),
    }
    out = discover(base_config(), sources=sources, llm=fake_llm)

    # discover did not crash on the DBLP outage; the candidate survived (via S3).
    assert any(c["title"] == "NoVenueButFamous" for c in out)
