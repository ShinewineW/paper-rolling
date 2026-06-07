from __future__ import annotations

from pathlib import Path

import pytest
from scripts.audit_config import AuditConfig, load_audit_config


def _write(workspace: Path, body: str) -> None:
    (workspace / "config").mkdir(parents=True, exist_ok=True)
    (workspace / "config" / "audit.yaml").write_text(body, encoding="utf-8")


def test_load_audit_config_defaults_when_absent(tmp_path: Path) -> None:
    cfg = load_audit_config(tmp_path)
    assert cfg == AuditConfig()
    assert cfg.skeptic_votes == 1
    assert cfg.max_gate_rounds == 1
    assert cfg.data_fidelity_tolerant is True


def test_load_audit_config_reads_strict_file(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "skeptic_votes: 3\n"
        "max_gate_rounds: 2\n"
        "data_fidelity:\n"
        "  mode: strict\n"
        "  max_unconfirmed: 0\n"
        "  max_unconfirmed_ratio: 0.0\n",
    )
    cfg = load_audit_config(tmp_path)
    assert cfg.skeptic_votes == 3
    assert cfg.max_gate_rounds == 2
    assert cfg.data_fidelity_tolerant is False
    assert cfg.data_fidelity_max_unconfirmed == 0


def test_load_audit_config_partial_file_keeps_defaults(tmp_path: Path) -> None:
    _write(tmp_path, "skeptic_votes: 5\n")
    cfg = load_audit_config(tmp_path)
    assert cfg.skeptic_votes == 5
    assert cfg.max_gate_rounds == 1  # default
    assert cfg.data_fidelity_tolerant is True  # default


def test_load_audit_config_rejects_unknown_mode(tmp_path: Path) -> None:
    _write(tmp_path, "data_fidelity:\n  mode: lenient\n")
    with pytest.raises(ValueError, match="mode"):
        load_audit_config(tmp_path)


def test_audit_config_validates_ranges() -> None:
    with pytest.raises(ValueError, match="skeptic_votes"):
        AuditConfig(skeptic_votes=0)
    with pytest.raises(ValueError, match="max_gate_rounds"):
        AuditConfig(max_gate_rounds=0)
    with pytest.raises(ValueError, match="ratio"):
        AuditConfig(data_fidelity_max_unconfirmed_ratio=1.5)
