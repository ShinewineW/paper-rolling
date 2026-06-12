# tests/ledger/test_store_consistency_preserve.py
from scripts.ledger.store import Ledger


def _make_ai_orphan(ws, name, *, with_ara):
    entry = ws / "ai_package" / name
    if with_ara:
        (entry / "ara").mkdir(parents=True)
        (entry / "ara" / "PAPER.md").write_text("x", encoding="utf-8")
    else:
        entry.mkdir(parents=True)  # 空壳
    return entry


def test_orphan_ai_with_ara_moved_not_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = _make_ai_orphan(tmp_path, "2026-06-12_T_2509.1", with_ara=True)
    # 无任何 done 行 → 它是孤儿
    led.consistency_check()
    assert not entry.exists(), "orphan must leave the vault"
    moved = tmp_path / "_failed" / "_orphans" / "2026-06-12_T_2509.1"
    assert (moved / "ara" / "PAPER.md").exists(), "ARA must be preserved, not deleted"


def test_orphan_empty_ai_still_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = _make_ai_orphan(tmp_path, "2026-06-12_T_2509.2", with_ara=False)
    led.consistency_check()
    assert not entry.exists()
    assert not (tmp_path / "_failed" / "_orphans" / "2026-06-12_T_2509.2").exists()


def test_orphan_person_vault_still_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = tmp_path / "person_vault" / "2026-06-12_T_2509.3"
    (entry / "report.md").parent.mkdir(parents=True)
    (entry / "report.md").write_text("r", encoding="utf-8")
    led.consistency_check()
    assert not entry.exists(), "person_vault orphan is cheap → still hard-deleted"
