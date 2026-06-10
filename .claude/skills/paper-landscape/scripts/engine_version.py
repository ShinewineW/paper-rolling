"""现场记录引擎版本——仅供人工 triage 诊断,不参与复用判定（ADR-0007 修订）。"""

from __future__ import annotations

import subprocess
from pathlib import Path


def current_commit(workspace: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return out.stdout.strip() or "unknown"
    except (subprocess.SubprocessError, OSError):
        return "unknown"
