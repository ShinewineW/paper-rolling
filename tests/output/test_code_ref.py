"""code_ref: clone-verify ordered candidates → three-state pointer; clone deleted."""

from __future__ import annotations

import subprocess
from pathlib import Path

from scripts.output.code_ref import Innovation, build_code_ref
from scripts.output.repo_resolve import RepoCandidate


def _fake_git(monkeypatch, files_by_url: dict[str, dict[str, str]]):
    """Stub `git clone` to materialize per-URL repo contents, and `git rev-parse`."""
    real_run = subprocess.run

    def fake_run(cmd, *args, **kwargs):
        if cmd[:2] == ["git", "clone"]:
            url, dest = cmd[-2], Path(cmd[-1])
            dest.mkdir(parents=True, exist_ok=True)
            for name, body in files_by_url.get(url, {}).items():
                (dest / name).write_text(body, encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if cmd[:2] == ["git", "rev-parse"]:
            return subprocess.CompletedProcess(cmd, 0, "abc1234def5678\n", "")
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", fake_run)


_SEARCH = "https://github.com/x/diffusiondrive"
_OFFICIAL = "https://github.com/pwc/official"


def test_search_candidate_verified_by_innovation_symbol(tmp_path, monkeypatch):
    _fake_git(monkeypatch, {_SEARCH: {"model.py": "class TruncatedDiffusion:\n    pass\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_SEARCH, "paper-text", "search")],
        innovations=[Innovation(name="Truncated diffusion", grep="TruncatedDiffusion")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2411.15139",
    )
    body = out.read_text(encoding="utf-8")
    assert _SEARCH in body
    assert "abc1234def5678" in body  # pinned SHA
    assert "model.py:1" in body  # located
    assert "Source**: paper-text (verified)" in body
    assert not (tmp_path / "repos" / "2411.15139").exists()  # clone deleted


def test_official_candidate_accepted_on_clone_without_locate(tmp_path, monkeypatch):
    # PwC is_official: a clean clone is enough even if no innovation symbol resolves.
    _fake_git(monkeypatch, {_OFFICIAL: {"README.md": "a project\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_OFFICIAL, "pwc-official", "official")],
        innovations=[Innovation(name="X", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2401.0",
    )
    body = out.read_text(encoding="utf-8")
    assert _OFFICIAL in body
    assert "Source**: pwc-official (official-flagged)" in body


def test_search_candidate_rejected_when_unverified(tmp_path, monkeypatch):
    # No innovation symbol AND no arxiv_id/title in repo → not THE repo → not found.
    _fake_git(monkeypatch, {_SEARCH: {"other.py": "irrelevant\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_SEARCH, "paper-text", "search")],
        innovations=[Innovation(name="X", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2401.0",
        arxiv_id="2401.00001",
        title="Some Paper",
    )
    body = out.read_text(encoding="utf-8")
    assert "No public repository found" in body
    assert "NOT a closed-source" in body


def test_search_candidate_verified_by_arxiv_id_in_readme(tmp_path, monkeypatch):
    _fake_git(monkeypatch, {_SEARCH: {"README.md": "Paper: arxiv.org/abs/2411.15139\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_SEARCH, "paper-text", "search")],
        innovations=[Innovation(name="X", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2411.15139",
        arxiv_id="2411.15139",
    )
    assert "Source**: paper-text (verified)" in out.read_text(encoding="utf-8")


def test_first_unverified_then_official_accepted(tmp_path, monkeypatch):
    # paper-text repo is a cited baseline (no match) → fall through to PwC official.
    _fake_git(
        monkeypatch,
        {
            _SEARCH: {"baseline.py": "unrelated\n"},
            _OFFICIAL: {"README.md": "the real repo\n"},
        },
    )
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[
            RepoCandidate(_SEARCH, "paper-text", "search"),
            RepoCandidate(_OFFICIAL, "pwc-official", "official"),
        ],
        innovations=[Innovation(name="X", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2401.0",
        arxiv_id="2401.00001",
    )
    body = out.read_text(encoding="utf-8")
    assert _OFFICIAL in body and _SEARCH not in body


def test_declared_repo_clone_failure_degrades_to_unavailable(tmp_path, monkeypatch):
    """Codex R17: a declared repo that won't clone → 'unavailable' pointer, not crash."""
    real_run = subprocess.run

    def failing_clone(cmd, *args, **kwargs):
        if cmd[:2] == ["git", "clone"]:
            raise subprocess.CalledProcessError(128, cmd, stderr="repository not found")
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", failing_clone)
    out = tmp_path / "code_ref.md"
    url = "https://github.com/x/deleted-or-private"
    build_code_ref(
        candidates=[RepoCandidate(url, "discovery", "search")],
        innovations=[Innovation(name="X", grep="X")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2411.15139",
    )
    body = out.read_text(encoding="utf-8")
    assert "unavailable" in body.lower()
    assert url in body  # link kept for provenance
    assert "CalledProcessError" in body
    assert not (tmp_path / "repos" / "2411.15139").exists()


def test_no_candidates_searched_not_found(tmp_path):
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[],
        innovations=[Innovation(name="X", grep="X")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="doi-abcd1234",
    )
    body = out.read_text(encoding="utf-8")
    assert "No public repository found" in body
    assert "NOT a closed-source" in body
    assert "closed-source paper" not in body.lower()  # the old mislabel is gone


def test_no_candidates_author_declared_closed(tmp_path):
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[],
        innovations=[Innovation(name="X", grep="X")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="doi-abcd1234",
        declared_closed=True,
    )
    assert "Author-declared closed-source" in out.read_text(encoding="utf-8")
