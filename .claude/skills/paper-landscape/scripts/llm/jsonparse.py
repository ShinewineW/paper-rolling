# .claude/skills/paper-landscape/scripts/llm/jsonparse.py
r"""Tolerant JSON extraction from LLM output (shared by every JSON-returning seam).

Models wrap JSON in ```fences``` / prose, and — critically for the analyzer —
emit LaTeX inside JSON strings (``"$\mathbf{w}$"``) where ``\m`` is an INVALID
JSON escape, so ``json.loads`` raises ``Invalid \escape``. The analyzer bundle is
full of ``$$...$$`` math; deepseek mis-escaped it 3/3. ``repair_json_escapes``
doubles any backslash that is not already a valid JSON escape, recovering the
LaTeX as a literal backslash, so a provider that doesn't perfectly escape can
still be parsed (the fallback hardening for non-Claude backends).
"""

from __future__ import annotations

import json
import re

_VALID_ESCAPE = set('"\\/bfnrtu')  # chars that may follow a backslash in JSON
_JSON_SPAN = re.compile(r"(\{.*\}|\[.*\])", re.S)
_FENCE_OPEN = re.compile(r"^```[a-zA-Z]*\n?")
_FENCE_CLOSE = re.compile(r"\n?```\s*$")


def repair_json_escapes(s: str) -> str:
    r"""Double only LONE backslashes that aren't a valid JSON escape.

    Pairwise scan: a valid escape pair (``\\``, ``\"``, ``\n``, ``\uXXXX`` …) is
    kept intact — so ALREADY-escaped LaTeX like ``\\mathbf`` is NOT corrupted — and
    a backslash followed by anything else (e.g. ``\mathbf``) is a stray LaTeX
    backslash and gets doubled to ``\\mathbf``. (A regex doubling every "bad"
    backslash mis-handled ``\\m`` -> ``\\\m`` and broke valid input.)
    """
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "\\":
            nxt = s[i + 1] if i + 1 < n else ""
            if nxt in _VALID_ESCAPE:  # valid escape pair — keep both, skip ahead
                out.append(ch)
                out.append(nxt)
                i += 2
                continue
            out.append("\\\\")  # lone/stray backslash — escape it
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def extract_json(text: str):
    """Parse a JSON value from model output, tolerating fences / prose / invalid
    LaTeX backslash escapes.

    Robust to a GROUNDED claude -p that narrates before the JSON ("Now I have all
    the info. Let me compile.\n\n```json\n{...}```") — a fenced block ANYWHERE and a
    balanced brace span are both tried, each as-is and escape-repaired.

    Raises:
        ValueError: no parseable JSON even after escape repair.
    """
    t = text.strip()
    candidates: list[str] = []
    # 1. A fenced ```json ... ``` (or bare ``` ... ```) block ANYWHERE — handles
    #    prose preamble/postamble around the JSON (grounded tool-use narration).
    fence = re.search(r"```(?:json|JSON)?\s*\n?(.*?)```", t, re.S)
    if fence:
        candidates.append(fence.group(1).strip())
    # 2. A leading fence stripped (back-compat).
    if t.startswith("```"):
        candidates.append(_FENCE_CLOSE.sub("", _FENCE_OPEN.sub("", t)).strip())
    # 3. The raw text.
    candidates.append(t)
    # 4. The first balanced-looking object/array span.
    span = _JSON_SPAN.search(t)
    if span:
        candidates.append(span.group(1))
    for cand in candidates:
        for variant in (cand, repair_json_escapes(cand)):
            try:
                return json.loads(variant)
            except json.JSONDecodeError:
                continue
    raise ValueError(f"JSON parse failed even after escape repair: {text[:300]!r}")
