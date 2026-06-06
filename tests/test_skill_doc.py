# tests/test_skill_doc.py
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "paper-landscape" / "SKILL.md"


def test_skill_md_exists():
    assert SKILL.exists()


def test_documents_campaign_hard_gate():
    text = SKILL.read_text(encoding="utf-8")
    assert "Hard Gate" in text
    assert "config/campaign.yaml" in text
    # First-time confirm topic + N; /loop tick reads config, no re-gate.
    assert "/loop" in text
    assert "no re-gate" in text.lower() or "不 re-gate" in text


def test_documents_full_pipeline_order():
    text = SKILL.read_text(encoding="utf-8")
    for stage in ["discover", "ingest", "ledger", "branch2", "branch1", "G2", "G3", "landscapes"]:
        assert stage in text, f"pipeline stage missing from SKILL.md: {stage}"


def test_documents_zero_mid_pipeline_questions_must():
    text = SKILL.read_text(encoding="utf-8")
    assert "MUST" in text
    assert "mid-pipeline" in text.lower() or "中段" in text


def test_documents_loop_daily_usage():
    text = SKILL.read_text(encoding="utf-8")
    assert "/loop" in text and ("daily" in text.lower() or "每天" in text or "日更" in text)
