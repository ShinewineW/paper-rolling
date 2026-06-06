"""Integration tests for the production campaign driver (GATE-1 fix).

`scripts/run_campaign.run_campaign(...)` is the single entry point the /loop tick
drives: it composes Ledger -> make_spoke(seams) -> run_campaign_tick so the
adversarial guarantees (G2 number-fabrication hard-block + G3 6-dim seal) run in
a real executable pipeline, not just prose. These tests prove the driver:
  (a) composes the FULL gated pipeline end-to-end with the same deterministic
      fake seams the spoke test uses (locked campaign -> done + non-empty
      landscape), and
  (b) propagates the campaign Hard Gate (no campaign locked -> GateRequired).
"""

from __future__ import annotations

import pytest
from scripts.campaign import CampaignConfig, write_campaign
from scripts.hub import GateRequired
from scripts.run_campaign import run_campaign
from test_spoke import (
    _CANDIDATE,
    _SOURCE_MD,
    _all_found_skeptic,
    _entailed,
    _good_rigor,
    _mineru_emitting,
    _resolve_analysis,
    _tier2_http,
)


def _discover(topic, n):
    """Fake discovery returning >=1 candidate (a fresh copy per call)."""
    return [dict(_CANDIDATE)]


def test_run_campaign_composes_full_pipeline_to_done(tmp_path, fake_http, fake_cli):
    # Lock a campaign so gate_needed() is False (no HITL re-gate this tick).
    write_campaign(
        tmp_path,
        CampaignConfig(
            topic="real-time diffusion planning",
            n_per_tick=1,
            is_ad_domain=True,
        ),
    )
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))

    tick = run_campaign(
        workspace=tmp_path,
        discover=_discover,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        http=fake_http,
        run_cli=fake_cli,
    )

    # The driver composed the full gated pipeline: a paper reached true-done...
    assert tick.hub.done_count >= 1
    # ...and branch2's headline frontmatter fed a non-empty cross-paper landscape.
    assert tick.landscape.paper_count >= 1
    assert tick.landscape.index_path.exists()
    assert tick.landscape.report_path.exists()
    # The done paper has both vault halves on disk (single-writer ledger record).
    done = (tmp_path / "ai_package").iterdir()
    assert any(d.is_dir() for d in done)


def test_run_campaign_propagates_gate_required_without_campaign(tmp_path, fake_http, fake_cli):
    # No config/campaign.yaml locked -> the Hard Gate must fire and propagate.
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))

    with pytest.raises(GateRequired):
        run_campaign(
            workspace=tmp_path,
            discover=_discover,
            resolve_analysis=_resolve_analysis,
            skeptic_votes=_all_found_skeptic,
            rigor_scores=_good_rigor,
            entailment_judge=_entailed,
            http=fake_http,
            run_cli=fake_cli,
        )
