"""Anchor lint CLI: exit 0 clean, exit 1 on violation."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Round 3 F1: non-pytest `python -m scripts.*` invocations need the skill root
# on PYTHONPATH (the pytest pythonpath/conftest bootstrap does not reach a
# subprocess). The skill root is the parent of the `scripts/` package.
_SKILL_ROOT = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "paper-landscape"


def _run(path: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(_SKILL_ROOT)}
    return subprocess.run(
        [sys.executable, "-m", "scripts.output.anchor_lint", str(path)],
        capture_output=True,
        text=True,
        env=env,
    )


def test_cli_exit_0_on_clean(tmp_path):
    f = tmp_path / "ok.md"
    f.write_text("达到 0.61 NDS<!--ref:nds--><!--anchor:page:7-->。\n", encoding="utf-8")
    r = _run(f)
    assert r.returncode == 0, r.stderr


def test_cli_exit_1_on_violation(tmp_path):
    f = tmp_path / "bad.md"
    f.write_text("提升 5 个百分点<!--ref:gain-->。\n", encoding="utf-8")
    r = _run(f)
    assert r.returncode == 1
    assert "without trailing anchor" in r.stderr
