"""code_ref repo resolution: ordered candidate cascade (T1 paper-text + T2a PwC)."""

from __future__ import annotations

from pathlib import Path

from scripts.output.repo_resolve import (
    RepoCandidate,
    author_declares_closed,
    hf_official_repo,
    resolve_repo_candidates,
)


def test_to_repo_url_normalization_via_md(tmp_path: Path) -> None:
    md = tmp_path / "p.md"
    md.write_text(
        "Code: https://github.com/Owner/Repo.git/tree/main and dup https://github.com/Owner/Repo\n",
        encoding="utf-8",
    )
    cands = resolve_repo_candidates("2401.00001", md, {}, pwc_lookup=lambda _i: None)
    assert [c.url for c in cands] == [
        "https://github.com/Owner/Repo"
    ]  # .git/tree stripped, deduped
    assert cands[0].source == "paper-text"


def test_to_repo_url_strips_trailing_sentence_punctuation(tmp_path: Path) -> None:
    # "...code at https://github.com/nv/cosmos-transfer1." — the period is prose.
    md = tmp_path / "p.md"
    md.write_text("Released at https://github.com/nv/cosmos-transfer1.\n", encoding="utf-8")
    cands = resolve_repo_candidates("2401.00001", md, {}, pwc_lookup=lambda _i: None)
    assert [c.url for c in cands] == ["https://github.com/nv/cosmos-transfer1"]
    assert cands[0].trust == "search"


def test_resolution_order_pwc_official_before_paper_text(tmp_path: Path) -> None:
    # Highest-trust-first: the curated pwc-official MUST precede the paper-text grep
    # so a cited-baseline link in the text never beats the real official repo.
    md = tmp_path / "p.md"
    md.write_text("see https://github.com/auth/paperrepo for code\n", encoding="utf-8")
    cands = resolve_repo_candidates(
        "2401.00001",
        md,
        {"github_repo": "https://github.com/disc/fromdiscovery"},
        pwc_lookup=lambda _i: "https://github.com/pwc/official",
    )
    assert cands == [
        RepoCandidate("https://github.com/pwc/official", "pwc-official", "official"),
        RepoCandidate("https://github.com/auth/paperrepo", "paper-text", "search"),
        RepoCandidate("https://github.com/disc/fromdiscovery", "discovery", "search"),
    ]


def test_pwc_official_is_high_trust() -> None:
    cands = resolve_repo_candidates(
        "2411.15139", None, {}, pwc_lookup=lambda _i: "https://github.com/hustvl/diffusiondrive"
    )
    assert len(cands) == 1
    assert cands[0].source == "pwc-official"
    assert cands[0].trust == "official"


def test_no_candidates_when_nothing_found() -> None:
    assert resolve_repo_candidates("9999.99999", None, {}, pwc_lookup=lambda _i: None) == []


def test_author_declares_closed_is_high_precision(tmp_path: Path) -> None:
    closed = tmp_path / "c.md"
    closed.write_text("Due to IP, the code will not be released publicly.\n", encoding="utf-8")
    assert author_declares_closed(closed) is True

    openish = tmp_path / "o.md"
    openish.write_text("We release the code at github. Results are strong.\n", encoding="utf-8")
    assert author_declares_closed(openish) is False  # absence/normal text != closed
    assert author_declares_closed(None) is False


def test_t2b_t4_off_by_default(tmp_path: Path) -> None:
    # No hf_lookup / web_search injected → only T1/T2a/discovery, no network tiers.
    cands = resolve_repo_candidates(
        "2401.00001", None, {}, pwc_lookup=lambda _i: "https://github.com/pwc/official"
    )
    assert [c.source for c in cands] == ["pwc-official"]


def test_t2b_hf_lookup_added_after_offline_tiers() -> None:
    cands = resolve_repo_candidates(
        "2604.01765",
        None,
        {},
        pwc_lookup=lambda _i: None,
        hf_lookup=lambda _i: "https://github.com/youngzhou1999/DriveDreamer-Policy",
    )
    assert cands == [
        RepoCandidate("https://github.com/youngzhou1999/DriveDreamer-Policy", "hf-live", "search")
    ]


def test_t4_websearch_extracts_github_urls_from_results() -> None:
    results = [
        "Project page xiaomi-mlab.github.io/Orion (no repo here)",
        "Code: https://github.com/xiaomi-mlab/Orion — official",
        "dup https://github.com/xiaomi-mlab/Orion",
    ]
    cands = resolve_repo_candidates(
        "2503.19755",
        None,
        {},
        pwc_lookup=lambda _i: None,
        web_search=lambda _q: results,
    )
    assert cands == [RepoCandidate("https://github.com/xiaomi-mlab/Orion", "websearch", "search")]


