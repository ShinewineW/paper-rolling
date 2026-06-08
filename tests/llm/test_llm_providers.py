from __future__ import annotations

from pathlib import Path

import pytest
from scripts.llm import providers as P
from scripts.llm.config import load_llm_config


def test_build_provider_claude_code_defaults() -> None:
    prov = P.build_provider("claude-code", {"type": "claude_code"})
    assert isinstance(prov, P.ClaudeCodeProvider)
    assert prov.name == "claude-code"
    assert prov.strong_model and prov.fast_model


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


def test_load_default_when_absent(tmp_path: Path) -> None:
    cfg = load_llm_config(tmp_path)
    assert set(cfg.providers) == {"claude-code"}
    assert all(cfg.routing[s] == "claude-code" for s in cfg.routing)
    assert cfg.for_seam("writer").name == "claude-code"


def test_load_routes_writer_to_opencode(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(
        "providers:\n"
        "  opencode:\n"
        "    type: openai_compatible\n"
        "    base_url: https://opencode.ai/zen/go/v1\n"
        "    api_key_env: OPENCODE_API_KEY\n"
        "    strong_model: deepseek-v4-pro\n"
        "    fast_model: deepseek-v4-flash\n"
        "seams:\n"
        "  analyzer: claude-code\n"
        "  writer: opencode\n",
        encoding="utf-8",
    )
    cfg = load_llm_config(tmp_path)
    assert cfg.for_seam("analyzer").name == "claude-code"  # claude-code auto-injected
    assert cfg.for_seam("writer").name == "opencode"
    assert cfg.for_seam("skeptic").name == "claude-code"  # unlisted -> default


def test_load_unknown_provider_in_routing_raises(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(
        "providers:\n  claude-code:\n    type: claude_code\nseams:\n  writer: ghost\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="undefined provider"):
        load_llm_config(tmp_path)


# --- FallbackProvider + EngineAbort (the mandatory failure path) ------------


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


def test_fallback_uses_primary_on_success() -> None:
    fb = P.FallbackProvider(
        primary=_FakeProvider("primary", result="P"), fallback=_FakeProvider("claude-code")
    )
    assert fb.complete("x") == "P"
    assert fb.name == "primary->fallback:claude-code"


def test_fallback_to_secondary_on_primary_error() -> None:
    fb = P.FallbackProvider(
        primary=_FakeProvider("opencode", fail=True),
        fallback=_FakeProvider("claude-code", result="FB"),
    )
    assert fb.complete("x") == "FB"  # primary failed -> fell back to claude-code


def test_engine_abort_when_both_fail() -> None:
    fb = P.FallbackProvider(
        primary=_FakeProvider("opencode", fail=True),
        fallback=_FakeProvider("claude-code", fail=True),
    )
    with pytest.raises(P.EngineAbort, match="both failed"):
        fb.complete("x")


def test_engine_abort_when_bottom_line_is_primary() -> None:
    # analyzer case: primary IS claude-code (== fallback). Its failure has no lower
    # tier -> abort, never silently continue.
    cc = _FakeProvider("claude-code", fail=True)
    fb = P.FallbackProvider(primary=cc, fallback=cc)
    with pytest.raises(P.EngineAbort, match="no distinct"):
        fb.complete("x")


def test_resolve_wraps_seam_with_claude_fallback(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(
        "providers:\n"
        "  opencode:\n    type: openai_compatible\n    base_url: https://x/v1\n"
        "    api_key_env: X\n    strong_model: s\n    fast_model: f\n"
        "seams:\n  writer: opencode\n",
        encoding="utf-8",
    )
    cfg = load_llm_config(tmp_path)
    fb = cfg.resolve("writer")
    assert isinstance(fb, P.FallbackProvider)
    assert fb.primary.name == "opencode"
    assert fb.fallback.name == "claude-code"  # always the bottom-line default


def test_claude_p_global_concurrency_cap_defaults_to_5():
    # Account-level rate-limit guard: claude -p is bounded process-wide to <=5.
    assert P._CLAUDE_P_MAX == 5
    assert P._CLAUDE_P_SEM._value <= P._CLAUDE_P_MAX
