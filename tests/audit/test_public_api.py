from __future__ import annotations

import inspect

import scripts.audit as audit
from scripts.audit import g2_data_fidelity, g3_seal, gate_runner


def test_public_gate_entrypoints_are_importable() -> None:
    assert callable(g2_data_fidelity.run_g2)
    assert callable(g3_seal.run_g3)
    assert callable(gate_runner.run_with_budget)


def test_run_g2_signature_is_stable_for_hub() -> None:
    sig = inspect.signature(g2_data_fidelity.run_g2)
    # Round 2 F3/F6: baseline signature. B8/B10 (defect-stage + cross-model) are
    # DEFERRED post-MVP (see Revision §"Deferred"), so run_g2 stays at the baseline
    # — no cross_model_fn/cross_model_sample params in the buildable MVP.
    assert list(sig.parameters) == ["ai_package_dir", "md_path", "skeptic_votes", "n_skeptics"]


def test_run_g3_signature_is_stable_for_hub() -> None:
    sig = inspect.signature(g3_seal.run_g3)
    assert list(sig.parameters) == [
        "person_vault_entry",
        "ai_package_entry",
        "md_path",
        "content_list_path",
        "rigor_scores",
        "entailment_judge",
    ]


def test_run_with_budget_signature_is_stable_for_hub() -> None:
    sig = inspect.signature(gate_runner.run_with_budget)
    assert list(sig.parameters) == [
        "gate",
        "max_rounds",
        "on_reemit",
        "failed_dir",
        "key",
        "paper_meta",
    ]


def test_top_level_exports_present() -> None:
    for name in ("GateVerdict", "GateOutcome", "Finding", "Severity", "ClaimRecord", "ClaimType"):
        assert hasattr(audit, name)
