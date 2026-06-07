"""Pluggable LLM provider + per-seam routing layer (runtime seam construction).

Not imported by the pure engine (which stays provider-agnostic via injected
callables); this is the runtime's transport kit. See providers.py / config.py.
"""

from scripts.llm.config import SEAMS, LLMConfig, load_llm_config
from scripts.llm.providers import (
    ClaudeCodeProvider,
    EngineAbort,
    FallbackProvider,
    LLMProvider,
    OpenAICompatibleProvider,
    ProviderError,
    build_provider,
    load_dotenv,
)

__all__ = [
    "SEAMS",
    "ClaudeCodeProvider",
    "EngineAbort",
    "FallbackProvider",
    "LLMConfig",
    "LLMProvider",
    "OpenAICompatibleProvider",
    "ProviderError",
    "build_provider",
    "load_dotenv",
    "load_llm_config",
]
