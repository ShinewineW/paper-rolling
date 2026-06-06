"""LLM query expansion + OpenAlex topic anchoring (D-发现-6).

Net-new (CC-BY-NC repo). The LLM (injected callable) is the primary recall driver: it
explodes a domain into canonical phrasing + sub-topics + known method names +
synonyms. HF ai_keywords feed a free second expansion round. OpenAlex
topics/concepts ID anchoring adds precision (resolve_topic_id; note OpenAlex
2024 migrated concepts->topics, so we hit /topics).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_EXPANSION_PROMPT = (
    "Expand the research domain below into a focused list of search queries "
    "for academic paper discovery. Include: the canonical phrasing, key "
    "sub-topics, known method/model names, and common synonyms. Return one "
    "query per line, no numbering.\n\nDomain: {topic}"
)


def expand_queries(
    topic: str,
    llm: Callable[[str], list[str]],
    ai_keywords: list[str] | None = None,
) -> list[str]:
    """Return a deduped, blank-stripped query list including the seed topic.

    Args:
        topic: the seed domain string.
        llm: callable taking a prompt, returning a list of query strings.
        ai_keywords: optional HF ai_keywords for a free second expansion round.
    """
    raw: list[str] = [topic]
    raw.extend(llm(_EXPANSION_PROMPT.format(topic=topic)))
    if ai_keywords:
        raw.extend(ai_keywords)
    seen: set[str] = set()
    out: list[str] = []
    for q in raw:
        cleaned = q.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        out.append(cleaned)
    return out


def resolve_topic_id(topic: str, openalex_client: Any) -> str | None:
    """Resolve a topic string to an OpenAlex topics id (e.g. 'T10044'), or None.

    OpenAlex 2024 migrated concepts -> topics; we anchor on the /topics search.
    """
    page = openalex_client.get_json(
        "https://api.openalex.org/topics", {"search": topic, "per_page": "1"}
    )
    results = page.get("results") or []
    if not results:
        return None
    full_id = results[0].get("id") or ""
    return full_id.rsplit("/", 1)[-1] or None
