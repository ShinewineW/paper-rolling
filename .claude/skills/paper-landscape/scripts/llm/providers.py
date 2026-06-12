# .claude/skills/paper-landscape/scripts/llm/providers.py
"""Pluggable LLM transport providers for the paper-landscape seams.

The engine itself is provider-agnostic: every LLM-backed seam is an injected
callable (see scripts/run_campaign.py). This module supplies the *transport*
behind those callables as swappable PROVIDERS, so the runtime can route each
seam to a different backend WITHOUT touching the engine.

Four provider TYPES ship; none is hard-wired to a vendor:

  - ``claude_code``        — a headless ``claude -p`` subprocess (Claude Code
                             subscription auth, ``--effort``, grounded Read/Grep).
                             A LOCAL agent: ``grounded_capable``. NOT a default.
  - ``codex_cli``          — a headless ``codex exec`` subprocess (Codex/ChatGPT
                             login, no-sandbox so it reads files itself). Also a
                             LOCAL agent: ``grounded_capable``.
  - ``openai_compatible``  — ANY OpenAI-/chat-completions-compatible HTTP API,
                             described by config (base_url + model ids + api-key
                             env var). OpenCode (deepseek) is ONE instance; OpenAI
                             / Gemini(-compat) / a local vLLM are config blocks, not
                             new classes. NOT grounded (no local file access).
  - ``round_robin``        — a COMPOSITE that alternates calls across N member
                             providers, so each member's own cap fills in parallel
                             (e.g. claude + codex → 10-wide). Grounded only if every
                             member is.

GROUNDED capability is explicit per type (``grounded_capable``), not inferred from
a missing ``base_url``: a grounded seam (the analyzer reads the source MD itself)
may route only to a grounded-capable provider — a local agent, or a pool of them.

CONCURRENCY is PER-PROVIDER: each leaf instance owns a semaphore sized to its own
``max_concurrent`` (from config/llm.yaml), so a generous backend can run wide and a
token-expensive one narrow — there is no process-global cap.

A provider exposes one method, ``complete(prompt, *, tier, effort, timeout) ->
str``, returning the raw assistant text (JSON parsing lives in the seam layer).
``tier`` selects the provider's strong/fast model; ``effort`` is honored where the
backend supports it (Claude Code) and ignored otherwise.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Protocol, runtime_checkable

import requests

# EngineAbort lives in the LLM-agnostic core (scripts/paths.py) so the engine/hub
# can recognize it WITHOUT importing this transport layer; re-exported here since
# StrictProvider raises it and seam code imports it from here.
from scripts.paths import EngineAbort

# Default concurrency cap when a provider spec omits `max_concurrent`. Concurrency
# is a PER-PROVIDER concern, NOT a process-global one: each provider INSTANCE owns
# its own semaphore (built in __post_init__, sized to its own `max_concurrent`),
# so every routed provider — claude-code, codex, an HTTP API, a future 3rd/4th
# model — can be given its OWN cap from config/llm.yaml. A cheap/generous backend
# may run wide (e.g. 10); a token-expensive one narrow (e.g. 3). The subprocess
# agents default to 5 (one paper's chunk fan-out — also the claude/codex account
# rate-limit guard); HTTP backends default higher since they have no subprocess
# cost. There is deliberately no module-global semaphore.
_DEFAULT_AGENT_CONCURRENCY = 5
_DEFAULT_API_CONCURRENCY = 8


class ProviderError(RuntimeError):
    """A provider call failed after exhausting its retry budget."""


class _RetryableHTTP(Exception):
    """Internal signal: a transient HTTP outcome (429 / 5xx / empty-or-malformed
    stream / over-budget) that the retry loop should back off and retry — as
    opposed to a non-429 4xx (bad key/model/request), which raises ProviderError
    and fails fast."""


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

    ``max_concurrent`` is this instance's OWN cap (its own semaphore) — the
    account rate-limit guard, settable per provider in config/llm.yaml.
    """

    name: str
    strong_model: str
    fast_model: str
    max_concurrent: int = _DEFAULT_AGENT_CONCURRENCY
    _sem: threading.Semaphore = field(init=False, compare=False, repr=False, default=None)
    cli: ClassVar[str] = "claude"  # preflight presence-checks `which(cli)`
    grounded_capable: ClassVar[bool] = True  # local Read/Grep → can run grounded

    def __post_init__(self) -> None:
        object.__setattr__(self, "_sem", threading.Semaphore(max(1, self.max_concurrent)))

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
                with self._sem:  # this instance's own cap (config max_concurrent)
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
    # This instance's OWN in-flight request cap (its own semaphore). An expensive
    # API can be throttled narrow (e.g. 3); a generous one run wide — per provider,
    # from config/llm.yaml (Goal 3).
    max_concurrent: int = _DEFAULT_API_CONCURRENCY
    # Idle-gap read timeout (seconds): the max SILENCE between streamed SSE chunks
    # before the call is treated as a dead/stalled connection and fails LOUDLY for
    # retry. Responses STREAM, so a slow-but-progressing generation (writer/rigor,
    # minutes long) keeps resetting this gap and is NEVER false-killed by total
    # length — while a hung connection (no bytes, e.g. proxy/endpoint dropped)
    # aborts in ~idle_timeout s instead of stalling for the full `timeout` budget.
    idle_timeout: float = 90.0
    _sem: threading.Semaphore = field(init=False, compare=False, repr=False, default=None)
    grounded_capable: ClassVar[bool] = False  # HTTP API: no local file access → no grounded

    def __post_init__(self) -> None:
        object.__setattr__(self, "_sem", threading.Semaphore(max(1, self.max_concurrent)))

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
        # files, so grounded extraction is a LOCAL-agent capability (claude-code /
        # codex). The routing layer (grounded_capable) keeps grounded seams off
        # this provider, so `tools` never arrives meaningfully here.
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
                return self._stream_completion(url, payload, headers, timeout)
            except requests.RequestException as exc:
                # Transport-level: connect drop, OR an idle-gap read timeout (no SSE
                # chunk for idle_timeout s = a stalled/dead connection). Retry.
                last = ProviderError(f"{self.name} request error: {exc}")
                conn_fail = True
                continue
            except _RetryableHTTP as exc:
                # 429 / 5xx / malformed-or-empty stream: transient, retry.
                last = ProviderError(str(exc))
                conn_fail = False
                continue
            # A 4xx other than 429 (bad key/model/request) raises ProviderError from
            # _stream_completion and propagates here — non-transient, fail fast.
        raise ProviderError(f"{self.name} failed after {attempt} attempt(s): {last}")

    def _stream_completion(self, url: str, payload: dict, headers: dict, timeout: float) -> str:
        """One streaming attempt. The response is consumed as an SSE stream so the
        ``(connect, idle)`` read timeout bounds SILENCE BETWEEN CHUNKS, not total
        time: a dead connection aborts in ~idle_timeout s while a long-but-flowing
        generation is never false-killed. `timeout` is an overall wall-clock cap.

        Returns the assembled content. Raises ``requests.RequestException`` on
        transport failure (incl. idle-gap timeout), ``_RetryableHTTP`` on
        429/5xx/empty-or-malformed stream, and ``ProviderError`` (fail-fast) on a
        non-429 4xx.
        """
        body = {**payload, "stream": True}
        read_to = (min(30.0, timeout), self.idle_timeout)  # (connect, idle-gap)
        deadline = time.monotonic() + timeout

        def _go(poster) -> str:
            with poster(url, json=body, headers=headers, stream=True, timeout=read_to) as resp:
                if resp.status_code == 429 or resp.status_code >= 500:
                    raise _RetryableHTTP(f"{self.name} HTTP {resp.status_code}: {resp.text[:200]}")
                if resp.status_code != 200:
                    raise ProviderError(f"{self.name} HTTP {resp.status_code}: {resp.text[:300]}")
                return self._consume_sse(resp, deadline)

        with self._sem:  # this instance's own in-flight cap (config max_concurrent)
            if self.no_proxy:
                # Ignore env proxies so this host is reached DIRECT (then the OS
                # routing / Clash DIRECT rule takes it straight to the server).
                with requests.Session() as sess:
                    sess.trust_env = False
                    return _go(sess.post)
            return _go(requests.post)

    def _consume_sse(self, resp: requests.Response, deadline: float) -> str:
        """Assemble streamed `data: {delta}` chunks into the full content. An
        overall-budget guard caps a slow trickle; per-chunk silence is bounded by
        the socket read timeout (raises RequestException, handled by the caller)."""
        # SSE frames are UTF-8, but `text/event-stream` rarely carries an explicit
        # charset, so requests defaults `resp.encoding` to ISO-8859-1 (RFC 2616) →
        # `iter_lines(decode_unicode=True)` then decodes CJK as latin-1 and the whole
        # Chinese report comes back as mojibake (e.g. 用户 → `ç¨æ·`). Pin UTF-8 so
        # the decode is correct regardless of the server's (missing) charset header.
        resp.encoding = "utf-8"
        parts: list[str] = []
        for raw in resp.iter_lines(decode_unicode=True):
            if time.monotonic() > deadline:
                raise _RetryableHTTP(f"{self.name} exceeded overall budget mid-stream")
            if not raw:
                continue
            line = raw.strip()
            if not line.startswith("data:"):
                continue
            chunk = line[len("data:") :].strip()
            if chunk == "[DONE]":
                break
            try:
                delta = json.loads(chunk)["choices"][0].get("delta", {})
            except (ValueError, KeyError, IndexError):
                continue  # keep-alive / usage-only / comment frame
            piece = delta.get("content") or delta.get("reasoning_content") or ""
            if piece:
                parts.append(piece)
        content = "".join(parts)
        if not content:
            raise _RetryableHTTP(f"{self.name} empty stream")
        return content


