from __future__ import annotations

import json
from pathlib import Path

from scripts.output.final_review import (
    is_reviewed,
    read_marker,
    unreviewed_compliant_keys,
    write_marker,
)


def _ara(tmp_path: Path, entry: str) -> Path:
    ara = tmp_path / "ai_package" / entry / "ara"
    ara.mkdir(parents=True)
    return ara


def test_write_then_read_marker_roundtrips(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_X_1111.11111")
    write_marker(ara, verdict="revised", edits=["report.md: 清掉思维链残留"], date="2026-06-14")
    assert is_reviewed(ara) is True
    m = read_marker(ara)
    assert m["verdict"] == "revised"
    assert m["by"] == "main-session-opus"
    assert m["date"] == "2026-06-14"
    assert m["edits"] == ["report.md: 清掉思维链残留"]
    # 落盘文件就在 ara/final_review.json
    data = json.loads((ara / "final_review.json").read_text(encoding="utf-8"))
    assert data["verdict"] == "revised"


def test_clean_marker_has_no_edits(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Y_2222.22222")
    write_marker(ara, verdict="clean", edits=[], date="2026-06-14")
    assert read_marker(ara)["verdict"] == "clean"
    assert read_marker(ara)["edits"] == []


def test_is_reviewed_false_when_absent(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Z_3333.33333")
    assert is_reviewed(ara) is False
    assert read_marker(ara) is None


def test_is_reviewed_false_for_empty_or_invalid_marker(tmp_path: Path) -> None:
    # 非阻断:{}/verdict 非法/非 dict 的 marker 不得算"已终审"(坏写入不能永久跳过该篇)。
    ara = _ara(tmp_path, "2026-06-14_V_7777.77777")
    for bad in ("{}", '{"verdict": "bogus"}', "[]", "[1, 2]"):
        (ara / "final_review.json").write_text(bad, encoding="utf-8")
        assert is_reviewed(ara) is False
    # 非 dict JSON 经 read_marker 归一为 None(is_reviewed 不会对 list 调 .get → 不崩)
    assert read_marker(ara) is None


def test_write_marker_rejects_unknown_verdict(tmp_path: Path) -> None:
    import pytest

    ara = _ara(tmp_path, "2026-06-14_W_4444.44444")
    with pytest.raises(ValueError, match="verdict"):
        write_marker(ara, verdict="failed", edits=[], date="2026-06-14")  # FAIL 不写 marker


def test_unreviewed_compliant_keys_filters(tmp_path: Path, monkeypatch) -> None:
    # 批次 = 合规、且没有 final_review.json 的已发布产物。
    # compliant 判定打桩(避免在本单测里铺一整套 report/seal 夹具)。
    import scripts.output.final_review as fr

    compliant = {"1111.11111", "5555.55555"}  # 这两篇合规;6666 不合规
    monkeypatch.setattr(fr, "_compliant_idbases", lambda ws: compliant)
    _ara(tmp_path, "2026-06-14_A_1111.11111")  # 合规 + 无 marker  -> 入批
    b = _ara(tmp_path, "2026-06-14_B_5555.55555")  # 合规 + 有 marker -> 跳过
    write_marker(b, verdict="clean", edits=[], date="2026-06-14")
    _ara(tmp_path, "2026-06-14_C_6666.66666")  # 不合规 -> 不入批
    assert unreviewed_compliant_keys(tmp_path) == ["1111.11111"]
