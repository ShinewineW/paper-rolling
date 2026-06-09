# .claude/skills/paper-landscape/scripts/llm/providers.py
"""Pluggable LLM transport providers for the paper-landscape seams.

The engine itself is provider-agnostic: every LLM-backed seam is an injected
callable (see scripts/run_campaign.py). This module supplies the *transport*
behind those callables as swappable PROVIDERS, so the runtime can route each
seam to a different backend WITHOUT touching the engine.

Two provider TYPES ship; neither is hard-wired to a vendor:

  - ``claude_code``        — a headless ``claude -p`` subprocess (uses the
                             caller's Claude Code subscription auth, supports
                             ``--effort`` and grounded Read/Grep). NOT a default:
                             a seam reaches it only when explicitly routed here.
  - ``openai_compatible``  — ANY OpenAI-/chat-completions-compatible HTTP API,
                             fully described by config (base_url + model ids +
                             api-key env var). OpenCode (deepseek) is just ONE
                             instance of this; adding OpenAI / Gemini(-compat) /
                             DeepSeek-direct / Together / a local vLLM is a config
                             block, NOT a new class. Do not couple to any vendor.

A provider exposes one method, ``complete(prompt, *, tier, effort, timeout) ->
str``, returning the raw assistant text (JSON parsing lives in the seam layer).
``tier`` selects the provider's strong/fast model; ``effort`` is honored where the
backend supports it (Claude Code) and ignored otherwise.
"""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

import requests

# EngineAbort lives in the LLM-agnostic core (scripts/paths.py) so the engine/hub
# can recognize it WITHOUT importing this transport layer; re-exported here since
# StrictProvider raises it and seam code imports it from here.
from scripts.paths import EngineAbort

# GLOBAL hard cap on concurrent `claude -p` subprocesses (account-level rate-limit
# guard). The analyzer fans out 5 chunks/paper; without this, N concurrent papers
# -> 5N concurrent `claude -p` saturated the API and stalled the whole run (see
# HANDOFF.md). This semaphore bounds it process-wide regardless of orchestration.
# Env-overridable but defaults to 5 (one paper's chunk fan-out).
_CLAUDE_P_MAX = max(1, int(os.environ.get("CLAUDE_P_MAX_CONCURRENCY", "5")))
_CLAUDE_P_SEM = threading.Semaphore(_CLAUDE_P_MAX)


class ProviderError(RuntimeError):
    """A provider call failed after exhausting its retry budget."""


@runtime_checkable
class LLMProvider(Protocol):
    """Transport behind one or more seams. Implementations must be stateless and
    safe to share across concurrent seam calls."""

    @property
    def name(self) -> str:
        """A stable identifier for routing/diagnostics."""
        ...

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        """Return the raw assistant text for ``prompt`` (no JSON parsing).

        ``tools`` (e.g. ``("Read","Grep","Glob")``) requests GROUNDED mode where
        the backend may read local files itself — honored by claude-code (which
        can Read/Grep), ignored by API backends that have no local file access.
        """
        ...


def _backoff_sleep(attempt: int) -> None:
    time.sleep(min(60.0, 5.0 * (2 ** (attempt - 1))))


# --------------------------------------------------------------------------- #
# Provider 1: Claude Code (`claude -p`) — the default transport                #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ClaudeCodeProvider:
    """Headless ``claude -p`` subprocess provider.

    Uses the caller's Claude Code session auth (no API key). Honors ``--effort``.
    Hardened with exponential-backoff retry on transient exit / rate-limit /
    timeout, since a non-zero exit with empty stderr is the rate-limit signature.

    No default models: ``strong_model`` / ``fast_model`` MUST be specified
    explicitly (in ``config/llm.yaml``). Routing a seam to the Claude Code
    subscription is always a deliberate choice, never an implicit default —
    silently defaulting here is what drained the account.
    """

    name: str
    strong_model: str
    fast_model: str

    def _model(self, tier: str) -> str:
        return self.strong_model if tier == "strong" else self.fast_model

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        model = self._model(tier)
        argv = ["claude", "-p", "--effort", effort, "--output-format", "json", "--model", model]
        if tools:
            # GROUNDED mode: let this isolated process Read/Grep the source files
            # itself (small prompt, file-grounded) instead of embedding huge text.
            argv += ["--allowedTools", ",".join(tools)]
        last: Exception | None = None
        timeouts = 0
        attempt = 0
        max_retries = 4
        while attempt <= max_retries:
            if attempt:
                _backoff_sleep(attempt)
            attempt += 1
            try:
                with _CLAUDE_P_SEM:  # global cap: <=5 concurrent `claude -p` (rate-limit guard)
                    proc = subprocess.run(  # noqa: S603 — fixed argv, prompt via stdin
                        argv,
                        input=prompt,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        check=False,
                    )
            except subprocess.TimeoutExpired:
                timeouts += 1
                last = ProviderError(f"claude -p timed out after {timeout:.0f}s")
                if timeouts >= 2:
                    break
                continue
            if proc.returncode != 0:
                last = ProviderError(f"claude -p exit {proc.returncode}: {proc.stderr[:400]}")
                continue
            try:
                env = json.loads(proc.stdout)
            except json.JSONDecodeError:
                last = ProviderError(f"claude -p non-JSON envelope: {proc.stdout[:200]}")
                continue
            if env.get("is_error"):
                last = ProviderError(f"claude -p error envelope: {str(env.get('result'))[:200]}")
                continue
            return str(env.get("result", ""))
        raise ProviderError(f"{self.name} failed after {attempt} attempt(s): {last}")