# --------------------------------------------------------------------------- #
# Provider 3: Codex CLI (`codex exec`) — local agent, grounded-capable          #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class CodexCliProvider:
    """Headless ``codex exec`` subprocess provider — a LOCAL agent like
    ``claude_code``, but on the Codex CLI (Codex/ChatGPT login, no API key).

    Runs with ``--dangerously-bypass-approvals-and-sandbox`` so the non-interactive
    agent (a) reads source files itself — GROUNDED, the equal of claude-code's
    Read/Grep — and (b) never blocks on an approval prompt. The final agent message
    is captured via ``-o <file>`` and returned RAW (JSON parsing lives in the seam
    layer), mirroring :class:`ClaudeCodeProvider`. NOT a default: a seam reaches it
    only when explicitly routed here.

    ``model`` is OPTIONAL: empty string lets the Codex CLI use its own configured
    default model (the codex convention). ``reasoning_effort`` (minimal|low|medium|
    high|xhigh) overrides the codex config default per call via ``-c
    model_reasoning_effort=…`` — scoped to THIS provider, NOT the user's global
    ~/.codex/config.toml. For grounded EXTRACTION the global xhigh default is wildly
    slow (150–366s/chunk); medium/low cuts it and reduces the variance. ``tier`` is
    ignored (single model); ``tools`` is ignored — codex always has its own file
    tools, and the grounded prompt names the path to read. ``max_concurrent`` is this
    instance's OWN cap; ``grounded_capable`` is True.
    """

    name: str
    model: str = ""  # "" => codex CLI default model
    reasoning_effort: str = ""  # "" => codex config default; else -c model_reasoning_effort
    max_concurrent: int = _DEFAULT_AGENT_CONCURRENCY
    _sem: threading.Semaphore = field(init=False, compare=False, repr=False, default=None)
    cli: ClassVar[str] = "codex"  # preflight checks `which(cli)` for local providers
    grounded_capable: ClassVar[bool] = True  # bypassed-sandbox agent reads files itself

    def __post_init__(self) -> None:
        object.__setattr__(self, "_sem", threading.Semaphore(max(1, self.max_concurrent)))

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        argv = ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-C", os.getcwd()]
        if self.model:
            argv += ["-m", self.model]
        if self.reasoning_effort:
            argv += ["-c", f"model_reasoning_effort={self.reasoning_effort}"]
        last: Exception | None = None
        attempt = 0
        max_retries = 4
        while attempt <= max_retries:
            if attempt:
                _backoff_sleep(attempt)
            attempt += 1
            fd, out_path = tempfile.mkstemp(prefix="codex_out_", suffix=".txt")
            os.close(fd)
            try:
                with self._sem:  # this instance's own cap (config max_concurrent)
                    proc = subprocess.run(  # noqa: S603 — fixed argv, prompt via stdin
                        [*argv, "-o", out_path],
                        input=prompt,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        check=False,
                    )
                if proc.returncode != 0:
                    last = ProviderError(f"codex exec exit {proc.returncode}: {proc.stderr[-400:]}")
                    continue
                result = Path(out_path).read_text(encoding="utf-8")
                if not result.strip():
                    last = ProviderError("codex exec produced an empty final message")
                    continue
                return result
            except subprocess.TimeoutExpired:
                last = ProviderError(f"codex exec timed out after {timeout:.0f}s")
                continue
            finally:
                try:
                    os.unlink(out_path)
                except OSError:
                    pass
        raise ProviderError(f"{self.name} failed after {attempt} attempt(s): {last}")


