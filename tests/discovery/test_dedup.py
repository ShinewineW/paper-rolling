"""Cross-source dedup + field merge (D-发现-7)."""

from __future__ import annotations

from scripts.discovery.dedup import dedup_candidates, merge_pair


def _c(**kw):
    base = {
        "openalex_id": None,
        "arxiv_id": None,
        "arxiv_version": None,
        "doi": None,
        "title": "",
        "year": None,
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


def test_doi_dedup_merges_two_sources():
    a = _c(
        doi="10.1/x",
        title="Attention Is All You Need",
        cited_by_count=134000,
        discovery_sources=["openalex"],
    )
    b = _c(
        doi="10.1/x",
        title="Attention is all you need",
        influential_citation_count=8200,
        github_repo="https://github.com/x/t",
        discovery_sources=["s2"],
    )
    out = dedup_candidates([a, b])
    assert len(out) == 1
    m = out[0]
    assert m["cited_by_count"] == 134000
    assert m["influential_citation_count"] == 8200
    assert m["github_repo"] == "https://github.com/x/t"
    assert set(m["discovery_sources"]) == {"openalex", "s2"}


def test_arxiv_id_version_dedup():
    a = _c(arxiv_id="2601.01234", arxiv_version="v2", title="Driving", discovery_sources=["arxiv"])
    b = _c(
        arxiv_id="2601.01234",
        arxiv_version="v2",
        title="Driving",
        upvotes=88,
        discovery_sources=["hf_papers"],
    )
    out = dedup_candidates([a, b])
    assert len(out) == 1
    assert out[0]["upvotes"] == 88


def test_different_arxiv_versions_are_distinct():
    a = _c(arxiv_id="2601.01234", arxiv_version="v1", title="Driving")
    b = _c(arxiv_id="2601.01234", arxiv_version="v2", title="Driving")
    assert len(dedup_candidates([a, b])) == 2


def test_title_similarity_dedup_when_no_ids():
    a = _c(
        title="Deep Residual Learning for Image Recognition",
        year=2016,
        cited_by_count=180000,
        discovery_sources=["openalex"],
    )
    b = _c(
        title="Deep residual learning for image recognition.",
        year=2016,
        venue="CVPR",
        discovery_sources=["dblp"],
    )
    out = dedup_candidates([a, b])
    assert len(out) == 1
    assert out[0]["venue"] == "CVPR"


def test_dissimilar_titles_stay_separate():
    a = _c(title="Deep Residual Learning for Image Recognition")
    b = _c(title="Attention Is All You Need")
    assert len(dedup_candidates([a, b])) == 2


def test_merge_pair_prefers_nonnull_and_unions_sources():
    a = _c(cited_by_count=100, venue=None, discovery_sources=["openalex"])
    b = _c(cited_by_count=0, venue="CVPR", discovery_sources=["dblp"])
    m = merge_pair(a, b)
    assert m["cited_by_count"] == 100
    assert m["venue"] == "CVPR"
    assert set(m["discovery_sources"]) == {"openalex", "dblp"}
