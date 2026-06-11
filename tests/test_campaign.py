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


def test_shipped_template_loads_with_runtime_schema(tmp_path: Path):
    # Regression (Codex Round-4 reject): the shipped config/campaign.yaml.example
    # MUST use the exact schema load_campaign reads (topic / n_per_tick /
    # is_ad_domain). The original template used `per_round_count` (+ no
    # is_ad_domain), so load_campaign KeyError'd on the real file — an
    # uncontrolled crash instead of the recoverable Hard Gate. Copy the shipped
    # template in as the live config and confirm it loads cleanly.
    import shutil

    import scripts.paths as paths

    template = paths.repo_root() / "config" / "campaign.yaml.example"
    assert template.exists(), "shipped template config/campaign.yaml.example missing"
    (tmp_path / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy(template, tmp_path / "config" / "campaign.yaml")

    cfg = load_campaign(tmp_path)  # must NOT raise KeyError on the shipped schema
    assert cfg is not None
    assert cfg.topic
    assert isinstance(cfg.n_per_tick, int) and cfg.n_per_tick > 0
    assert isinstance(cfg.is_ad_domain, bool)


def test_campaign_config_auto_discover_defaults_true_and_round_trips(tmp_path):
    from scripts.campaign import CampaignConfig, load_campaign, write_campaign

    # Default preserves current behavior.
    cfg = CampaignConfig(topic="world model survey", n_per_tick=5, is_ad_domain=True)
    assert cfg.auto_discover is True

    # list-mode value survives a write→load round trip.
    listed = CampaignConfig(
        topic="my reading list on world models",
        n_per_tick=5,
        is_ad_domain=True,
        force_include=[{"arxiv_id": "2407.01392", "title": "DiffusionForcing"}],
        auto_discover=False,
    )
    write_campaign(tmp_path, listed)
    loaded = load_campaign(tmp_path)
    assert loaded is not None
    assert loaded.auto_discover is False
    assert loaded.force_include[0]["arxiv_id"] == "2407.01392"
