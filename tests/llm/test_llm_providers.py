from __future__ import annotations

from pathlib import Path

import pytest
from scripts.llm import providers as P
from scripts.llm.config import load_llm_config


def test_build_provider_claude_code_requires_explicit_models() -> None:
    # No default models: routing to the Claude Code subscription is a deliberate
    # choice, so the models must be specified explicitly or build fails.
    prov = P.build_provider(
        "claude-code",
        {"type": "claude_code", "strong_model": "S", "fast_model": "F"},
    )
    assert isinstance(prov, P.ClaudeCodeProvider)
    assert prov.name == "claude-code"
    assert (prov.strong_model, prov.fast_model) == ("S", "F")


def test_build_provider_claude_code_missing_models_raises() -> None:
    with pytest.raises(P.ProviderError, match="claude_code missing"):
        P.build_provider("claude-code", {"type": "claude_code"})


def test_build_provider_openai_compatible() -> None:
    prov = P.build_provider(
        "opencode",
        {
            "type": "openai_compatible",
            "base_url": "https://opencode.ai/zen/go/v1",
            "api_key_env": "OPENCODE_API_KEY",
            "strong_model": "deepseek-v4-pro",
            "fast_model": "deepseek-v4-flash",
        },
    )
    assert isinstance(prov, P.OpenAICompatibleProvider)
    assert prov.strong_model == "deepseek-v4-pro"


def test_build_provider_unknown_type_raises() -> None:
    with pytest.raises(P.ProviderError, match="unknown type"):
        P.build_provider("x", {"type": "telepathy"})


def test_build_provider_openai_missing_field_raises() -> None:
    with pytest.raises(P.ProviderError, match="missing"):
        P.build_provider("bad", {"type": "openai_compatible", "base_url": "u"})


def test_openai_complete_missing_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TEST_KEY_ENV", raising=False)
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    with pytest.raises(P.ProviderError, match="TEST_KEY_ENV"):
        prov.complete("hi")


def test_openai_complete_parses_content(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    captured: dict = {}

    class _Resp:
        status_code = 200

        def json(self) -> dict:
            return {"choices": [{"message": {"content": "hello-world"}}]}

    def _fake_post(url, json, headers, timeout):  # noqa: A002 - mirror requests API
        captured["url"] = url
        captured["model"] = json["model"]
        captured["auth"] = headers["Authorization"]
        return _Resp()

    monkeypatch.setattr(P.requests, "post", _fake_post)
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="STRONG",
        fast_model="FAST",
        api_key_env="TEST_KEY_ENV",
    )
    assert prov.complete("hi", tier="fast") == "hello-world"
    assert captured["url"].endswith("/chat/completions")
    assert captured["model"] == "FAST"  # tier routing
    assert captured["auth"] == "Bearer sk-test"


def test_openai_complete_4xx_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")

    class _Resp:
        status_code = 400
        text = "bad request"

    monkeypatch.setattr(P.requests, "post", lambda *a, **k: _Resp())
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    with pytest.raises(P.ProviderError, match="HTTP 400"):
        prov.complete("hi")


def test_load_absent_config_raises(tmp_path: Path) -> None:
    # No implicit all-claude-code default: a missing config file is a loud error.
    with pytest.raises(ValueError, match="not found"):
        load_llm_config(tmp_path)


def _full_seam_yaml(*, analyzer: str = "{ provider: claude-code, mode: grounded }") -> str:
    """A config routing ALL six seams (every seam must be explicitly routed)."""
    return (
        "providers:\n"
        "  claude-code:\n"
        "    type: claude_code\n"
        "    strong_model: claude-sonnet-4-6\n"
        "    fast_model: claude-haiku-4-5\n"
        "  opencode:\n"
        "    type: openai_compatible\n"
        "    base_url: https://opencode.ai/zen/go/v1\n"
        "    api_key_env: OPENCODE_API_KEY\n"
        "    strong_model: deepseek-v4-pro\n"
        "    fast_model: deepseek-v4-flash\n"
        "seams:\n"
        f"  analyzer: {analyzer}\n"
        "  skeptic: opencode\n"
        "  rigor: opencode\n"
        "  entailment: opencode\n"
        "  expand: opencode\n"
        "  writer: opencode\n"
    )


def test_load_routes_seams_explicitly(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(_full_seam_yaml(), encoding="utf-8")
    cfg = load_llm_config(tmp_path)
    assert cfg.for_seam("analyzer").name == "claude-code"  # explicit, grounded
    assert cfg.for_seam("writer").name == "opencode"
    assert cfg.for_seam("skeptic").name == "opencode"


def test_load_unrouted_seam_raises(tmp_path: Path) -> None:
    # Drop the writer routing -> must fail loud (no default routing).
    yaml_text = _full_seam_yaml().replace("  writer: opencode\n", "")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(yaml_text, encoding="utf-8")
    with pytest.raises(ValueError, match="seam 'writer' is not routed"):
        load_llm_config(tmp_path)


def test_load_unknown_provider_in_routing_raises(tmp_path: Path) -> None:
    # All seams routed, but writer points at an undefined provider.
    yaml_text = _full_seam_yaml().replace("  writer: opencode\n", "  writer: ghost\n")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(yaml_text, encoding="utf-8")
    with pytest.raises(ValueError, match="undefined provider"):
        load_llm_config(tmp_path)


# --- StrictProvider + EngineAbort (the loud, no-fallback failure path) ------


class _FakeProvider:
    """Test double: returns a fixed result, or raises ProviderError if `fail`."""

    def __init__(self, name: str, *, fail: bool = False, result: str = "ok") -> None:
        self._name = name
        self._fail = fail
        self._result = result

    @property
    def name(self) -> str:
        return self._name

    def complete(self, prompt, *, tier="strong", effort="high", timeout=900.0, tools=None) -> str:
        if self._fail:
            raise P.ProviderError(f"{self._name} forced failure")
        return self._result


def test_strict_passes_through_on_success() -> None:
    sp = P.StrictProvider(_FakeProvider("opencode", result="P"))
    assert sp.complete("x") == "P"
    assert sp.name == "opencode"


def test_strict_aborts_loudly_on_failure() -> None:
    # No fallback: a failing provider raises EngineAbort (which the hub treats as a
    # whole-tick abort), never silently swapping to another backend.
    sp = P.StrictProvider(_FakeProvider("opencode", fail=True))
    with pytest.raises(P.EngineAbort, match="NO fallback"):
        sp.complete("x")


def test_resolve_wraps_seam_in_strict_provider(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(_full_seam_yaml(), encoding="utf-8")
    cfg = load_llm_config(tmp_path)
    sp = cfg.resolve("writer")
    assert isinstance(sp, P.StrictProvider)
    assert sp.name == "opencode"  # the explicitly-routed provider, no fallback field
    assert not hasattr(sp, "fallback")


def test_claude_p_global_concurrency_cap_defaults_to_5():
    # Account-level rate-limit guard: claude -p is bounded process-wide to <=5.
    assert P._CLAUDE_P_MAX == 5
    assert P._CLAUDE_P_SEM._value <= P._CLAUDE_P_MAX
