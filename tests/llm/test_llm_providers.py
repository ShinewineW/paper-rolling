from __future__ import annotations

import subprocess
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


class _StreamResp:
    """Fake streaming response: a context manager whose iter_lines yields SSE
    `data:` frames (the new transport contract)."""

    def __init__(self, status_code: int, lines: list[str] | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._lines = lines or []
        self.text = text

    def __enter__(self) -> _StreamResp:
        return self

    def __exit__(self, *exc) -> bool:
        return False

    def iter_lines(self, decode_unicode: bool = False):  # noqa: FBT002 - mirror requests API
        yield from self._lines


def test_openai_complete_parses_content(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    captured: dict = {}

    def _fake_post(url, json, headers, stream, timeout):  # noqa: A002 - mirror requests API
        captured["url"] = url
        captured["model"] = json["model"]
        captured["stream"] = stream
        captured["auth"] = headers["Authorization"]
        # Content arrives as two streamed delta chunks, then the [DONE] sentinel.
        return _StreamResp(
            200,
            [
                'data: {"choices": [{"delta": {"content": "hello-"}}]}',
                'data: {"choices": [{"delta": {"content": "world"}}]}',
                "data: [DONE]",
            ],
        )

    monkeypatch.setattr(P.requests, "post", _fake_post)
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="STRONG",
        fast_model="FAST",
        api_key_env="TEST_KEY_ENV",
    )
    assert prov.complete("hi", tier="fast") == "hello-world"  # deltas assembled
    assert captured["url"].endswith("/chat/completions")
    assert captured["model"] == "FAST"  # tier routing
    assert captured["stream"] is True  # streamed transport
    assert captured["auth"] == "Bearer sk-test"


class _EncStreamResp:
    """Fake SSE response whose `iter_lines(decode_unicode=True)` decodes its raw
    UTF-8 frames via `self.encoding` — mirroring requests, which defaults a
    charset-less `text/event-stream` to ISO-8859-1. Lets us prove the provider
    pins UTF-8 (else CJK comes back as mojibake)."""

    def __init__(self, frames_utf8: list[str]) -> None:
        self.status_code = 200
        self.encoding = "ISO-8859-1"  # requests' charset-less default
        self._raw = [f.encode("utf-8") for f in frames_utf8]
        self.text = ""

    def __enter__(self) -> _EncStreamResp:
        return self

    def __exit__(self, *exc) -> bool:
        return False

    def iter_lines(self, decode_unicode: bool = False):  # noqa: FBT002 - mirror requests API
        for b in self._raw:
            yield b.decode(self.encoding) if decode_unicode else b


def test_openai_sse_decodes_cjk_as_utf8_not_latin1(monkeypatch: pytest.MonkeyPatch) -> None:
    # Regression: a charset-less SSE stream made requests decode CJK as latin-1,
    # turning a Chinese report into mojibake (ORION revival demo). _consume_sse must
    # pin resp.encoding='utf-8' so the assembled content is the real Chinese.
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    cjk = "本文模型达到 28.4 NDS,仅用 10% 数据"
    monkeypatch.setattr(
        P.requests,
        "post",
        lambda *a, **k: _EncStreamResp(
            [f'data: {{"choices": [{{"delta": {{"content": "{cjk}"}}}}]}}', "data: [DONE]"]
        ),
    )
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    assert prov.complete("hi") == cjk  # real Chinese, NOT 'æ\x9c¬æ\x96\x87...' mojibake


def test_openai_sse_excludes_reasoning_content_from_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    # Regression: reasoning models stream chain-of-thought in `reasoning_content`
    # and the answer in `content`. The consumer must return ONLY content — the old
    # `content or reasoning_content` concatenated the model's thinking into the
    # report (ORION: "Wait, I should be careful… Previous Rejection: '2026'…").
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    monkeypatch.setattr(
        P.requests,
        "post",
        lambda *a, **k: _StreamResp(
            200,
            [
                'data: {"choices": [{"delta": {"reasoning_content": "Wait, be careful"}}]}',
                'data: {"choices": [{"delta": {"content": "正式答案"}}]}',
                'data: {"choices": [{"delta": {"reasoning_content": "double-check"}}]}',
                "data: [DONE]",
            ],
        ),
    )
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    assert prov.complete("hi") == "正式答案"  # ONLY the answer, no chain-of-thought


def test_openai_sse_falls_back_to_reasoning_when_no_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Degenerate model that emits only reasoning_content (no separate answer): we
    # still return something rather than treating it as an empty stream.
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    monkeypatch.setattr(
        P.requests,
        "post",
        lambda *a, **k: _StreamResp(
            200,
            [
                'data: {"choices": [{"delta": {"reasoning_content": "only-reasoning"}}]}',
                "data: [DONE]",
            ],
        ),
    )
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    assert prov.complete("hi") == "only-reasoning"


def test_openai_complete_4xx_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    monkeypatch.setattr(P.requests, "post", lambda *a, **k: _StreamResp(400, text="bad request"))
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    with pytest.raises(P.ProviderError, match="HTTP 400"):
        prov.complete("hi")


def test_openai_complete_empty_stream_retries_then_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 200 stream that yields no content is transient (_RetryableHTTP): the loop
    retries and, on persistent emptiness, raises ProviderError — never returns ''."""
    monkeypatch.setenv("TEST_KEY_ENV", "sk-test")
    monkeypatch.setattr(P.time, "sleep", lambda *_a, **_k: None)  # skip real backoff
    calls = {"n": 0}

    def _empty_post(*a, **k):
        calls["n"] += 1
        return _StreamResp(200, ["data: [DONE]"])  # no delta content

    monkeypatch.setattr(P.requests, "post", _empty_post)
    prov = P.OpenAICompatibleProvider(
        name="t",
        base_url="https://x/v1",
        strong_model="s",
        fast_model="f",
        api_key_env="TEST_KEY_ENV",
    )
    with pytest.raises(P.ProviderError):
        prov.complete("hi")
    assert calls["n"] > 1  # it retried, did not pass the empty result through


def test_load_absent_config_raises(tmp_path: Path) -> None:
    # No implicit all-claude-code default: a missing config file is a loud error.
    with pytest.raises(ValueError, match="not found"):
        load_llm_config(tmp_path)


def _full_seam_yaml(*, analyzer: str = "{ provider: claude-code, mode: grounded }") -> str:
    """A config routing ALL seven seams (every seam must be explicitly routed)."""
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
        "  faithfulness: opencode\n"
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


def test_provider_concurrency_is_per_instance_and_configurable():
    # Goal 3: each provider instance owns its OWN semaphore, sized to its own
    # `max_concurrent` from config — NOT a process-global cap. A generous backend
    # can run wide while an expensive one runs narrow, independently.
    claude = P.build_provider(
        "claude-code", {"type": "claude_code", "strong_model": "S", "fast_model": "F"}
    )
    codex_narrow = P.build_provider("codex", {"type": "codex_cli", "max_concurrent": 3})
    api_wide = P.build_provider(
        "api",
        {
            "type": "openai_compatible",
            "base_url": "u",
            "strong_model": "s",
            "fast_model": "f",
            "api_key_env": "K",
            "max_concurrent": 10,
        },
    )
    assert claude.max_concurrent == 5  # agent default
    assert claude._sem._value == 5
    assert codex_narrow.max_concurrent == 3  # independently set narrow
    assert codex_narrow._sem._value == 3
    assert api_wide.max_concurrent == 10  # independently set wide
    assert api_wide._sem._value == 10
    # distinct semaphore objects → independent caps, no shared global
    assert claude._sem is not codex_narrow._sem is not api_wide._sem


def test_provider_max_concurrent_must_be_positive_int():
    for bad in (0, -1, "5", 2.5, True):
        with pytest.raises(P.ProviderError, match="max_concurrent"):
            P.build_provider("codex", {"type": "codex_cli", "max_concurrent": bad})


def test_grounded_capability_is_per_type():
    claude = P.build_provider("c", {"type": "claude_code", "strong_model": "S", "fast_model": "F"})
    codex = P.build_provider("x", {"type": "codex_cli"})
    api = P.build_provider(
        "a",
        {
            "type": "openai_compatible",
            "base_url": "u",
            "strong_model": "s",
            "fast_model": "f",
            "api_key_env": "K",
        },
    )
    assert claude.grounded_capable is True
    assert codex.grounded_capable is True
    assert api.grounded_capable is False  # HTTP: no local file access


# --- Codex CLI provider (third type: local agent, grounded-capable) ----------


def test_build_provider_codex_cli_defaults_model_empty() -> None:
    prov = P.build_provider("codex", {"type": "codex_cli"})
    assert isinstance(prov, P.CodexCliProvider)
    assert prov.name == "codex"
    assert prov.model == ""  # empty => codex CLI default model
    assert prov.cli == "codex"  # preflight checks `which("codex")`


def test_build_provider_codex_cli_optional_model() -> None:
    prov = P.build_provider("codex", {"type": "codex_cli", "model": "gpt-5.3-codex"})
    assert isinstance(prov, P.CodexCliProvider)
    assert prov.model == "gpt-5.3-codex"


def test_codex_complete_returns_final_message(monkeypatch: pytest.MonkeyPatch) -> None:
    # codex exec writes its final message to the `-o <file>` path; the provider
    # returns that raw text (JSON parsing lives in the seam layer, like claude-code).
    seen: dict = {}

    def fake_run(argv, *, input, capture_output, text, timeout, check):  # noqa: A002
        assert argv[0:2] == ["codex", "exec"]
        assert "--dangerously-bypass-approvals-and-sandbox" in argv
        out_path = argv[argv.index("-o") + 1]
        Path(out_path).write_text('{"concepts": []}', encoding="utf-8")
        seen["prompt"] = input
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(P.subprocess, "run", fake_run)
    prov = P.build_provider("codex", {"type": "codex_cli"})
    assert prov.complete("hello") == '{"concepts": []}'
    assert seen["prompt"] == "hello"


def test_codex_complete_passes_model_when_set(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    def fake_run(argv, *, input, capture_output, text, timeout, check):  # noqa: A002
        captured["argv"] = argv
        Path(argv[argv.index("-o") + 1]).write_text("ok", encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(P.subprocess, "run", fake_run)
    prov = P.build_provider("codex", {"type": "codex_cli", "model": "gpt-5.3-codex"})
    prov.complete("x")
    argv = captured["argv"]
    assert "-m" in argv and argv[argv.index("-m") + 1] == "gpt-5.3-codex"


def test_codex_complete_nonzero_exit_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(P, "_backoff_sleep", lambda *_a: None)  # no real sleeps in tests

    def fake_run(argv, **_k):
        return subprocess.CompletedProcess(argv, 2, stdout="", stderr="boom")

    monkeypatch.setattr(P.subprocess, "run", fake_run)
    prov = P.build_provider("codex", {"type": "codex_cli"})
    with pytest.raises(P.ProviderError, match="codex exec exit 2"):
        prov.complete("x")


def test_codex_concurrency_defaults_to_agent_default():
    # codex's own per-instance cap defaults to the agent default (5), independent
    # of claude's — set it lower in config for an expensive run.
    prov = P.build_provider("codex", {"type": "codex_cli"})
    assert prov.max_concurrent == P._DEFAULT_AGENT_CONCURRENCY == 5
    assert prov._sem._value == 5


def _codex_grounded_yaml(*, analyzer_provider: str = "codex") -> str:
    return (
        "providers:\n"
        "  codex:\n"
        "    type: codex_cli\n"
        "  opencode:\n"
        "    type: openai_compatible\n"
        "    base_url: https://opencode.ai/zen/go/v1\n"
        "    api_key_env: OPENCODE_API_KEY\n"
        "    strong_model: deepseek-v4-pro\n"
        "    fast_model: deepseek-v4-flash\n"
        "seams:\n"
        f"  analyzer: {{ provider: {analyzer_provider}, mode: grounded }}\n"
        "  skeptic: opencode\n"
        "  rigor: opencode\n"
        "  entailment: opencode\n"
        "  expand: opencode\n"
        "  writer: opencode\n"
        "  faithfulness: opencode\n"
    )


def test_grounded_analyzer_allows_codex_provider(tmp_path: Path) -> None:
    # codex_cli is a LOCAL agent (no base_url) → grounded routing is permitted,
    # exactly like claude-code. This is the cross-model analyzer swap.
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(_codex_grounded_yaml(), encoding="utf-8")
    cfg = load_llm_config(tmp_path)
    assert cfg.for_seam("analyzer").name == "codex"
    assert cfg.mode_for("analyzer") == "grounded"


def test_grounded_analyzer_rejects_http_provider(tmp_path: Path) -> None:
    # An HTTP API has no local Read/Grep → grounded routing must still fail loud.
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(
        _codex_grounded_yaml(analyzer_provider="opencode"), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="grounded"):
        load_llm_config(tmp_path)


# --- RoundRobinProvider (composite: alternate claude <-> codex) ---------------


class _Spy:
    """Member double: records the calls it received, returns a tagged result."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.cli = name
        self.calls = 0

    def complete(self, prompt, *, tier="strong", effort="high", timeout=900.0, tools=None) -> str:
        self.calls += 1
        return f"{self.name}:{prompt}"


def test_round_robin_alternates_members() -> None:
    a, b = _Spy("claude"), _Spy("codex")
    rr = P.RoundRobinProvider("pool", (a, b))
    assert [rr.complete(str(i)) for i in range(4)] == [
        "claude:0",
        "codex:1",
        "claude:2",
        "codex:3",
    ]
    assert a.calls == 2 and b.calls == 2  # balanced across the two backends


def test_round_robin_member_clis_distinct() -> None:
    rr = P.RoundRobinProvider("pool", (_Spy("claude"), _Spy("codex")))
    assert rr.member_clis == ("claude", "codex")


def test_round_robin_empty_members_raises() -> None:
    with pytest.raises(P.ProviderError, match="round_robin"):
        P.RoundRobinProvider("pool", ())


def test_round_robin_thread_safe_balance() -> None:
    import threading as _t

    a, b = _Spy("claude"), _Spy("codex")
    rr = P.RoundRobinProvider("pool", (a, b))

    def worker() -> None:
        for _ in range(50):
            rr.complete("x")

    threads = [_t.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # 200 total calls split evenly under the lock (no lost/duplicated rotation).
    assert a.calls + b.calls == 200
    assert abs(a.calls - b.calls) <= 1


def _round_robin_yaml() -> str:
    return (
        "providers:\n"
        "  claude-code:\n"
        "    type: claude_code\n"
        "    strong_model: claude-sonnet-4-6\n"
        "    fast_model: claude-haiku-4-5\n"
        "  codex:\n"
        "    type: codex_cli\n"
        "  analyzer-pool:\n"
        "    type: round_robin\n"
        "    members: [claude-code, codex]\n"
        "  opencode:\n"
        "    type: openai_compatible\n"
        "    base_url: https://opencode.ai/zen/go/v1\n"
        "    api_key_env: OPENCODE_API_KEY\n"
        "    strong_model: deepseek-v4-pro\n"
        "    fast_model: deepseek-v4-flash\n"
        "seams:\n"
        "  analyzer: { provider: analyzer-pool, mode: grounded }\n"
        "  skeptic: opencode\n"
        "  rigor: opencode\n"
        "  entailment: opencode\n"
        "  expand: opencode\n"
        "  writer: opencode\n"
        "  faithfulness: opencode\n"
    )


def test_round_robin_pool_grounded_analyzer_loads(tmp_path: Path) -> None:
    # A round_robin of two LOCAL agents is grounded-capable (no base_url) and
    # resolves its members via the 2-pass build.
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(_round_robin_yaml(), encoding="utf-8")
    cfg = load_llm_config(tmp_path)
    pool = cfg.for_seam("analyzer")
    assert isinstance(pool, P.RoundRobinProvider)
    assert pool.member_clis == ("claude", "codex")
    assert cfg.mode_for("analyzer") == "grounded"


def test_round_robin_undefined_member_raises(tmp_path: Path) -> None:
    bad = _round_robin_yaml().replace(
        "members: [claude-code, codex]", "members: [claude-code, ghost]"
    )
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(bad, encoding="utf-8")
    with pytest.raises(P.ProviderError, match="not defined"):
        load_llm_config(tmp_path)


def _api_member_provider():
    return P.build_provider(
        "api",
        {
            "type": "openai_compatible",
            "base_url": "u",
            "strong_model": "s",
            "fast_model": "f",
            "api_key_env": "K",
        },
    )


def test_round_robin_grounded_capable_only_if_all_members_are() -> None:
    claude = P.build_provider("c", {"type": "claude_code", "strong_model": "S", "fast_model": "F"})
    codex = P.build_provider("x", {"type": "codex_cli"})
    api = _api_member_provider()
    assert P.RoundRobinProvider("ok", (claude, codex)).grounded_capable is True
    # one HTTP member ⇒ the pool is NOT grounded-capable (it can't read files).
    assert P.RoundRobinProvider("mixed", (claude, api)).grounded_capable is False


def test_round_robin_member_clis_excludes_http_members() -> None:
    claude = P.build_provider("c", {"type": "claude_code", "strong_model": "S", "fast_model": "F"})
    pool = P.RoundRobinProvider("mixed", (claude, _api_member_provider()))
    assert pool.member_clis == ("claude",)  # HTTP member has no CLI → not defaulted to claude


def test_grounded_pool_with_http_member_is_rejected(tmp_path: Path) -> None:
    # A pool mixing a local agent with an HTTP member must NOT pass grounded
    # validation — the HTTP member cannot read the source MD (Codex R1 BLOCKING).
    bad = _round_robin_yaml().replace(
        "members: [claude-code, codex]", "members: [claude-code, opencode]"
    )
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(bad, encoding="utf-8")
    with pytest.raises(ValueError, match="grounded"):
        load_llm_config(tmp_path)


def test_round_robin_members_keep_independent_caps() -> None:
    # The pool has no cap of its own; each member self-limits with its own
    # semaphore, so total concurrency is the SUM (claude 5 + codex 3 here).
    claude = P.build_provider(
        "c", {"type": "claude_code", "strong_model": "S", "fast_model": "F", "max_concurrent": 5}
    )
    codex = P.build_provider("x", {"type": "codex_cli", "max_concurrent": 3})
    pool = P.RoundRobinProvider("p", (claude, codex))
    caps = {m.name: m._sem._value for m in pool.members}
    assert caps == {"c": 5, "x": 3}
