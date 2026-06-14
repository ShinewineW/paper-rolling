from __future__ import annotations

import json
from pathlib import Path

from scripts.demote import _candidate_from_paper, demote_to_scene


class _FakeLedger:
    """最小账本替身:只记录 record() 调用(demote 用 _candidate_key 还原键,不查账本)。"""

    def __init__(self) -> None:
        self.recorded: list[dict] = []

    def record(self, key: str, **kw) -> None:
        self.recorded.append({"key": key, **kw})


def _publish(
    tmp_path: Path, idbase: str, name: str, *, doi: str | None = None, version: str = ""
) -> None:
    full = f"2026-06-14_{name}_{idbase}"
    ara = tmp_path / "ai_package" / full / "ara"
    ara.mkdir(parents=True)
    doi_line = f"doi: {doi}\n" if doi else f"doi: arXiv:{idbase}\n"
    (ara / "PAPER.md").write_text(
        f"---\nkey: '{idbase}'\ntitle: {name}\nyear: 2024\nauthors:\n- A. Author\n"
        f"{doi_line}---\n# x\n",
        encoding="utf-8",
    )
    (ara / "src").mkdir()
    (ara / "src" / "code_ref.md").write_text("# Code Reference\n", encoding="utf-8")
    pv = tmp_path / "person_vault" / full
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("# r\n\n## 评价\n> ok\n", encoding="utf-8")
    cdir = f"{idbase}{version}_{name}"  # ingest 口径:arXiv 带版本 → {id}{version}_{Name}
    corpus = tmp_path / "corpus" / cdir
    corpus.mkdir(parents=True)
    (corpus / f"{cdir}.md").write_text("# paper md\n", encoding="utf-8")
    (corpus / "content_list.json").write_text("[]", encoding="utf-8")


def test_demote_moves_products_to_branch2_scene_and_records_deferred(tmp_path: Path) -> None:
    _publish(tmp_path, "1111.11111", "Foo")
    led = _FakeLedger()

    demote_to_scene(
        tmp_path, "1111.11111", ledger=led, category="读错论文", reason="正文讲的是另一篇"
    )

    # 现场建立 + branch2 根(现场名 = vault key,同 _g3_to_scene 约定)
    scene = tmp_path / "_failed" / "2026-06-14_Foo_1111.11111"
    manifest = json.loads((scene / "scene.json").read_text(encoding="utf-8"))
    assert manifest["failed_gate"] == "结构门"
    assert manifest["findings"][0]["target"] == "ara"
    assert "读错论文" in manifest["findings"][0]["observation"]
    # 产物被收进现场(ai/ara + person/report)、原 vault 已清空
    assert (scene / "ai" / "ara" / "PAPER.md").exists()
    assert (scene / "person" / "report.md").exists()
    assert not (tmp_path / "ai_package" / "2026-06-14_Foo_1111.11111").exists()
    assert not (tmp_path / "person_vault" / "2026-06-14_Foo_1111.11111").exists()
    # candidate 带齐 write_branch2._paper_md 需要的字段(title/year 是必填下标)
    cand = manifest["candidate"]
    assert cand["arxiv_id"] == "1111.11111"
    assert cand["year"] == 2024
    assert cand["title"] == "Foo"
    assert cand["authors"] == ["A. Author"]
    # 账本记 deferred(无 TTL,等复活赛);键 = _candidate_key(candidate)
    assert led.recorded == [
        {
            "key": "1111.11111",
            "status": "deferred",
            "failure_class": "audit_block",
            "retry_after": None,
        }
    ]


def test_demote_doi_only_records_under_safe_keyed_ledger_key(tmp_path: Path) -> None:
    # B2:DOI-only 产物记账本须用 _candidate_key(safe-keyed 裸 DOI),不是 doi-hash idbase。
    _publish(tmp_path, "doi-1a2b3c4d", "Qux", doi="10.1234/qux")
    led = _FakeLedger()
    demote_to_scene(tmp_path, "doi-1a2b3c4d", ledger=led, category="整体胡说", reason="编的")
    assert led.recorded[0]["key"] == "10.1234_qux"  # 同 hub._candidate_key


def test_demote_finds_versioned_corpus_md(tmp_path: Path) -> None:
    # B1(R6):arXiv 带版本的 corpus(`{id}v2_Name`)也要能被找到,否则 FAIL 路径起不来。
    _publish(tmp_path, "2401.00001", "Foo", version="v2")
    led = _FakeLedger()
    scene = demote_to_scene(tmp_path, "2401.00001", ledger=led, category="读错论文", reason="x")
    assert (scene / "scene.json").exists()
    assert led.recorded[0]["key"] == "2401.00001"


def test_demote_raises_when_product_missing(tmp_path: Path) -> None:
    import pytest

    led = _FakeLedger()
    with pytest.raises(FileNotFoundError):
        demote_to_scene(tmp_path, "9999.99999", ledger=led, category="整体胡说", reason="x")


def test_demote_candidate_doi_only_keeps_arxiv_id_none(tmp_path: Path) -> None:
    # Final 轮:DOI-only 产物不得把裸 DOI 放进 arxiv_id(identity_base 会把任何非空 arxiv_id
    # 当身份基 → 复活改键)。也确认 year 被还原(write_branch2 必填)。
    full = "2026-06-14_Qux_doi-1a2b3c4d"
    ara = tmp_path / "ai_package" / full / "ara"
    ara.mkdir(parents=True)
    (ara / "PAPER.md").write_text(
        "---\nkey: 'doi-1a2b3c4d'\ntitle: Qux\nyear: 2023\ndoi: 10.1234/qux\n---\n# x\n",
        encoding="utf-8",
    )
    c = _candidate_from_paper(ara)
    assert c["arxiv_id"] is None
    assert c["doi"] == "10.1234/qux"
    assert c["year"] == 2023


def test_demote_synthesizes_content_list_when_corpus_lacks_it(tmp_path: Path) -> None:
    # F3:corpus 缺 content_list.json 的产物也必须降级出带 content_list.json 的现场
    # (复活赛 G3 的 equation 门要读它),并就地补回 corpus。
    _publish(tmp_path, "2222.22222", "Bar")
    (tmp_path / "corpus" / "2222.22222_Bar" / "content_list.json").unlink()
    led = _FakeLedger()
    scene = demote_to_scene(tmp_path, "2222.22222", ledger=led, category="整体胡说", reason="编的")
    assert (scene / "content_list.json").exists()
    assert (tmp_path / "corpus" / "2222.22222_Bar" / "content_list.json").exists()


def test_demote_preserves_products_under_failed_if_write_scene_raises(
    tmp_path: Path, monkeypatch
) -> None:
    # F2 数据安全:write_scene 在 move 之后抛错时,产物必须留存于 _failed/(可恢复),
    # 绝不被 finally 清理删掉;ledger 不前进(record 仅在 write_scene 成功后执行)。
    import pytest

    _publish(tmp_path, "3333.33333", "Baz")
    led = _FakeLedger()

    def _boom(**kw):
        raise RuntimeError("write_scene blew up after the moves")

    monkeypatch.setattr("scripts.demote.write_scene", _boom)
    with pytest.raises(RuntimeError):
        demote_to_scene(tmp_path, "3333.33333", ledger=led, category="重写级", reason="x")
    assert not (tmp_path / "ai_package" / "2026-06-14_Baz_3333.33333").exists()
    survivors = list((tmp_path / "_failed").rglob("PAPER.md"))
    assert survivors, "products must survive under _failed/ when write_scene fails"
    assert led.recorded == []
