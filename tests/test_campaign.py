# tests/test_campaign.py
from pathlib import Path

import pytest
from scripts.campaign import (
    CampaignConfig,
    GateError,
    gate_needed,
    load_campaign,
    write_campaign,
)


def test_first_time_gate_needed_when_no_config(tmp_path: Path):
    # No config file yet → campaign gate MUST fire (first-time HITL confirm).
    assert load_campaign(tmp_path) is None
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None) is True


def test_write_then_load_roundtrips(tmp_path: Path):
    cfg = CampaignConfig(
        topic="end-to-end autonomous driving trajectory prediction",
        n_per_tick=5,
        is_ad_domain=True,
    )
    write_campaign(tmp_path, cfg)
    loaded = load_campaign(tmp_path)
    assert loaded == cfg
    assert (tmp_path / "config" / "campaign.yaml").exists()


def test_loop_tick_does_not_regate(tmp_path: Path):
    # After campaign established, a /loop tick (no new topic/N) reads config and
    # does NOT re-gate — autonomous (吸收-D4).
    write_campaign(tmp_path, CampaignConfig(topic="topic alpha", n_per_tick=3, is_ad_domain=False))
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None) is False


def test_changing_topic_or_n_regates(tmp_path: Path):
    # Only changing topic / N re-fires the gate (中枢-D1).
    write_campaign(tmp_path, CampaignConfig(topic="topic alpha", n_per_tick=3, is_ad_domain=False))
    assert gate_needed(tmp_path, requested_topic="different topic beta", requested_n=None) is True
    assert gate_needed(tmp_path, requested_topic=None, requested_n=7) is True
    assert gate_needed(tmp_path, requested_topic="topic alpha", requested_n=3) is False


def test_vague_topic_rejected(tmp_path: Path):
    # "不容模糊" — a vague single-word topic is rejected at gate time (中枢-D1).
    with pytest.raises(GateError, match="too vague"):
        CampaignConfig(topic="自动驾驶", n_per_tick=5, is_ad_domain=True)


def test_nonpositive_n_rejected(tmp_path: Path):
    with pytest.raises(GateError, match="must be a positive"):
        CampaignConfig(topic="some sufficiently specific topic", n_per_tick=0, is_ad_domain=False)
