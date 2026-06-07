# .claude/skills/paper-landscape/scripts/llm/config.py
"""Per-seam LLM routing AND execution mode, loaded from ``config/llm.yaml``.

Each seam is finalized as ``{provider, mode}``:

  - **provider** — which backend (``claude-code`` / an ``openai_compatible`` API
    like opencode). Defined in the same file, so a new vendor is a config block.
  - **mode** — HOW it runs:
      * ``inline``     — content embedded in the prompt (default; fits API + small
                         inputs).
      * ``grounded``   — the backend READS the source files itself (Read/Grep) with
                         a small prompt — claude-code only (an HTTP API has no local
                         files). Used for the heavy analyzer so it never does an
                         unstable one-shot embed of the whole paper.
      * ``agent_team`` — OPT-IN: the runtime agent dispatches isolated sub-agents
                         (Workflow); their context never enters the main session,
                         which only AGGREGATES results. NOT executable by the
                         synchronous engine — it requires the agent-driven runner.

Default operating state is provider seams (claude-code / API); agent_team is only
used when the operator selects it. The file is OPTIONAL — absent, every seam is
``claude-code`` / its default mode.

A seam entry may be a bare provider string (``writer: opencode`` -> default mode)
or a mapping (``analyzer: {provider: claude-code, mode: grounded}``).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from scripts.llm.providers import LLMProvider, build_provider, load_dotenv

LLM_CONFIG_REL = Path("config") / "llm.yaml"

SEAMS = ("analyzer", "skeptic", "rigor", "entailment", "expand", "writer")
VALID_MODES = ("inline", "grounded", "agent_team")

_DEFAULT_PROVIDER = "claude-code"
# Per-seam default execution mode (the finalized spec). Only the heavy analyzer
# defaults to grounded; the rest are inline. agent_team is never a default.
_DEFAULT_MODES = {
    "analyzer": "grounded",
    "skeptic": "inline",
    "rigor": "inline",
    "entailment": "inline",
    "expand": "inline",
    "writer": "inline",
}


@dataclass(frozen=True)
class LLMConfig:
    """Resolved providers + per-seam {provider, mode}."""

    providers: dict[str, LLMProvider]
    routing: dict[str, str]
    modes: dict[str, str]

    def for_seam(self, seam: str) -> LLMProvider:
        """Return the provider routed to ``seam`` (falls back to the default)."""
        name = self.routing.get(seam, _DEFAULT_PROVIDER)
        if name not in self.providers:
            raise KeyError(
                f"seam {seam!r} routed to unknown provider {name!r}; "
                f"defined providers: {sorted(self.providers)}"
            )
        return self.providers[name]

    def mode_for(self, seam: str) -> str:
        """Return the execution mode for ``seam`` (inline | grounded | agent_team)."""
        return self.modes.get(seam, _DEFAULT_MODES.get(seam, "inline"))


def _default_config() -> LLMConfig:
    return LLMConfig(
        providers={_DEFAULT_PROVIDER: build_provider(_DEFAULT_PROVIDER, {"type": "claude_code"})},
        routing={s: _DEFAULT_PROVIDER for s in SEAMS},
        modes=dict(_DEFAULT_MODES),
    )


def _seam_entry(value, default_provider: str, default_mode: str) -> tuple[str, str]:
    """Normalize a seam config value (string provider, or {provider, mode})."""
    if value is None:
        return default_provider, default_mode
    if isinstance(value, str):
        return value, default_mode
    if isinstance(value, dict):
        return value.get("provider", default_provider), value.get("mode", default_mode)
    raise ValueError(f"seam entry must be a string or a mapping, got {type(value).__name__}")


def load_llm_config(workspace: Path) -> LLMConfig:
    """Load ``config/llm.yaml`` (or the all-claude-code default if absent).

    Raises:
        ValueError: malformed file, unknown provider type, a seam routed to an
            undefined provider, or an invalid mode — fail fast.
    """
    workspace = Path(workspace)
    load_dotenv(workspace)  # surface API keys from the gitignored .env
    path = workspace / LLM_CONFIG_REL
    if not path.exists():
        return _default_config()

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{LLM_CONFIG_REL} must be a YAML mapping")

    prov_specs = raw.get("providers") or {}
    if not isinstance(prov_specs, dict) or not prov_specs:
        raise ValueError(f"{LLM_CONFIG_REL}: 'providers' must be a non-empty mapping")
    prov_specs.setdefault(_DEFAULT_PROVIDER, {"type": "claude_code"})
    providers = {name: build_provider(name, spec) for name, spec in prov_specs.items()}

    seams_cfg = raw.get("seams") or {}
    if not isinstance(seams_cfg, dict):
        raise ValueError(f"{LLM_CONFIG_REL}: 'seams' must be a mapping")
    routing: dict[str, str] = {}
    modes: dict[str, str] = {}
    for s in SEAMS:
        provider, mode = _seam_entry(
            seams_cfg.get(s), _DEFAULT_PROVIDER, _DEFAULT_MODES.get(s, "inline")
        )
        if provider not in providers:
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} routed to undefined provider {provider!r}; "
                f"defined: {sorted(providers)}"
            )
        if mode not in VALID_MODES:
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} has invalid mode {mode!r}; {VALID_MODES}"
            )
        if (
            mode == "grounded"
            and providers[provider].name != "claude-code"
            and (getattr(providers[provider], "base_url", None) is not None)
        ):
            # grounded needs local file tools; an HTTP API can't. Fail fast so the
            # operator fixes the routing rather than silently degrading.
            raise ValueError(
                f"{LLM_CONFIG_REL}: seam {s!r} mode=grounded requires a claude-code "
                f"provider (local Read/Grep); {provider!r} is an HTTP API."
            )
        routing[s], modes[s] = provider, mode
    return LLMConfig(providers=providers, routing=routing, modes=modes)
