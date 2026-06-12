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
    # Baseline + the cross-model overlay (B10 / ROADMAP C2 is now SHIPPED): the
    # optional `cross_model_votes` heterogeneous-family verifier strengthens the
    # gate. Plus the operator-tunable tolerance knobs (config/audit.yaml): when
    # `tolerant`, a few unconfirmed numbers within `max_unconfirmed` /
    # `max_unconfirmed_ratio` are flagged instead of hard-blocking. All are
    # keyword-only with back-compatible defaults (tolerant=False = strict), so the
    # hub's existing calls are unchanged.
    assert list(sig.parameters) == [
        "ai_package_dir",
        "md_path",
        "skeptic_votes",
        "n_skeptics",
        "cross_model_votes",
        "tolerant",
        "max_unconfirmed",
        "max_unconfirmed_ratio",
    ]


def test_run_g3_signature_is_stable_for_hub() -> None:
    sig = inspect.signature(g3_seal.run_g3)
    # ADR-0012: empirical_classifier seam (ROADMAP C4) removed — prose-anchor
    # requirement dropped; check_branch1_md_anchors no longer uses a classifier.
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
        "write_quarantine_note",
    ]


def test_top_level_exports_present() -> None:
    for name in ("GateVerdict", "GateOutcome", "Finding", "Severity", "ClaimRecord", "ClaimType"):
        assert hasattr(audit, name)
