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

    Raises:
        ValueError: no parseable JSON even after escape repair.
    """
    t = text.strip()
    if t.startswith("```"):
        t = _FENCE_OPEN.sub("", t)
        t = _FENCE_CLOSE.sub("", t).strip()
    # Try as-is, then with LaTeX-backslash repair.
    for candidate in (t, repair_json_escapes(t)):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    # Fallback: first balanced-looking object/array span (also escape-repaired).
    m = _JSON_SPAN.search(t)
    if not m:
        raise ValueError(f"no JSON value found in output: {text[:300]!r}")
    span = m.group(1)
    for candidate in (span, repair_json_escapes(span)):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"JSON parse failed even after escape repair: {text[:300]!r}")