# --------------------------------------------------------------------------- #
# Provider 2: generic OpenAI-compatible HTTP API — vendor-agnostic             #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class OpenAICompatibleProvider:
    """ANY OpenAI chat-completions-compatible HTTP backend, defined by config.

    NOT bound to a vendor: OpenCode (deepseek) is one instance; OpenAI, Gemini
    (OpenAI-compat), DeepSeek-direct, Together, a local vLLM, etc. are just other
    ``base_url`` / model / key-env triples. The API key is read from the named
    environment variable (never hard-coded).
    """

    name: str
    base_url: str
    strong_model: str
    fast_model: str
    api_key_env: str
    # Optional OpenAI-style reasoning-effort passthrough; off by default since not
    # every compatible backend accepts it.
    send_reasoning_effort: bool = False
    # Bypass environment proxies (HTTP(S)_PROXY/ALL_PROXY) for this provider's host.
    # Set for internal endpoints that must be reached DIRECT (e.g. a company API
    # behind Clash with a DIRECT rule) while other providers keep using the proxy.
    no_proxy: bool = False

    def _model(self, tier: str) -> str:
        return self.strong_model if tier == "strong" else self.fast_model

    def _api_key(self) -> str:
        key = os.environ.get(self.api_key_env, "").strip()
        if not key:
            raise ProviderError(
                f"{self.name}: env var {self.api_key_env} is unset — set it in .env "
                f"(gitignored) or the environment before routing a seam here"
            )
        return key

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        # `tools` (grounded mode) is ignored: an HTTP API has no access to local
        # files, so grounded extraction is a claude-code-only capability. The
        # caller routes grounded seams to claude-code.
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload: dict = {
            "model": self._model(tier),
            "messages": [{"role": "user", "content": prompt}],
        }
        if self.send_reasoning_effort:
            payload["reasoning_effort"] = effort
        headers = {
            "Authorization": f"Bearer {self._api_key()}",
            "Content-Type": "application/json",
        }
        last: Exception | None = None
        conn_fail = False  # last failure was a connection/proxy drop (longer backoff)
        attempt = 0
        # Big requests (the analyzer's ~90k-char payload) intermittently get the
        # proxy dropped mid-flight; give transport failures a generous budget +
        # longer backoff so a flaky proxy window (~minutes) is spanned, while a
        # bad key/model still fails fast (4xx below).
        max_retries = 7
        while attempt <= max_retries:
            if attempt:
                # Connection/proxy drops back off longer (cap 120s) than HTTP
                # 429/5xx (cap 60s), since the proxy may be down for a while.
                cap, base = (120.0, 8.0) if conn_fail else (60.0, 5.0)
                time.sleep(min(cap, base * (2 ** (attempt - 1))))
            attempt += 1
            try:
                if self.no_proxy:
                    # Ignore env proxies so this host is reached DIRECT (then the OS
                    # routing / Clash DIRECT rule takes it straight to the server).
                    with requests.Session() as sess:
                        sess.trust_env = False
                        resp = sess.post(url, json=payload, headers=headers, timeout=timeout)
                else:
                    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            except requests.RequestException as exc:
                last = ProviderError(f"{self.name} request error: {exc}")
                conn_fail = True
                continue
            conn_fail = False
            if resp.status_code == 429 or resp.status_code >= 500:
                last = ProviderError(f"{self.name} HTTP {resp.status_code}: {resp.text[:200]}")
                continue
            if resp.status_code != 200:
                # 4xx other than 429 = non-transient (bad key/model/request); fail fast.
                raise ProviderError(f"{self.name} HTTP {resp.status_code}: {resp.text[:300]}")
            try:
                data = resp.json()
                msg = data["choices"][0]["message"]
                # Some reasoning backends split content/reasoning; prefer content.
                content = msg.get("content") or msg.get("reasoning_content") or ""
            except (ValueError, KeyError, IndexError) as exc:
                last = ProviderError(f"{self.name} malformed response: {exc}: {resp.text[:200]}")
                continue
            return str(content)
        raise ProviderError(f"{self.name} failed after {attempt} attempt(s): {last}")


