# .claude/skills/paper-landscape/scripts/llm/config.py
"""Per-seam LLM routing AND execution mode, loaded from ``config/llm.yaml``.

Each seam is finalized as ``{provider, mode}``:

  - **provider** — which backend (``claude-code`` / an ``openai_compatible`` API
    like opencode). Defined in the same file, so a new vendor is a config block.
  - **mode** — HOW it runs:
      * ``inline``     — content embedded in the prompt (default; fits API + small
                         inputs).
      * ``grounded``   — the backend READS the source files itself (Read/Grep) with
                         a small prompt — a LOCAL agent only (claude-code or codex,
                         or a round_robin pool of them; an HTTP API has no local
                         files). Used for the heavy analyzer so it never does an
                         unstable one-shot embed of the whole paper.
      * ``agent_team`` — OPT-IN: the runtime agent dispatches isolated sub-agents
                         (Workflow); their context never enters the main session,
                         which only AGGREGATES results. NOT executable by the
                         synchronous engine — it requires the agent-driven runner.

Default operating state is provider seams (a local agent / an API); agent_team is
only used when the operator selects it. The file is REQUIRED and EVERY seam must be
explicitly routed — there is NO implicit default to ``claude-code`` (an absent file
or an unrouted seam is a hard error; ``load_llm_config`` raises).

A seam entry may be a bare provider string (``writer: opencode`` -> default mode)
or a mapping (``analyzer: {provider: claude-code, mode: grounded}``).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from scripts.llm.providers import (
    LLMProvider,
    StrictProvider,
    build_provider,
    load_dotenv,
)

LLM_CONFIG_REL = Path("config") / "llm.yaml"

SEAMS = ("analyzer", "skeptic", "rigor", "entailment", "expand", "writer", "faithfulness")
# OPTIONAL seams: routed via config like any other (so the backend/key/model is managed
# in one place — config/llm.yaml), but NOT required. An optional seam left unrouted is
# simply OFF — used for fail-soft ENRICHMENT tiers whose absence degrades gracefully
# (e.g. web_search = the T4 long-tail repo-discovery tier in repo_resolve), as opposed
# to the correctness-critical SEAMS whose absence is a hard error.
OPTIONAL_SEAMS = ("web_search",)
VALID_MODES = ("inline", "grounded", "agent_team")

# Per-seam default execution MODE only (the finalized spec). Only the heavy
# analyzer defaults to grounded; the rest are inline. agent_team is never a
# default. NOTE: there is intentionally NO default PROVIDER — every seam must be
# explicitly routed in config/llm.yaml (silent routing to the Claude Code
# subscription is what drained the account).
_DEFAULT_MODES = {
    "analyzer": "grounded",
    "skeptic": "inline",
    "rigor": "inline",
    "entailment": "inline",
    "expand": "inline",
    "writer": "inline",
    "faithfulness": "inline",  # ADR-0012 rev: branch1 「评价」 (c) note-writer (advisory)
}


@dataclass(frozen=True)
class LLMConfig:
    """Resolved providers + per-seam {provider, mode}."""

    providers: dict[str, LLMProvider]
    routing: dict[str, str]
    modes: dict[str, str]

    def for_seam(self, seam: str) -> LLMProvider:
        """Return the provider explicitly routed to ``seam`` (load_llm_config
        guarantees every seam is routed to a defined provider)."""
        name = self.routing[seam]
        return self.providers[name]

    def mode_for(self, seam: str) -> str:
        """Return the execution mode for ``seam`` (inline | grounded | agent_team)."""
        return self.modes.get(seam, _DEFAULT_MODES.get(seam, "inline"))

    def resolve(self, seam: str) -> StrictProvider:
        """The runtime provider for ``seam``: its explicitly-routed provider wrapped
        so a transport failure raises EngineAbort (loud, aborts the tick). There is
        NO fallback — a failing provider stops the engine instead of silently
        degrading to another backend or the Claude Code subscription.
        """
        return StrictProvider(self.for_seam(seam))

    def resolve_optional(self, seam: str) -> StrictProvider | None:
        """Like :meth:`resolve` but returns None when an OPTIONAL seam is not routed
        (the tier is simply OFF). The caller is responsible for fail-soft behavior —
        an enrichment seam must not abort a tick on its own failure."""
        return StrictProvider(self.providers[self.routing[seam]]) if seam in self.routing else None


def _seam_entry(value, default_mode: str) -> tuple[str, str]:
    """Normalize a seam config value (provider string, or {provider, mode}).

    The provider is REQUIRED — there is no default routing. Only the execution
    ``mode`` falls back to ``default_mode``.
    """
    if isinstance(value, str):
        return value, default_mode
    if isinstance(value, dict):
        provider = value.get("provider")
        if not provider:
            raise ValueError("seam entry mapping must include 'provider'")
        return provider, value.get("mode", default_mode)
    raise ValueError(
        f"seam entry must be a provider string or a mapping, got {type(value).__name__}"
    )


def load_llm_config(workspace: Path) -> LLMConfig:
    """Load ``config/llm.yaml``. The file is REQUIRED — there is no implicit
    all-claude-code default. Every seam must be explicitly routed to a provider,
    so that using the Claude Code subscription is always a deliberate choice.

    Raises:
        ValueError: missing file, malformed file, unknown provider type, a seam
            routed to an undefined provider, a seam left unrouted, or an invalid
            mode — fail fast and loud.
    """
    workspace = Path(workspace)
    load_dotenv(workspace)  # surface API keys from the gitignored .env
    path = workspace / LLM_CONFIG_REL
    if not path.exists():
        raise ValueError(
            f"{LLM_CONFIG_REL} not found: every LLM seam must be explicitly routed "
            f"to a provider (there is NO default to the Claude Code subscription). "
            f"Create config/llm.yaml routing all seams: {', '.join(SEAMS)}."
        )

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{LLM_CONFIG_REL} must be a YAML mapping")

    prov_specs = raw.get("providers") or {}
    if not isinstance(prov_specs, dict) or not prov_specs:
        raise ValueError(f"{LLM_CONFIG_REL}: 'providers' must be a non-empty mapping")
    # 2-pass build: leaf providers first, then composites (round_robin) that
    # reference leaves by name. Keeps round_robin member resolution simple.
    providers: dict = {}
    composite = {n: s for n, s in prov_specs.items() if (s or {}).get("type") == "round_robin"}
    for pname, spec in prov_specs.items():
        if pname not in composite:
            providers[pname] = build_provider(pname, spec)
    for pname, spec in composite.items():
        providers[pname] = build_provider(pname, spec, built=providers)

    seams_cfg = raw.get("seams") or {}
    if not isinstance(seams_cfg, dict):
        raise ValueError(f"{LLM_CONFIG_REL}: 'seams' must be a mapping")
    routing: dict[str, str] = {}
    modes: dict[str, str] = {}
    for s in SEAMS:
        entry = seams_cfg.get(s)
        if entry is None:
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} is not routed to any provider — every "
                f"seam must be explicitly routed (no default). Defined providers: "
                f"{sorted(providers)}."
            )
        provider, mode = _seam_entry(entry, _DEFAULT_MODES.get(s, "inline"))
        if provider not in providers:
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} routed to undefined provider {provider!r}; "
                f"defined: {sorted(providers)}"
            )
        if mode not in VALID_MODES:
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} has invalid mode {mode!r}; {VALID_MODES}"
            )
        if mode == "grounded" and not getattr(providers[provider], "grounded_capable", False):
            # grounded needs local file tools (the agent reads the source MD itself).
            # Only a LOCAL agent — or a round_robin pool of agents where EVERY member
            # is grounded-capable — qualifies. An HTTP API (or a pool containing one)
            # is rejected loud so the operator fixes the routing, never silently
            # degrades into a member that cannot read the file.
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} mode=grounded requires a grounded-capable "
                f"provider (a local agent, or a pool whose every member is one); "
                f"{provider!r} is not (an HTTP member cannot read local files)."
            )
        routing[s], modes[s] = provider, mode

    # OPTIONAL seams: routed the same way (one config-managed place for the backend/
    # key/model) but absence is OK — the tier is just OFF. Validate the provider when
    # present; do NOT require it.
    for s in OPTIONAL_SEAMS:
        entry = seams_cfg.get(s)
        if entry is None:
            continue
        provider, mode = _seam_entry(entry, _DEFAULT_MODES.get(s, "inline"))
        if provider not in providers:
            raise ValueError(
                f"{LLM_CONFIG_REL}: optional seam {s!r} routed to undefined provider "
                f"{provider!r}; defined: {sorted(providers)}"
            )
        if mode not in VALID_MODES:
            raise ValueError(
                f"{LLM_CONFIG_REL}: optional seam {s!r} has invalid mode {mode!r}; {VALID_MODES}"
            )
        routing[s], modes[s] = provider, mode
    return LLMConfig(providers=providers, routing=routing, modes=modes)
