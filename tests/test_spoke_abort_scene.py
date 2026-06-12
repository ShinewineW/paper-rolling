"""Integration test: EngineAbort at G2 preserves the built ARA as a _failed/ scene.

ADR-0011 regression: a transport abort (e.g. the Qwen audit endpoint dropping)
after the ARA is built must not silently delete the paid-for ARA. The spoke must
scene it into _failed/<key>/ and re-raise so the tick still aborts.
"""

from __future__ import annotations

import pytest
from scripts.hub import _candidate_key
from scripts.ledger.store import Ledger
from scripts.paths import EngineAbort
from scripts.spoke import make_spoke

# Reuse the fully-valid fixtures from test_spoke.py (produce a Seal-1-passing ARA).
from test_spoke import (
    _CANDIDATE,
    _SOURCE_MD,
    _entailed,
    _good_rigor,
    _mineru_emitting,
    _resolve_analysis,
    _tier2_http,
)


def test_abort_at_g2_preserves_scene_and_reraises(tmp_path, fake_http, fake_cli):
    """ADR-0011: EngineAbort during G2 (after ARA is built) must scene the ARA
    into _failed/<key>/ and re-raise — the tick still aborts, cost guard unchanged."""
    _tier2_http(fake_http, dict(_CANDIDATE))

    def _aborting_skeptic(numbers, source_md, claim_context):
        raise EngineAbort("qwen audit endpoint down")

    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_aborting_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=Ledger(tmp_path),
        n_skeptics=1,
        max_gate_rounds=1,
    )

    with pytest.raises(EngineAbort):
        spoke(dict(_CANDIDATE))

    cand_key = _candidate_key(dict(_CANDIDATE))
    scene_dir = tmp_path / "_failed" / cand_key
    assert scene_dir.exists(), f"_failed/{cand_key}/ scene must be created on EngineAbort"
    assert (scene_dir / "ai" / "ara").is_dir(), "built ARA must be in the scene"
