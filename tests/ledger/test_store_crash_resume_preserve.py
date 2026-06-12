# tests/ledger/test_store_crash_resume_preserve.py
from scripts.ledger.store import Ledger


def test_crash_resume_preserves_ai_ara(tmp_path):
    led = Ledger(tmp_path)
    ai = tmp_path / "ai_package" / "k1"
    (ai / "ara").mkdir(parents=True)
    (ai / "ara" / "PAPER.md").write_text("x", encoding="utf-8")
    # 非 done 行，记录了 ai_package_path
    led.record_status("k1", status="analyzed", ai_package_path=str(ai))
    led.crash_resume_sweep()
    assert not ai.exists()
    assert (tmp_path / "_failed" / "_orphans" / "k1" / "ara" / "PAPER.md").exists()


def test_crash_resume_deletes_person_path(tmp_path):
    led = Ledger(tmp_path)
    person = tmp_path / "person_vault" / "k2"
    person.mkdir(parents=True)
    (person / "report.md").write_text("r", encoding="utf-8")
    led.record_status("k2", status="analyzed", person_vault_path=str(person))
    led.crash_resume_sweep()
    assert not person.exists()  # 廉价 → 仍删
