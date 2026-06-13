from __future__ import annotations

import json
from pathlib import Path

from scripts.status import _idbase, collect


def test_idbase_extracts_arxiv_id_regardless_of_naming_order() -> None:
    # vault key: id is the SUFFIX; corpus dir: id is the PREFIX; scene: bare id.
    assert _idbase("2026-06-13_GenieGenerative_2402.15391") == "2402.15391"
    assert _idbase("2402.15391_GenieGenerative") == "2402.15391"
    assert _idbase("2407.01392") == "2407.01392"


def _seal(ai: Path, *, passes: bool) -> None:
    (ai / "ara").mkdir(parents=True, exist_ok=True)
    (ai / "ara" / "level2_report.json").write_text(
        json.dumps({"overall": {"passes_seal2": passes}}), encoding="utf-8"
    )


def test_collect_classifies_each_state(tmp_path: Path) -> None:
    ws = tmp_path
    # compliant: paired, sealed, report has 评价 + no anchors
    pv = ws / "person_vault" / "2026-01-01_A_1111.11111"
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("# A\n\n## 评价\n> ok\n\n## 摘要\n本文达到 1。", encoding="utf-8")
    _seal(ws / "ai_package" / "2026-01-01_A_1111.11111", passes=True)
    # done-stale (report carries a retired anchor, no 评价)
    pv2 = ws / "person_vault" / "2026-01-01_B_2222.22222"
    pv2.mkdir(parents=True)
    (pv2 / "report.md").write_text(
        "# B\n本文 2<!--ref:r--><!--anchor:quote:2-->。", encoding="utf-8"
    )
    _seal(ws / "ai_package" / "2026-01-01_B_2222.22222", passes=True)
    # done-stale (unsealed: no level2_report)
    pv3 = ws / "person_vault" / "2026-01-01_C_3333.33333"
    pv3.mkdir(parents=True)
    (pv3 / "report.md").write_text("# C\n\n## 评价\n> ok\n", encoding="utf-8")
    (ws / "ai_package" / "2026-01-01_C_3333.33333" / "ara").mkdir(parents=True)
    # failed scene
    fs = ws / "_failed" / "2026-01-01_D_4444.44444"
    fs.mkdir(parents=True)
    (fs / "scene.json").write_text("{}", encoding="utf-8")
    # ingested only (corpus dir, id is the PREFIX)
    (ws / "corpus" / "5555.55555_E").mkdir(parents=True)

    recs = {r["idbase"]: r for r in collect(ws)}
    assert recs["1111.11111"]["state"] == "compliant"
    assert (
        recs["2222.22222"]["state"] == "done-stale"
        and "stale-report" in recs["2222.22222"]["detail"]
    )
    assert (
        recs["3333.33333"]["state"] == "done-stale"
        and recs["3333.33333"]["detail"] == "unsealed-ARA"
    )
    assert recs["4444.44444"]["state"] == "failed"
    assert recs["5555.55555"]["state"] == "ingested"