def test_t4_websearch_skipped_when_a_higher_tier_already_found_a_repo() -> None:
    # Cost gate: T4 (a live websearch sub-agent) must fire ONLY for the long tail —
    # never when PwC/paper-text/discovery/HF already yielded a candidate.
    def _boom(_q):
        raise AssertionError("web_search must NOT run when a higher tier already found a repo")

    cands = resolve_repo_candidates(
        "2401.00001",
        None,
        {},
        pwc_lookup=lambda _i: "https://github.com/pwc/official",
        web_search=_boom,
    )
    assert [c.source for c in cands] == ["pwc-official"]


def test_t4_websearch_fires_only_when_all_higher_tiers_miss() -> None:
    # The long-tail recovery path (e.g. FastWAM): PwC frozen-table miss + no github link
    # in the paper + HF has no githubRepo → T4 websearch is the tier that recovers it.
    called = {"n": 0}

    def _search(_q):
        called["n"] += 1
        return ["https://github.com/yuantianyuan01/FastWAM official codebase"]

    cands = resolve_repo_candidates(
        "2603.16666",
        None,
        {},
        pwc_lookup=lambda _i: None,
        hf_lookup=lambda _i: None,
        web_search=_search,
    )
    assert called["n"] == 1
    assert cands == [
        RepoCandidate("https://github.com/yuantianyuan01/FastWAM", "websearch", "search")
    ]


def test_hf_artifacts_surface_as_candidates_even_when_a_github_repo_is_found() -> None:
    # "Read all of HF, not just githubRepo": linked models/datasets surface as
    # trust="artifact" candidates ALONGSIDE a found github repo (not gated on its absence).
    cands = resolve_repo_candidates(
        "2603.16666",
        None,
        {},
        pwc_lookup=lambda _i: "https://github.com/x/official",
        hf_artifacts=lambda _i: [
            ("model", "https://huggingface.co/yuanty/fastwam"),
            ("dataset", "https://huggingface.co/datasets/yuanty/robotwin2.0-fastwam"),
        ],
    )
    assert RepoCandidate("https://github.com/x/official", "pwc-official", "official") in cands
    arts = [(c.source, c.url) for c in cands if c.trust == "artifact"]
    assert arts == [
        ("hf-model", "https://huggingface.co/yuanty/fastwam"),
        ("hf-dataset", "https://huggingface.co/datasets/yuanty/robotwin2.0-fastwam"),
    ]


def test_hf_linked_artifacts_parses_models_datasets_spaces() -> None:
    from scripts.output.repo_resolve import hf_linked_artifacts

    data = {
        "linkedModels": [{"id": "yuanty/fastwam"}],
        "linkedDatasets": [{"id": "yuanty/robotwin2.0-fastwam"}],
        "linkedSpaces": [],
    }
    arts = hf_linked_artifacts("2603.16666v2", http_get=lambda _u, _h: data)
    assert arts == [
        ("model", "https://huggingface.co/yuanty/fastwam"),
        ("dataset", "https://huggingface.co/datasets/yuanty/robotwin2.0-fastwam"),
    ]


def test_hf_linked_artifacts_degrades_to_empty_on_error() -> None:
    from scripts.output.repo_resolve import hf_linked_artifacts

    def _boom(_u, _h):
        raise OSError("network down")

    assert hf_linked_artifacts("2603.16666", http_get=_boom) == []


def test_hf_official_repo_parses_and_strips_version() -> None:
    seen = {}

    def fake_get(url, headers):
        seen["url"] = url
        return {"githubRepo": "https://github.com/youngzhou1999/DriveDreamer-Policy"}

    repo = hf_official_repo("2604.01765v2", http_get=fake_get)
    assert repo == "https://github.com/youngzhou1999/DriveDreamer-Policy"
    assert seen["url"].endswith("/api/papers/2604.01765")  # version stripped


def test_hf_official_repo_none_on_missing_or_error() -> None:
    assert hf_official_repo("2604.01765", http_get=lambda _u, _h: {}) is None
    assert hf_official_repo(None, http_get=lambda _u, _h: {"githubRepo": "x"}) is None

    def boom(_u, _h):
        raise TimeoutError("slow")

    assert hf_official_repo("2604.01765", http_get=boom) is None


def test_make_repo_resolver_wires_t2b_default_and_optional_t4():
    from scripts.output.repo_resolve import hf_official_repo, make_repo_resolver

    r = make_repo_resolver()
    assert r.keywords["hf_lookup"] is hf_official_repo  # T2b on by default
    assert r.keywords["web_search"] is None  # T4 off unless supplied

    def ws(_q):
        return []

    assert make_repo_resolver(web_search=ws).keywords["web_search"] is ws
