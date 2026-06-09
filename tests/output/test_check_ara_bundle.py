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
