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
