"""code_ref repo resolution — ordered candidate cascade (分析-D1).

Generates an ORDERED list of repo candidates for a paper; `build_code_ref` then
clone-verifies them in order and the first ACCEPTED one wins. Authority order:

  T1  paper-text   — github links the authors wrote in the frozen MD (verify:
                     could also be a cited baseline's repo, so it is not trusted blindly)
  T2a pwc-official — Papers-with-Code `is_official` offline table (high trust)
  discovery        — a github_repo carried by a discovery source, if any (verify)

T2b (HF live) and T4 (websearch) are Phase 2: they add injected seams to this
function without changing its callers (kwargs-only, defaulted).

Candidate GENERATION lives here (pure + offline); candidate VERIFICATION (clone +
match) lives in build_code_ref — the two concerns are deliberately split.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from scripts.output.pwc_lookup import official_repo as _pwc_official_repo

# github.com/<owner>/<repo> (also git@github.com:owner/repo). Captures owner/repo
# and stops at the next '/', so .../tree/main and .../blob/... keep just owner/repo.
_GH = re.compile(r"github\.com[/:]([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)")
_ARXIV_VERSION = re.compile(r"v\d+$")

# Author-declared closed-source cues. HIGH-PRECISION on purpose: the bug being
# fixed is the OPPOSITE (labelling 'not found' as 'closed-source'), so closed is
# only ever inferred from an explicit statement, never from absence of a link.
_CLOSED = re.compile(
    r"(?i)(?:"
    r"code\s+(?:is\s+|will\s+)?not\s+(?:be\s+)?(?:released|made\s+public|publicly\s+available)"
    r"|do\s+not\s+(?:plan\s+to\s+)?release\s+(?:the\s+|our\s+)?code"
    r"|proprietary\s+(?:code|model|implementation)"
    r")"
)


@dataclass(frozen=True)
class RepoCandidate:
    """One repo candidate to clone-verify.

    Attributes:
        url: Canonical ``https://github.com/owner/repo``.
        source: Where it came from (paper-text / pwc-official / discovery / ...).
        trust: ``"official"`` → accept on clone success; ``"search"`` → require a
            verification match (innovation symbol located, or arxiv_id/title in repo).
    """

    url: str
    source: str
    trust: str


def _to_repo_url(raw: str | None) -> str | None:
    """Normalize any github reference to ``https://github.com/owner/repo``, else None."""
    if not raw:
        return None
    m = _GH.search(raw)
    if not m:
        return None
    # The char class allows '.'/'-' (real in repo names like cosmos-predict2.5),
    # so a trailing sentence period/bracket gets captured — strip such punctuation.
    slug = m.group(1).rstrip("/").rstrip(".,;:)]}'\"")
    if slug.endswith(".git"):
        slug = slug[:-4]
    return f"https://github.com/{slug}"


def _grep_md_github(md_path: Path) -> list[str]:
    """Ordered, de-duplicated github repo URLs referenced in the frozen MD."""
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    out: list[str] = []
    seen: set[str] = set()
    for m in _GH.finditer(text):
        url = _to_repo_url(m.group(0))
        if url and url not in seen:
            seen.add(url)
            out.append(url)
    return out


def author_declares_closed(md_path: Path | None) -> bool:
    """True only on an explicit 'code will not be released' style statement.

    Deliberately conservative — never infer closed-source from a missing link.
    """
    if md_path is None or not Path(md_path).exists():
        return False
    return bool(_CLOSED.search(Path(md_path).read_text(encoding="utf-8", errors="ignore")))


def _default_http_get_json(url: str, headers: dict[str, str]) -> dict:
    """Stdlib GET → parsed JSON dict (injectable for tests)."""
    req = urllib.request.Request(url, headers=headers)  # noqa: S310 (https only, below)
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
        return json.load(resp)


def hf_official_repo(
    arxiv_id: str | None,
    *,
    http_get: Callable[[str, dict[str, str]], dict] = _default_http_get_json,
) -> str | None:
    """T2b — the repo HF Papers links for `arxiv_id` (live), or None.

    Covers papers added after the PwC freeze. The link is HF-`auto`-added and may
    be a reimplementation, so it enters the cascade as a "search" candidate (the
    clone-verification gate confirms it). Network/parse failures degrade to None.
    """
    if not arxiv_id:
        return None
    from scripts.discovery.hf_papers import _hf_headers

    key = _ARXIV_VERSION.sub("", arxiv_id.strip())
    try:
        data = http_get(f"https://huggingface.co/api/papers/{key}", _hf_headers())
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None
    repo = data.get("githubRepo") if isinstance(data, dict) else None
    return repo or None


def resolve_repo_candidates(
    arxiv_id: str | None,
    md_path: Path | None,
    candidate: dict,
    *,
    pwc_lookup: Callable[[str | None], str | None] = _pwc_official_repo,
    hf_lookup: Callable[[str | None], str | None] | None = None,
    web_search: Callable[[str], list[str]] | None = None,
) -> list[RepoCandidate]:
    """Ordered, de-duplicated repo candidates (T1 → T2a → discovery → T2b → T4).

    T2b (`hf_lookup`) and T4 (`web_search`) are injected by the driver and OFF by
    default — so the pure path (and every unit test) never touches the network.
    """
    out: list[RepoCandidate] = []
    seen: set[str] = set()

    def add(raw: str | None, source: str, trust: str) -> None:
        url = _to_repo_url(raw)
        if url and url not in seen:
            seen.add(url)
            out.append(RepoCandidate(url=url, source=source, trust=trust))

    # T1 — links the authors wrote in the paper (verify; may be a baseline repo).
    if md_path is not None and Path(md_path).exists():
        for url in _grep_md_github(Path(md_path)):
            add(url, "paper-text", "search")
    # T2a — Papers-with-Code is_official offline table (high trust).
    add(pwc_lookup(arxiv_id), "pwc-official", "official")
    # A repo a discovery source already carried (e.g. HF Papers); verify.
    add(candidate.get("github_repo"), "discovery", "search")
    # T2b — HF live (post-PwC-freeze papers); injected, verify.
    if hf_lookup is not None:
        add(hf_lookup(arxiv_id), "hf-live", "search")
    # T4 — websearch long-tail; injected. The seam returns result strings; we
    # extract github repo URLs from them (driver does the actual search).
    if web_search is not None:
        title = candidate.get("title") or ""
        query = f"{title} {arxiv_id or ''} official code github".strip()
        for result in web_search(query):
            for m in _GH.finditer(result or ""):
                add(m.group(0), "websearch", "search")
    return out


def make_repo_resolver(*, web_search: Callable[[str], list[str]] | None = None) -> Callable:
    """Compose the PRODUCTION code_ref resolver for the driver to inject.

    Wires T1+T2a (always) + **T2b HF-live on by default** (deterministic, free) +
    **T4 only when `web_search` is supplied** (an Agent WebSearch invocation that
    returns result strings). Pass the result as `run_campaign(repo_resolver=...)`.
    Unit tests use the bare `resolve_repo_candidates` instead, so they stay offline.
    """
    return partial(resolve_repo_candidates, hf_lookup=hf_official_repo, web_search=web_search)
