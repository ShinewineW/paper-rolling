# .claude/skills/paper-landscape/scripts/adapters.py
"""Default deterministic infra adapters — the "just works" wiring (READY).

`run_campaign(...)` takes EIGHT injected callables. Four are LLM seams that MUST
be independent Agent-tool invocations and therefore can only be supplied by the
runtime agent (see ``references/wiring-the-seams.md``). The other THREE are pure
deterministic I/O:

    http(url) -> (status, body)              # Tier-1 HTML / Tier-2 PDF fetch
    run_cli(argv, cwd) -> CompletedProcess   # Tier-2 MinerU / pandoc
    discover(topic, n) -> list[dict]         # the discovery layer

There is no reason to re-improvise deterministic plumbing per run, so this module
ships tested defaults. With them, invoking /paper-landscape reduces to: construct
the four LLM seams, then call ``run_campaign(..., http=build_http(),
run_cli=build_run_cli(), discover=build_discover(llm=...), ...)``. Pass your own
callable to override any adapter.
"""

from __future__ import annotations

import subprocess
import time
import urllib.request
from collections.abc import Callable
from datetime import datetime
from typing import Any
from urllib.parse import urlencode

import requests

from scripts.discovery.arxiv_src import ArxivSource
from scripts.discovery.dblp import DblpSource
from scripts.discovery.discover import discover as _discover
from scripts.discovery.hf_papers import HFPapersSource
from scripts.discovery.http_client import ThrottledClient
from scripts.discovery.openalex import OpenAlexSource
from scripts.discovery.s2 import S2Source

_UA = "paper-rolling/0.1 (research; +https://github.com/ShinewineW/paper-rolling)"


def build_http(*, timeout: float = 120.0) -> Callable[[str], tuple[int, bytes]]:
    """Return an ``http(url) -> (status, body)`` seam (requests; honors env proxies).

    On any network error returns ``(0, b"")`` so the ingest tier logic treats it
    as a clean fetch failure (``status != 200`` -> Tier failed -> quarantine /
    backfill) instead of crashing the unattended /loop tick.
    """

    def http(url: str) -> tuple[int, bytes]:
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": _UA})
        except requests.RequestException:
            return 0, b""
        return resp.status_code, resp.content

    return http


def build_run_cli() -> Callable[[list[str], str], subprocess.CompletedProcess]:
    """Return a ``run_cli(argv, cwd) -> CompletedProcess`` seam (subprocess.run).

    Captures stdout/stderr as text and never raises on a non-zero exit (callers
    check ``result.returncode``), so a failed MinerU / pandoc run is a recoverable
    Tier failure rather than a crash.
    """

    def run_cli(argv: list[str], cwd: str) -> subprocess.CompletedProcess:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)  # noqa: S603

    return run_cli


class _PacedTextClient:
    """Minimal paced text GET for the arXiv Atom API (the ``get_text`` surface).

    ``ThrottledClient`` is JSON-only; ``ArxivSource`` needs ``get_text``. This is a
    small self-contained text client (paced GET + decode) rather than a change to
    the core JSON client. arXiv asks for ~3 s between requests, hence the pacing.
    """

    def __init__(self, *, min_interval: float = 3.0, timeout: float = 30.0) -> None:
        self._min_interval = min_interval
        self._timeout = timeout
        self._last: float | None = None

    def get_text(self, url: str, query: Any = None) -> str:
        if query:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}{urlencode(dict(query))}"
        if self._last is not None:
            elapsed = time.monotonic() - self._last
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
        self._last = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:  # noqa: S310
            return resp.read().decode("utf-8", errors="replace")


def build_discover(
    llm: Callable[[str], list[str]],
    *,
    is_ad_domain: bool = True,
    polite_email: str | None = None,
    from_year: int | None = None,
    overfetch_factor: int = 3,
) -> Callable[[str, int], list[dict[str, Any]]]:
    """Return a ``discover(topic, n) -> list[dict]`` seam wiring all five sources.

    The four JSON sources (OpenAlex, Semantic Scholar, HF Papers, DBLP) share the
    default real-HTTP ``ThrottledClient``; arXiv uses ``_PacedTextClient``. ``llm``
    is the query-expansion seam — the one LLM-backed part of discovery, an
    independent Agent-tool invocation (see ``references/wiring-the-seams.md``).

    Args:
        llm: query-expansion callable (prompt -> list[str]).
        is_ad_domain: copy of ``CampaignConfig.is_ad_domain``; selects the authority
            whitelists (general only, vs. general + autonomous-driving/robotics).
        polite_email: optional OpenAlex polite-pool email (lifts the request rate).
        from_year: lower-bound publication year; defaults to current_year - 2.
        overfetch_factor: candidate over-pull multiple for failure backfill.
    """
    sources: dict[str, Any] = {
        "openalex": OpenAlexSource(ThrottledClient(polite=bool(polite_email)), polite_email),
        "s2": S2Source(ThrottledClient()),
        "arxiv": ArxivSource(_PacedTextClient()),
        "dblp": DblpSource(ThrottledClient()),
        "hf_papers": HFPapersSource(ThrottledClient()),
    }

    def discover(topic: str, n: int) -> list[dict[str, Any]]:
        current_year = datetime.now().year
        floor_year = from_year if from_year is not None else current_year - 2
        campaign_config: dict[str, Any] = {
            "topic": topic,
            "top_k": n,
            "overfetch_factor": overfetch_factor,
            "is_ad_domain": is_ad_domain,
            "from_year": floor_year,
            "from_date": f"{floor_year}-01-01",
            "current_year": current_year,
        }
        return _discover(campaign_config, sources, llm)

    return discover
