#!/usr/bin/env python
"""Offline spot-check of code_ref repo resolution over the local corpus (P0).

For every `corpus/{ID}_*/` paper, run the OFFLINE candidate cascade (T1 grep of
the frozen MD + T2a Papers-with-Code official table) and print the ordered
candidates — no cloning, no network. Lets a human eyeball resolution accuracy
before/after the P0 change.

Usage (from repo root):
    uv run .claude/skills/paper-landscape/scripts/tools/rescan_code_ref.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parents[2]
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from scripts.output.repo_resolve import (  # noqa: E402
    author_declares_closed,
    resolve_repo_candidates,
)


def main() -> None:
    repo_root = Path.cwd()
    corpus = repo_root / "corpus"
    if not corpus.is_dir():
        print(f"no corpus/ under {repo_root}", file=sys.stderr)
        raise SystemExit(1)

    found = closed = empty = 0
    for paper_dir in sorted(corpus.iterdir()):
        if not paper_dir.is_dir():
            continue
        arxiv_id = paper_dir.name.split("_", 1)[0]
        md = paper_dir / f"{paper_dir.name}.md"
        md_path = md if md.exists() else None
        cands = resolve_repo_candidates(arxiv_id, md_path, {})
        if cands:
            found += 1
            top = cands[0]
            extra = f" (+{len(cands) - 1} more)" if len(cands) > 1 else ""
            print(f"  {arxiv_id:12} → [{top.source}/{top.trust}] {top.url}{extra}")
        elif author_declares_closed(md_path):
            closed += 1
            print(f"  {arxiv_id:12} → author-declared closed-source")
        else:
            empty += 1
            print(f"  {arxiv_id:12} → searched, not found")

    print(f"\n{found} resolved · {closed} declared-closed · {empty} not-found")


if __name__ == "__main__":
    main()
