"""code_ref repo resolution: ordered candidate cascade (T1 paper-text + T2a PwC)."""

from __future__ import annotations

from pathlib import Path

from scripts.output.repo_resolve import (
    RepoCandidate,
    author_declares_closed,
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


def test_resolution_order_paper_text_then_pwc_then_discovery(tmp_path: Path) -> None:
    md = tmp_path / "p.md"
    md.write_text("see https://github.com/auth/paperrepo for code\n", encoding="utf-8")
    cands = resolve_repo_candidates(
        "2401.00001",
        md,
        {"github_repo": "https://github.com/disc/fromdiscovery"},
        pwc_lookup=lambda _i: "https://github.com/pwc/official",
    )
    assert cands == [
        RepoCandidate("https://github.com/auth/paperrepo", "paper-text", "search"),
        RepoCandidate("https://github.com/pwc/official", "pwc-official", "official"),
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