# --------------------------------------------------------------------------- #
# Composite: round-robin across local agent providers (claude + codex)          #
# --------------------------------------------------------------------------- #


class RoundRobinProvider:
    """Alternate each ``complete()`` call across N member providers (thread-safe).

    Lets the analyzer's chunk fan-out (and parallel papers) spread across several
    backends — e.g. claude-code + codex — so each member's OWN semaphore (its
    per-instance ``max_concurrent``) fills independently and total concurrency is
    the SUM of the members' caps (e.g. 5 claude + 5 codex = 10) instead of one
    backend's 5. Members are assumed interchangeable in quality (operator's
    explicit choice). NOT frozen: it holds a rotating index behind a lock.

    Capability is derived from the members, NOT faked: ``grounded_capable`` is True
    only when EVERY member is grounded-capable, so a pool with an HTTP member is
    correctly rejected for a grounded seam. ``members`` exposes them so preflight
    recurses into each (agent → presence-check its CLI; HTTP → key/liveness).
    ``member_clis`` reports only the agent members' CLI binaries.
    """

    def __init__(self, name: str, members: tuple[LLMProvider, ...]) -> None:
        if not members:
            raise ProviderError(f"round_robin provider {name!r}: needs >= 1 member")
        self.name = name
        self._members = members
        self._lock = threading.Lock()
        self._i = 0

    @property
    def members(self) -> tuple[LLMProvider, ...]:
        """The pool's member providers (for recursive preflight / validation)."""
        return self._members

    @property
    def grounded_capable(self) -> bool:
        """True only if EVERY member can run grounded (local file access). A pool
        containing an HTTP member is NOT grounded-capable — the routing layer uses
        this to reject it for a grounded seam instead of silently letting an HTTP
        member fail to read the source file."""
        return all(getattr(m, "grounded_capable", False) for m in self._members)

    @property
    def member_clis(self) -> tuple[str, ...]:
        # Distinct CLI binaries of the AGENT members only (e.g. ("claude", "codex")).
        # HTTP members have no `cli` and are presence-checked differently (by key/
        # liveness in preflight via `members`), so they are NOT defaulted to claude.
        seen: list[str] = []
        for m in self._members:
            cli = getattr(m, "cli", None)
            if cli and cli not in seen:
                seen.append(cli)
        return tuple(seen)

    def _next(self) -> LLMProvider:
        with self._lock:
            m = self._members[self._i % len(self._members)]
            self._i += 1
            return m

    def complete(
        self,
        prompt: str,
        *,
        tier: str = "strong",
        effort: str = "high",
        timeout: float = 900.0,
        tools: tuple[str, ...] | None = None,
    ) -> str:
        return self._next().complete(prompt, tier=tier, effort=effort, timeout=timeout, tools=tools)


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

