"""code_ref repo resolution — ordered candidate cascade (分析-D1).

Generates an ORDERED list of repo candidates for a paper; `build_code_ref` then
clone-verifies them in order and the first ACCEPTED one wins. Authority order is
HIGHEST-TRUST-FIRST (the curated official repo must beat an unverified paper-text
link — see resolve_repo_candidates for why):

  T2a pwc-official — Papers-with-Code `is_official` offline table (high trust)
  T1  paper-text   — github links the authors wrote in the frozen MD (verify:
                     could also be a cited baseline's repo, so it is not trusted blindly)
  discovery        — a github_repo carried by a discovery source, if any (verify)
  T2b hf-live      — the repo (or, soon, artifacts) HF Papers links; injected `hf_lookup`,
                     ON by default in make_repo_resolver
  T4  websearch    — long-tail recovery; injected `web_search` seam (config/llm.yaml →
                     a fresh sub-agent WebSearch). ONLY fires when every higher tier
                     came up empty (cost-correct), and is FAIL-SOFT. This is the tier
                     that recovers repos the PwC freeze + a project-page-only paper + an
                     HF-no-githubRepo paper would otherwise miss (e.g. FastWAM).

Both T2b and T4 are injected seams (kwargs-only, defaulted) so they add to this
function without changing its pure/offline callers.

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


def hf_linked_artifacts(
    arxiv_id: str | None,
    *,
    http_get: Callable[[str, dict[str, str]], dict] = _default_http_get_json,
) -> list[tuple[str, str]]:
    """T2b (broadened) — HF artifacts (models / datasets / spaces) the paper page links,
    as ``(kind, url)`` pairs in that priority. HF auto-links these; a paper can ship its
    OFFICIAL weights/data here with NO ``githubRepo`` field at all (e.g. FastWAM:
    yuanty/fastwam model + yuanty/robotwin2.0-fastwam dataset). Reading only ``githubRepo``
    threw these away — surfacing them keeps 'no github repo' from reading as 'no
    code/artifacts'. Network/parse failure degrades to []."""
    if not arxiv_id:
        return []
    from scripts.discovery.hf_papers import _hf_headers

    key = _ARXIV_VERSION.sub("", arxiv_id.strip())
    try:
        data = http_get(f"https://huggingface.co/api/papers/{key}", _hf_headers())
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    out: list[tuple[str, str]] = []
    for kind, field, prefix in (
        ("model", "linkedModels", "https://huggingface.co/"),
        ("dataset", "linkedDatasets", "https://huggingface.co/datasets/"),
        ("space", "linkedSpaces", "https://huggingface.co/spaces/"),
    ):
        for item in data.get(field) or []:
            hid = item.get("id") if isinstance(item, dict) else None
            if hid:
                out.append((kind, f"{prefix}{hid}"))
    return out


def resolve_repo_candidates(
    arxiv_id: str | None,
    md_path: Path | None,
    candidate: dict,
    *,
    pwc_lookup: Callable[[str | None], str | None] = _pwc_official_repo,
    hf_lookup: Callable[[str | None], str | None] | None = None,
    hf_artifacts: Callable[[str | None], list[tuple[str, str]]] | None = None,
    web_search: Callable[[str], list[str]] | None = None,
) -> list[RepoCandidate]:
    """Ordered, de-duplicated repo candidates, HIGHEST TRUST FIRST: T2a pwc-official
    → T1 paper-text → discovery → T2b hf-live → T4 websearch.

    Order matters: build_code_ref accepts the FIRST candidate that verifies, so the
    curated `is_official` repo must be tried BEFORE the paper-text grep — a paper's
    text lists its own repo AND cited-baseline repos indistinguishably, and a
    baseline that cites this paper's arxiv id would otherwise verify and win over the
    real official repo (observed: Cosmos-WFM's text → NVlabs/TokenBench beating
    nvidia-cosmos/cosmos-predict1). T2b (`hf_lookup`) / T4 (`web_search`) are injected
    by the driver and OFF by default — the pure path never touches the network.
    """
    out: list[RepoCandidate] = []
    seen: set[str] = set()

    def add(raw: str | None, source: str, trust: str) -> None:
        url = _to_repo_url(raw)
        if url and url not in seen:
            seen.add(url)
            out.append(RepoCandidate(url=url, source=source, trust=trust))

    # T2a — Papers-with-Code is_official offline table (high trust): tried FIRST so a
    # curated official repo beats an unverified paper-text link (see docstring).
    add(pwc_lookup(arxiv_id), "pwc-official", "official")
    # T1 — links the authors wrote in the paper (verify; may be a cited baseline).
    if md_path is not None and Path(md_path).exists():
        for url in _grep_md_github(Path(md_path)):
            add(url, "paper-text", "search")
    # A repo a discovery source already carried (e.g. HF Papers); verify.
    add(candidate.get("github_repo"), "discovery", "search")
    # T2b — HF live (post-PwC-freeze papers); injected, verify.
    if hf_lookup is not None:
        add(hf_lookup(arxiv_id), "hf-live", "search")
    # T4 — websearch long-tail; injected. ONLY fires when every higher-trust tier came
    # up empty (cost-correct: one websearch sub-agent per UNRESOLVED paper, not per
    # paper — a paper already resolved by PwC/paper-text/HF never pays the search). This
    # is the tier that recovers repos PwC's frozen table + a project-page-only paper +
    # an HF-no-githubRepo paper would otherwise miss (e.g. FastWAM). The seam returns
    # result strings; we extract repo URLs from them (the driver does the actual search).
    if web_search is not None and not out:
        title = candidate.get("title") or ""
        query = f"{title} {arxiv_id or ''} official code github".strip()
        for result in web_search(query):
            for m in _GH.finditer(result or ""):
                add(m.group(0), "websearch", "search")
    # HF linked artifacts (models/datasets/spaces): surfaced ALWAYS — even when a github
    # repo was found, the official weights/data are relevant code semantics ("read all of
    # HF, not just githubRepo"). NOT clone-verified github repos → trust="artifact", which
    # build_code_ref renders in a separate "Linked artifacts" section. Not gated on `out`.
    if hf_artifacts is not None:
        for kind, url in hf_artifacts(arxiv_id):
            if url and url not in seen:
                seen.add(url)
                out.append(RepoCandidate(url=url, source=f"hf-{kind}", trust="artifact"))
    return out


def make_repo_resolver(*, web_search: Callable[[str], list[str]] | None = None) -> Callable:
    """Compose the PRODUCTION code_ref resolver for the driver to inject.

    Wires T1+T2a (always) + **T2b HF-live on by default** (deterministic, free) — both
    the github repo (`hf_lookup`) AND the linked HF artifacts (`hf_artifacts`: models/
    datasets/spaces) — + **T4 only when `web_search` is supplied** (an Agent WebSearch
    invocation that returns result strings). Pass the result as
    `run_campaign(repo_resolver=...)`. Unit tests use the bare `resolve_repo_candidates`
    instead, so they stay offline.
    """
    return partial(
        resolve_repo_candidates,
        hf_lookup=hf_official_repo,
        hf_artifacts=hf_linked_artifacts,
        web_search=web_search,
    )
