"""ARA bundle regression gate (审计 §6.1): code_ref three-state, tables, drift."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.output.branch2_ara import write_branch2
from scripts.output.check_ara_bundle import check_bundle


def _bundle(tmp_path: Path, *, code_ref: str, tables: dict[str, str], level2: dict | None = None):
    ara = tmp_path / "ara"
    (ara / "src").mkdir(parents=True)
    (ara / "src" / "code_ref.md").write_text(code_ref, encoding="utf-8")
    tdir = ara / "evidence" / "tables"
    tdir.mkdir(parents=True)
    for name, body in tables.items():
        (tdir / name).write_text(body, encoding="utf-8")
    if level2 is not None:
        (ara / "level2_report.json").write_text(json.dumps(level2), encoding="utf-8")
    return ara


_FOUND = "# Code Reference\n\n- **Repository**: x\n\n## Innovation → code location\n"
_NOT_FOUND = "# Code Reference\n\n**No public repository found** — ... NOT a closed-source ...\n"
_RETIRED = "# Code Reference\n\n**No public repository** — closed-source paper; ...\n"


def test_clean_bundle_passes(tmp_path):
    ara = _bundle(tmp_path, code_ref=_FOUND, tables={"t1.md": "| a |\n|---|\n| 1 |\n"})
    assert check_bundle(ara) == []


def test_retired_mislabel_flagged(tmp_path):
    ara = _bundle(tmp_path, code_ref=_RETIRED, tables={"t1.md": "x\n"})
    assert any("retired" in v for v in check_bundle(ara))


def test_unrecognized_code_ref_flagged(tmp_path):
    ara = _bundle(
        tmp_path, code_ref="# Code Reference\n\nsomething else\n", tables={"t1.md": "x\n"}
    )
    assert any("not a recognized three-state" in v for v in check_bundle(ara))


def test_empty_tables_flagged(tmp_path):
    ara = _bundle(tmp_path, code_ref=_NOT_FOUND, tables={})
    assert any("evidence/tables/ is empty" in v for v in check_bundle(ara))


def test_review_table_drift_flagged(tmp_path):
    # P1-b regression guard: level2 says tables missing while tables/ is non-empty.
    level2 = {
        "findings": [
            {
                "observation": "The bundle does not contain the actual evidence tables "
                "(Table 2-6); only a descriptive index is present."
            }
        ]
    }
    ara = _bundle(
        tmp_path, code_ref=_FOUND, tables={"t1.md": "| a |\n|---|\n| 1 |\n"}, level2=level2
    )
    assert any("drift" in v for v in check_bundle(ara))


def test_no_drift_when_level2_clean(tmp_path):
    level2 = {"findings": [{"observation": "Evidence tables substantively support the claims."}]}
    ara = _bundle(tmp_path, code_ref=_FOUND, tables={"t1.md": "x\n"}, level2=level2)
    assert check_bundle(ara) == []


def test_freshly_produced_bundle_passes_gate(tmp_path, candidate, analysis):
    # Integration: the engine's own branch2 output must satisfy the regression gate
    # (locks code_ref three-state + tables present against future regressions).
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    assert check_bundle(ara) == []


_CLOSED_VARIANT = (
    "# Code Reference\n\n**No public repository found** — treating this as closed-source\n"
)


def test_closed_source_assertion_outside_author_declared_flagged(tmp_path):
    # Codex Round 1: a not-found pointer that still asserts closed-source (in any
    # wording, not just the exact retired phrase) must be flagged (P0).
    ara = _bundle(tmp_path, code_ref=_CLOSED_VARIANT, tables={"t1.md": "x\n"})
    assert any("asserts closed-source" in v for v in check_bundle(ara))


def test_valid_states_do_not_trip_closed_source_guard(tmp_path):
    # The legitimate not-found ("NOT a closed-source") and author-declared states
    # both mention 'closed-source' and must NOT be flagged.
    declared = "# Code Reference\n\n**Author-declared closed-source** — the paper states...\n"
    for i, cr in enumerate((_NOT_FOUND, declared)):
        ara = _bundle(tmp_path / f"b{i}", code_ref=cr, tables={"t1.md": "x\n"})
        assert check_bundle(ara) == []


_COMBO_BYPASS = (
    "# Code Reference\n\n**No public repository found** ... NOT a closed-source claim ... "
    "treating the implementation as closed-source.\n"
)


def test_closed_source_combo_bypass_flagged(tmp_path):
    # Codex Round 2: a file mixing the legit "NOT a closed-source" disclaimer with a
    # later bad "...as closed-source" assertion must still be flagged (whole-file
    # substring exceptions were insufficient).
    ara = _bundle(tmp_path, code_ref=_COMBO_BYPASS, tables={"t1.md": "x\n"})
    assert any("asserts closed-source" in v for v in check_bundle(ara))


_NOT_FOUND_ROWS = (
    "# Code Reference\n\n- **Repository**: x\n- **Pinned commit**: `abc`\n\n"
    "## Innovation → code location\n\n| Innovation | Location (`file:line`) |\n|---|---|\n"
    "| foo | model.py:10 |\n| bar | _not found_ |\n"
)
_DOC_LOCATIONS = (
    "# Code Reference\n\n- **Repository**: x\n- **Pinned commit**: `abc`\n\n"
    "## Innovation → code location\n\n| Innovation | Location (`file:line`) |\n|---|---|\n"
    "| foo | README.md:20 |\n| bar | docs/api.rst:5 |\n"
)
_REAL_SOURCE_LOCATIONS = (
    "# Code Reference\n\n- **Repository**: x\n- **Pinned commit**: `abc`\n\n"
    "## Innovation → code location\n\n| Innovation | Location (`file:line`) |\n|---|---|\n"
    "| foo | src/model.py:10 |\n| bar | train.py:42 |\n"
)


def test_not_found_rows_flagged(tmp_path):
    # Codex R1: a stale shipped file still carrying the retired '_not found_' table form
    # (the two reverted papers) must be flagged — the gate gap that let it pass green.
    ara = _bundle(tmp_path, code_ref=_NOT_FOUND_ROWS, tables={"t1.md": "x\n"})
    assert any("_not found_" in v for v in check_bundle(ara))


def test_non_source_innovation_location_flagged(tmp_path):
    # Codex R1: a Location pointing at prose/docs (README.md:20, *.rst) is dishonest —
    # the honest renderer cites SOURCE only. Both bad locations are surfaced.
    vs = check_bundle(_bundle(tmp_path, code_ref=_DOC_LOCATIONS, tables={"t1.md": "x\n"}))
    assert any("non-source" in v and "README.md:20" in v and "docs/api.rst:5" in v for v in vs)


def test_real_source_locations_pass(tmp_path):
    # A genuine found pointer whose Locations are real source files passes cleanly.
    ara = _bundle(tmp_path, code_ref=_REAL_SOURCE_LOCATIONS, tables={"t1.md": "x\n"})
    assert check_bundle(ara) == []


def test_drift_catches_descriptions_and_no_numbers_phrasings(tmp_path):
    # Codex Round 5: reviewer phrasings the narrow regex missed — "only ... table
    # descriptions" and "only metadata with no actual numerical data".
    for i, obs in enumerate(
        [
            "The evidence bundle only contains table descriptions, not the data.",
            "These evidence files are only metadata with no actual numerical data.",
        ]
    ):
        ara = _bundle(
            tmp_path / f"d{i}",
            code_ref=_FOUND,
            tables={"t1.md": "| a |\n|---|\n| 1 |\n"},
            level2={"findings": [{"observation": obs}]},
        )
        assert any("drift" in v for v in check_bundle(ara)), obs
