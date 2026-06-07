# .claude/skills/paper-landscape/scripts/preflight.py
"""Environment preflight — verify the local machine has EVERY external
prerequisite the engine needs BEFORE a campaign runs, so a missing tool is a
loud STOP, never a silent per-paper skip.

Checks (all REQUIRED):
  - python:requests / python:pyyaml — runtime deps (uv run auto-syncs these).
  - pandoc — Tier-1 ingest (arXiv-HTML -> Markdown).
  - mineru — Tier-2 ingest (PDF -> Markdown).

NOT preflighted (no install / no silent-failure surface): the four LLM seams are
agent-provided; the HF token ships in source (anonymous fallback otherwise);
OpenAlex / Semantic Scholar / arXiv / DBLP are anonymous public APIs.

Stdlib-only (no third-party imports) so it runs and REPORTS even when the runtime
deps themselves are missing.

CLI: `python -m scripts.preflight` -> prints a report; exit 0 if all present,
exit 1 if any required prerequisite is missing (with its fix command).
"""

from __future__ import annotations

import importlib.util
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    """One prerequisite's status + the command to fix it if missing."""

    name: str
    ok: bool
    detail: str
    fix: str


def _has_module(mod: str) -> bool:
    """True if `mod` is importable, without importing it."""
    return importlib.util.find_spec(mod) is not None


def check_environment() -> list[Check]:
    """Return one Check per REQUIRED prerequisite (order = report order)."""
    checks: list[Check] = []

    for mod, pkg in (("requests", "requests"), ("yaml", "pyyaml")):
        present = _has_module(mod)
        checks.append(
            Check(
                name=f"python:{pkg}",
                ok=present,
                detail="importable" if present else f"missing module {mod!r}",
                fix="uv sync",
            )
        )

    pandoc = shutil.which("pandoc")
    checks.append(
        Check(
            name="pandoc",
            ok=pandoc is not None,
            detail=pandoc or "not on PATH",
            fix="brew install pandoc  (or a GitHub release binary)",
        )
    )

    mineru = shutil.which("mineru")
    checks.append(
        Check(
            name="mineru",
            ok=mineru is not None,
            detail=mineru or "not on PATH",
            fix='uv pip install -U "mineru[core]"',
        )
    )

    return checks


def all_ok(checks: list[Check]) -> bool:
    """True iff every required prerequisite is present."""
    return all(c.ok for c in checks)


def format_report(checks: list[Check]) -> str:
    """Human-readable PASS/MISS report; names the fix for each missing item."""
    lines = ["paper-landscape preflight (all prerequisites are REQUIRED):"]
    for c in checks:
        mark = "OK  " if c.ok else "MISS"
        lines.append(f"  [{mark}] {c.name}: {c.detail}")
        if not c.ok:
            lines.append(f"         fix: {c.fix}")
    lines.append(
        "ALL PRESENT — safe to proceed."
        if all_ok(checks)
        else "MISSING PREREQUISITES — install the above, then re-run. DO NOT proceed."
    )
    return "\n".join(lines)


def _main() -> int:
    checks = check_environment()
    print(format_report(checks))
    return 0 if all_ok(checks) else 1


if __name__ == "__main__":
    import sys

    sys.exit(_main())
