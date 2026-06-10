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
    assert 'uv tool install --with socksio "mineru[core]"' in report


def test_report_all_present_banner(monkeypatch):
    _all_present(monkeypatch)
    assert "ALL HEALTHY" in format_report(check_environment())


def test_check_is_a_frozen_dataclass():
    c = Check(name="x", ok=True, detail="d", fix="f")
    assert (c.name, c.ok, c.detail, c.fix) == ("x", True, "d", "f")


# --- Layer 3: golden compare (pure) ----------------------------------------

_GOLDEN = {
    "equation_blocks": 1,
    "image_blocks": 1,
    "text_blocks_min": 1,
    "image_files_min": 1,
    "md_chars_min": 300,
}


def test_golden_problems_pass():
    assert preflight._golden_problems({"equation": 1, "image": 1, "text": 3}, 2, 643, _GOLDEN) == []


def test_golden_problems_flags_lost_equation_and_image():
    probs = preflight._golden_problems({"equation": 0, "image": 0, "text": 3}, 0, 643, _GOLDEN)
    joined = "; ".join(probs)
    assert "equation" in joined and "image" in joined


def test_golden_problems_flags_truncated_md():
    probs = preflight._golden_problems({"equation": 1, "image": 1, "text": 3}, 2, 10, _GOLDEN)
    assert any("md chars" in p for p in probs)


# --- Layer 2: llm config + provider liveness -------------------------------


class _FakeProv:
    def __init__(self, name, *, base_url=None, api_key_env=None, reply="OK", boom=False):
        self.name = name
        if base_url is not None:
            self.base_url = base_url
        if api_key_env is not None:
            self.api_key_env = api_key_env
        self._reply, self._boom = reply, boom

    def complete(self, prompt, **kw):
        if self._boom:
            raise RuntimeError("dead endpoint")
        return self._reply


class _FakeCfg:
    def __init__(self, mapping):
        self._m = mapping

    def for_seam(self, seam):
        return self._m[seam]


def test_provider_live_ok():
    ok, detail = preflight._provider_live(_FakeProv("p", reply="OK"))
    assert ok and "reachable" in detail


def test_provider_live_unreachable_no_crash():
    ok, detail = preflight._provider_live(_FakeProv("p", boom=True))
    assert not ok and "unreachable" in detail


def test_check_llm_static_reports_keys_and_never_leaks_secret(monkeypatch):
    from scripts.llm.config import SEAMS

    cc = _FakeProv("claude-code")  # no base_url → presence-only, not probed
    api = _FakeProv("hellorobotaxi", base_url="http://x/v1", api_key_env="FAKE_KEY", reply="OK")
    mapping = {s: (cc if s == "analyzer" else api) for s in SEAMS}
    monkeypatch.setattr("scripts.llm.config.load_llm_config", lambda ws: _FakeCfg(mapping))
    monkeypatch.setattr(preflight.shutil, "which", lambda t: "/usr/bin/claude")
    monkeypatch.setenv("FAKE_KEY", "sk-supersecret-value")

    checks = preflight.check_llm(probe=True)
    by = {c.name: c for c in checks}
    assert by["llm:llm.yaml"].ok
    assert by["provider:claude-code"].ok and "not probed" in by["provider:claude-code"].detail
    assert by["provider:hellorobotaxi"].ok and "reachable" in by["provider:hellorobotaxi"].detail
    # the api key value must NEVER appear in any check output
    assert all("supersecret" not in c.detail for c in checks)


def test_check_llm_unset_key_fails(monkeypatch):
    from scripts.llm.config import SEAMS

    api = _FakeProv("hellorobotaxi", base_url="http://x/v1", api_key_env="UNSET_KEY_XYZ")
    monkeypatch.setattr(
        "scripts.llm.config.load_llm_config", lambda ws: _FakeCfg(dict.fromkeys(SEAMS, api))
    )
    monkeypatch.delenv("UNSET_KEY_XYZ", raising=False)
    checks = preflight.check_llm(probe=True)
    prov = next(c for c in checks if c.name == "provider:hellorobotaxi")
    assert not prov.ok and "UNSET" in prov.detail


def test_check_llm_unroutable_config_fails(monkeypatch):
    def _boom(ws):
        raise ValueError("seam 'writer' routes to undefined provider 'typo'")

    monkeypatch.setattr("scripts.llm.config.load_llm_config", _boom)
    checks = preflight.check_llm(probe=False)
    assert len(checks) == 1 and not checks[0].ok and "unroutable" in checks[0].detail
