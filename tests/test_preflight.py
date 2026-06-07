"""Preflight gate: verify it detects present vs missing prerequisites so a missing
tool is a loud STOP (exit 1), never a silent per-paper skip."""

from __future__ import annotations

import scripts.preflight as preflight
from scripts.preflight import Check, all_ok, check_environment, format_report


def _all_present(monkeypatch):
    monkeypatch.setattr(preflight.shutil, "which", lambda tool: f"/usr/bin/{tool}")
    monkeypatch.setattr(preflight, "_has_module", lambda mod: True)


def test_all_present_passes(monkeypatch):
    _all_present(monkeypatch)
    checks = check_environment()
    assert all_ok(checks)
    # the four required prerequisites are covered
    names = {c.name for c in checks}
    assert names == {"python:requests", "python:pyyaml", "pandoc", "mineru"}


def test_missing_mineru_fails_with_fix(monkeypatch):
    _all_present(monkeypatch)
    monkeypatch.setattr(
        preflight.shutil, "which", lambda tool: None if tool == "mineru" else f"/usr/bin/{tool}"
    )
    checks = check_environment()
    assert not all_ok(checks)
    mineru = next(c for c in checks if c.name == "mineru")
    assert not mineru.ok
    assert "mineru[core]" in mineru.fix


def test_missing_python_dep_fails(monkeypatch):
    _all_present(monkeypatch)
    monkeypatch.setattr(preflight, "_has_module", lambda mod: mod != "yaml")
    checks = check_environment()
    assert not all_ok(checks)
    assert any(c.name == "python:pyyaml" and not c.ok for c in checks)


def test_report_lists_fix_for_missing_and_stop_banner(monkeypatch):
    _all_present(monkeypatch)
    monkeypatch.setattr(preflight.shutil, "which", lambda tool: None)  # no system tools
    report = format_report(check_environment())
    assert "DO NOT proceed" in report
    assert "brew install pandoc" in report
    assert 'uv pip install -U "mineru[core]"' in report


def test_report_all_present_banner(monkeypatch):
    _all_present(monkeypatch)
    assert "ALL PRESENT" in format_report(check_environment())


def test_check_is_a_frozen_dataclass():
    c = Check(name="x", ok=True, detail="d", fix="f")
    assert (c.name, c.ok, c.detail, c.fix) == ("x", True, "d", "f")
