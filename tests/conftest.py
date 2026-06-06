# tests/conftest.py
"""Pytest bootstrap: put the skill ROOT on sys.path so the `scripts` package
imports resolve (`import scripts.paths`, `from scripts.discovery... import ...`)
without an install. Round 2 F1: the canonical namespace is `scripts.*`, so the
skill root (parent of `scripts/`) goes on the path — NOT the `scripts/` dir.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".claude" / "skills" / "paper-landscape"

if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))
