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


def test_locate_reports_source_file_not_doc_match(tmp_path, monkeypatch):
    # The grep symbol appears in BOTH README.md (sorts first) and model.py. The
    # location must point at the SOURCE file, not the README (honesty: a code
    # location is code, not prose). Without the _CODE_EXT filter, README.md:1 wins.
    _fake_git(
        monkeypatch,
        {_SEARCH: {"README.md": "see MySymbol in the docs\n", "model.py": "class MySymbol:\n"}},
    )
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_SEARCH, "paper-text", "search")],
        innovations=[Innovation(name="My innovation", grep="MySymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2411.15139",
    )
    body = out.read_text(encoding="utf-8")
    assert "model.py:1" in body
    assert "README.md:" not in body  # the doc match is never reported as a code location


def test_unresolved_innovations_omit_not_found_rows(tmp_path, monkeypatch):
    # An accepted (official) repo where NO innovation symbol resolves to source must
    # NOT render a table of '_not found_' rows — it omits the map and says so honestly,
    # keeping the verified repo + SHA.
    _fake_git(monkeypatch, {_OFFICIAL: {"README.md": "a project\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[RepoCandidate(_OFFICIAL, "pwc-official", "official")],
        innovations=[Innovation(name="Unfindable", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2401.1",
    )
    body = out.read_text(encoding="utf-8")
    assert _OFFICIAL in body and "abc1234def5678" in body  # repo + SHA kept
    assert "_not found_" not in body
    assert "## Innovation → code location" not in body
    assert "not mechanically resolved" in body


def test_hf_artifacts_rendered_without_cloning_when_no_github(tmp_path, monkeypatch):
    # trust="artifact" candidates (HF models/datasets) are NOT clone-verified — they
    # render in a "Linked artifacts" section. No github candidate → not-found primary,
    # artifacts surfaced below (so 'no repo' never reads as 'no code/artifacts').
    def _no_clone(cmd, *a, **k):
        raise AssertionError(f"artifacts must not be git-cloned: {cmd}")

    monkeypatch.setattr(subprocess, "run", _no_clone)
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[
            RepoCandidate("https://huggingface.co/yuanty/fastwam", "hf-model", "artifact"),
            RepoCandidate(
                "https://huggingface.co/datasets/yuanty/rt2-fastwam", "hf-dataset", "artifact"
            ),
        ],
        innovations=[],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2603.16666",
    )
    body = out.read_text(encoding="utf-8")
    assert "## Linked artifacts (Hugging Face)" in body
    assert "**Model**: https://huggingface.co/yuanty/fastwam" in body
    assert "**Dataset**: https://huggingface.co/datasets/yuanty/rt2-fastwam" in body
    assert "No public repository found" in body  # no github → not-found primary + artifacts below


def test_found_github_repo_keeps_artifacts_section(tmp_path, monkeypatch):
    # A verified github repo AND linked HF artifacts: both surface (primary repo pointer
    # + the artifacts section below it).
    _fake_git(monkeypatch, {_OFFICIAL: {"README.md": "proj\n"}})
    out = tmp_path / "code_ref.md"
    build_code_ref(
        candidates=[
            RepoCandidate(_OFFICIAL, "pwc-official", "official"),
            RepoCandidate("https://huggingface.co/yuanty/fastwam", "hf-model", "artifact"),
        ],
        innovations=[Innovation(name="X", grep="NoSuchSymbol")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="2401.2",
    )
    body = out.read_text(encoding="utf-8")
    assert "**Pinned commit**" in body  # github repo found + verified (primary)
    assert "## Linked artifacts (Hugging Face)" in body  # artifacts still surfaced
    assert "**Model**: https://huggingface.co/yuanty/fastwam" in body
