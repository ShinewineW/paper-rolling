"""Shallow clone → pointer → delete (分析-D2): clone must not survive."""

from __future__ import annotations

import subprocess
from pathlib import Path

from scripts.output.code_ref import Innovation, build_code_ref


def _fake_git(monkeypatch, clone_root: Path):
    """Stub `git clone` to materialize a tiny repo, and `git rev-parse`."""
    real_run = subprocess.run

    def fake_run(cmd, *args, **kwargs):
        if cmd[:2] == ["git", "clone"]:
            dest = Path(cmd[-1])
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "model.py").write_text(
                "class TruncatedDiffusion:\n    def forward(self):\n        return self.denoise()\n",  # noqa: E501
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if cmd[:2] == ["git", "rev-parse"]:
            return subprocess.CompletedProcess(cmd, 0, "abc1234def5678\n", "")
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", fake_run)


def test_clone_is_deleted_pointer_survives(tmp_path, monkeypatch):
    clone_root = tmp_path / "repos"
    _fake_git(monkeypatch, clone_root)
    out = tmp_path / "code_ref.md"
    build_code_ref(
        github_repo="https://github.com/x/diffusiondrive",
        innovations=[Innovation(name="Truncated diffusion", grep="TruncatedDiffusion")],
        out_path=out,
        clone_root=clone_root,
        idbase="2411.15139",
    )
    # Pointer exists and is self-contained.
    body = out.read_text(encoding="utf-8")
    assert "https://github.com/x/diffusiondrive" in body
    assert "abc1234def5678" in body  # pinned SHA
    assert "model.py:1" in body  # innovation located to file:line
    # Clone DELETED.
    assert not (clone_root / "2411.15139").exists()


def test_closed_source_writes_stub(tmp_path):
    out = tmp_path / "code_ref.md"
    build_code_ref(
        github_repo=None,
        innovations=[Innovation(name="X", grep="X")],
        out_path=out,
        clone_root=tmp_path / "repos",
        idbase="doi-abcd1234",
    )
    body = out.read_text(encoding="utf-8")
    assert "No public repository" in body
    assert not (tmp_path / "repos").exists() or not any((tmp_path / "repos").iterdir())
