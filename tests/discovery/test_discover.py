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
    dblp = FakeSource([])
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