# --------------------------------------------------------------------------- #
# Fallback wrapper — the mandatory failure path                                 #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class StrictProvider:
    """A seam's routed provider with NO fallback — fail loud, never degrade.

    On ``ProviderError`` (the wrapped provider already exhausted its own retries)
    this raises :class:`EngineAbort`, which the hub treats as a whole-tick abort
    that surfaces to the operator. There is deliberately **no** fallback to any
    other backend or to the Claude Code subscription: a failing/misconfigured
    provider (bad key, dead endpoint, wrong model) MUST be seen and fixed, not
    silently papered over by quietly draining the main account.

    Single-provider-per-seam today; the periphery is intentionally shaped so a
    future cross-audit can wrap several providers + a judge here instead.
    """

    provider: LLMProvider

    @property
    def name(self) -> str:
        return self.provider.name

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        try:
            return self.provider.complete(
                prompt, tier=tier, effort=effort, timeout=timeout, tools=tools
            )
        except ProviderError as exc:
            raise EngineAbort(
                f"provider {self.provider.name!r} failed and there is NO fallback "
                f"(by design): fix the provider/key/config — the engine will not "
                f"silently fall back to another backend. cause: {exc}"
            ) from exc


# --------------------------------------------------------------------------- #
# Factory                                                                      #
# --------------------------------------------------------------------------- #

_PROVIDER_TYPES = ("claude_code", "openai_compatible")


def build_provider(name: str, spec: dict) -> LLMProvider:
    """Construct a provider from a config spec dict.

    Args:
        name: The provider's config key (its routing identity).
        spec: ``{"type": "claude_code"|"openai_compatible", ...}``. For
            ``openai_compatible``: requires ``base_url``, ``strong_model``,
            ``fast_model``, ``api_key_env``; optional ``send_reasoning_effort``.
            For ``claude_code``: requires ``strong_model`` / ``fast_model``
            (no default — must be specified explicitly).

    Raises:
        ProviderError: unknown type or missing required field.
    """
    ptype = spec.get("type")
    if ptype == "claude_code":
        missing = [k for k in ("strong_model", "fast_model") if not spec.get(k)]
        if missing:
            raise ProviderError(
                f"provider {name!r}: claude_code missing {missing} — models must be "
                f"specified explicitly (no default; routing to the Claude Code "
                f"subscription is always a deliberate choice)"
            )
        return ClaudeCodeProvider(
            name=name,
            strong_model=spec["strong_model"],
            fast_model=spec["fast_model"],
        )
    if ptype == "openai_compatible":
        missing = [
            k for k in ("base_url", "strong_model", "fast_model", "api_key_env") if not spec.get(k)
        ]
        if missing:
            raise ProviderError(f"provider {name!r}: openai_compatible missing {missing}")
        return OpenAICompatibleProvider(
            name=name,
            base_url=spec["base_url"],
            strong_model=spec["strong_model"],
            fast_model=spec["fast_model"],
            api_key_env=spec["api_key_env"],
            send_reasoning_effort=bool(spec.get("send_reasoning_effort", False)),
            no_proxy=bool(spec.get("no_proxy", False)),
        )
    raise ProviderError(
        f"provider {name!r}: unknown type {ptype!r} (expected one of {_PROVIDER_TYPES})"
    )


def load_dotenv(workspace: Path) -> None:
    """Best-effort: load ``<workspace>/.env`` into os.environ (does not override
    already-set vars). Lets API keys live in the gitignored .env file."""
    path = Path(workspace) / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())