_PROVIDER_TYPES = ("claude_code", "openai_compatible", "codex_cli", "round_robin")


def build_provider(
    name: str, spec: dict, *, built: dict[str, LLMProvider] | None = None
) -> LLMProvider:
    """Construct a provider from a config spec dict.

    Args:
        name: The provider's config key (its routing identity).
        spec: ``{"type": "claude_code"|"openai_compatible"|"codex_cli"|"round_robin",
            ...}``. For ``openai_compatible``: requires ``base_url``, ``strong_model``,
            ``fast_model``, ``api_key_env``; optional ``send_reasoning_effort``.
            For ``claude_code``: requires ``strong_model`` / ``fast_model``
            (no default — must be specified explicitly). For ``codex_cli``: optional
            ``model``. For ``round_robin``: ``members`` (a list of OTHER provider
            names), resolved from ``built``.
        built: already-constructed providers, for ``round_robin`` member resolution
            (a 2-pass build: leaves first, then composites).

    Every leaf provider also takes an optional ``max_concurrent`` (its OWN cap —
    a per-instance semaphore). ``round_robin`` takes no cap: each member self-limits
    with its own, so the pool's total is the sum of the members' caps.

    Raises:
        ProviderError: unknown type, missing required field, an unresolved member,
            or a non-positive ``max_concurrent``.
    """
    ptype = spec.get("type")

    def _max_concurrent(default: int) -> int:
        v = spec.get("max_concurrent", default)
        if not isinstance(v, int) or isinstance(v, bool) or v < 1:
            raise ProviderError(
                f"provider {name!r}: max_concurrent must be a positive integer, got {v!r}"
            )
        return v

    if ptype == "round_robin":
        member_names = spec.get("members") or []
        if not isinstance(member_names, list) or not member_names:
            raise ProviderError(f"provider {name!r}: round_robin needs a non-empty 'members' list")
        pool = built or {}
        missing = [m for m in member_names if m not in pool]
        if missing:
            raise ProviderError(
                f"provider {name!r}: round_robin members {missing} are not defined "
                f"(define them as providers; members must precede composites)"
            )
        return RoundRobinProvider(name=name, members=tuple(pool[m] for m in member_names))
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
            max_concurrent=_max_concurrent(_DEFAULT_AGENT_CONCURRENCY),
        )
    if ptype == "codex_cli":
        # No required fields: `model` is optional (empty => codex CLI default).
        # Auth is the local Codex login; there is no api_key_env to validate.
        return CodexCliProvider(
            name=name,
            model=spec.get("model") or "",
            reasoning_effort=spec.get("reasoning_effort") or "",
            max_concurrent=_max_concurrent(_DEFAULT_AGENT_CONCURRENCY),
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
            idle_timeout=float(spec.get("idle_timeout", 90.0)),
            max_concurrent=_max_concurrent(_DEFAULT_API_CONCURRENCY),
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
