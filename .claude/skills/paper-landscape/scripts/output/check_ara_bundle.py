"""ARA bundle regression gate (审计 §6.1) — guard the P0/P1 fixes from rotting.

Asserts, per produced ARA bundle (the `ara/` dir under an `ai_package/{key}/`):

  1. **code_ref three-state** — `src/code_ref.md` exists and is one of the valid
     states (found / searched-not-found / author-declared-closed / unreachable),
     NEVER the retired `None→"closed-source paper"` mislabel, and NEVER asserts
     closed-source outside the explicit author-declared state (P0).
  2. **evidence tables non-empty** — `evidence/tables/` has at least one table, i.e.
     the substantive numeric evidence is present.
  3. **no review↔tables drift** — `level2_report.json` must not claim the evidence
     tables are missing while `evidence/tables/` is non-empty (P1-b).

Scope note: the P1-a figure-caption-index wiring is regression-guarded by the test
suite (tests/output/test_branch2.py — branch2 indexes figures when the MD has
them), NOT here: figure presence is paper-dependent (a genuinely figureless paper
is legitimate), so "must have a Figures section" is not a sound per-bundle assertion.

`check_bundle(ara_dir)` returns a list of violation strings ([] = pass). The CLI
sweeps `ai_package/*/ara` (or given paths) and exits non-zero on any violation:

    PYTHONPATH=.claude/skills/paper-landscape \
        uv run python -m scripts.output.check_ara_bundle [ara_dir ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# The retired P0 mislabel — its presence means code_ref regressed to "absence ==
# closed-source". The new not-found state says "...NOT a closed-source", which does
# NOT contain this exact substring, so the check is precise.
_RETIRED_MISLABEL = "closed-source paper"

# The ONLY legitimate lower-cased 'closed-source' mentions across the engine's
# renders: the author-declared state header and the not-found disclaimer. Stripping
# these, any residual 'closed-source' is an illegitimate assertion (P0).
_CLOSED_OK = re.compile(r"author-declared closed-source|not a closed-source")

# A recognized three-state (or unreachable) pointer carries one of these markers.
# The found state is identified by EITHER marker: "**Pinned commit**" is always present
# (repo + SHA), while "## Innovation → code location" is now OMITTED when no innovation
# resolves to source (honesty: no fabricated/_not found_ table). Accept both so a found
# pointer is recognized whether or not the innovation map is present.
_VALID_MARKERS = (
    "**Pinned commit**",  # found — repo + SHA (innovation map may be omitted)
    "## Innovation → code location",  # found — innovation map present
    "No public repository found",  # searched, not found
    "Author-declared closed-source",  # author-declared closed
    "unavailable — clone failed",  # declared repo unreachable
)

# Innovation→location honesty (Codex R1). The honest renderer OMITS unresolved rows and
# cites SOURCE files only; a shipped file still carrying the retired fabricated-map form
# — a literal "_not found_" cell, or a Location pointing at prose/docs (README.md:20,
# *.rst, AGENTS.md) instead of source — is a regression a green gate must NOT let pass.
_NOT_FOUND_ROW = "_not found_"
_LOC_CELL = re.compile(r"\|\s*([^|]+?:\d+)\s*\|")  # a `path:line` Location cell in a table row
_DOC_EXT = (".md", ".rst", ".txt", ".yaml", ".yml", ".cfg", ".ini", ".toml", ".json", ".csv")

# level2 text claiming the tables/numbers are absent (P1-b drift), lower-cased match.
# Covers the family of "tables are only descriptions / metadata / not included / no
# real numbers" phrasings a reviewer uses when it was fed the index but not the tables.
_DRIFT = re.compile(
    r"only a[a-z ]*index"
    r"|not included in the bundle"
    r"|tables?[^.]{0,40}\bnot (?:included|present)"
    r"|evidence tables?[^.]{0,40}(?:missing|absent)"
    r"|no actual (?:numeric|numerical)"
    r"|only (?:the )?(?:metadata|table descriptions)"
    r"|only (?:contains?|provides?|includes?|has) (?:the )?(?:table )?descriptions"
    r"|only (?:contains?|provides?|includes?|has) (?:table )?metadata"
)


def _has_table(tables_dir: Path) -> bool:
    return tables_dir.is_dir() and any(tables_dir.glob("*.md"))


def check_bundle(ara_dir: Path) -> list[str]:
    """Return regression violations for one ARA bundle ([] = clean)."""
    ara = Path(ara_dir)
    violations: list[str] = []

    code_ref = ara / "src" / "code_ref.md"
    if not code_ref.is_file():
        violations.append("missing src/code_ref.md")
    else:
        text = code_ref.read_text(encoding="utf-8", errors="ignore")
        low = text.lower()
        if _RETIRED_MISLABEL in low:
            violations.append("code_ref.md uses the retired None→closed-source mislabel (P0)")
        elif "closed-source" in _CLOSED_OK.sub("", low):
            # The ONLY legitimate 'closed-source' mentions are the author-declared
            # state header and the not-found state's "...NOT a closed-source"
            # disclaimer. Strip those; ANY remaining 'closed-source' anywhere in the
            # file is an illegitimate assertion (P0) — robust to a file mixing the
            # legit disclaimer with a later bad claim.
            violations.append(
                "code_ref.md asserts closed-source outside the author-declared state (P0)"
            )
        elif not any(marker in text for marker in _VALID_MARKERS):
            violations.append("code_ref.md is not a recognized three-state pointer")
        if _NOT_FOUND_ROW in text:
            violations.append(
                "code_ref.md innovation table carries '_not found_' rows (retired "
                "fabricated-map form; the honest renderer omits unresolved rows)"
            )
        bad_locs = sorted(
            {
                loc
                for loc in _LOC_CELL.findall(text)
                if loc.rsplit(":", 1)[0].strip().lower().endswith(_DOC_EXT)
            }
        )
        if bad_locs:
            violations.append(
                "code_ref.md innovation location(s) point at non-source files "
                f"(prose/docs, not code): {', '.join(bad_locs)}"
            )

    tables = ara / "evidence" / "tables"
    has_table = _has_table(tables)
    if not has_table:
        violations.append("evidence/tables/ is empty (no substantive numeric evidence)")

    level2 = ara / "level2_report.json"
    if level2.is_file() and has_table:
        blob = level2.read_text(encoding="utf-8", errors="ignore").lower()
        if _DRIFT.search(blob):
            violations.append(
                "level2_report claims evidence tables missing, but evidence/tables/ "
                "is non-empty (P1-b review↔product drift)"
            )
    return violations


def _iter_targets(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    return sorted(Path.cwd().glob("ai_package/*/ara"))


def main(argv: list[str] | None = None) -> int:
    targets = _iter_targets(list(argv if argv is not None else sys.argv[1:]))
    if not targets:
        print("no ARA bundles found (pass an ara/ dir or run from a workspace root)")
        return 0
    total = 0
    for ara in targets:
        violations = check_bundle(ara)
        if violations:
            total += len(violations)
            print(f"✗ {ara}")
            for v in violations:
                print(f"    - {v}")
        else:
            print(f"✓ {ara}")
    print(f"\n{len(targets)} bundle(s), {total} violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
