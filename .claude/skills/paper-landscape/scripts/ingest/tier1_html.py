"""Tier-1 ingest: arXiv official HTML (LaTeXML) -> GFM via pandoc.

摄取-D1: highest-fidelity path. Fetch arxiv.org/html/{id}, run quality gate
(HTML missing / LaTeXML error markers), download original <img> figures, then
convert HTML->GFM with pandoc (MathML -> LaTeX $$). No PDF is downloaded in
Tier-1. Raises Tier1Unavailable to signal "demote to Tier-2". Returns a
Tier1Output whose html_had_math flag feeds the orchestrator's equation gate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# LaTeXML / ar5iv error markers that indicate a broken render -> demote to Tier-2.
_LATEXML_ERROR = re.compile(rb"ltx_ERROR|LaTeXML\s+error|\bUnable to process\b", re.IGNORECASE)
# Extract <img src="..."> targets (single or double quotes).
_IMG_SRC = re.compile(rb"""<img\b[^>]*\bsrc=["']([^"']+)["']""", re.IGNORECASE)
# Presence of MathML / LaTeXML math in the source HTML — used by the orchestrator's
# equation-count gate: if HTML had math but pandoc emitted 0 $$ blocks -> demote.
_HTML_MATH = re.compile(rb"<math\b|ltx_Math|ltx_equation", re.IGNORECASE)


class Tier1Unavailable(Exception):
    """Soft signal: Tier-1 cannot produce a trustworthy MD; caller falls to Tier-2."""


@dataclass
class Tier1Output:
    md_text: str
    images: list[str]
    html_had_math: bool


def _arxiv_html_url(arxiv_id: str, version: str) -> str:
    return f"https://arxiv.org/html/{arxiv_id}{version}"


def _is_local_ref(src: bytes) -> bool:
    """True if an <img src> is a relative, in-paper figure (not http/data:)."""
    s = src.decode("utf-8", "ignore").strip()
    return not (s.startswith("http://") or s.startswith("https://") or s.startswith("data:"))


def run_tier1(
    arxiv_id: str,
    version: str,
    out_dir: Path,
    *,
    http,
    run_cli,
    pandoc_version: str,
) -> Tier1Output:
    """Convert arXiv HTML -> GFM markdown. Returns Tier1Output.

    `http(url) -> (status, bytes)` and `run_cli(argv, cwd) -> result(.returncode)`
    are injected seams. Raises Tier1Unavailable when the quality gate fails.
    `pandoc_version` is surfaced by the orchestrator into the contract.
    """
    out_dir = Path(out_dir)
    base_url = _arxiv_html_url(arxiv_id, version)

    status, body = http(base_url)
    if status != 200 or not body:
        raise Tier1Unavailable(f"html_missing: {base_url} status={status}")
    if _LATEXML_ERROR.search(body):
        raise Tier1Unavailable(f"latexml_error: marker found in {base_url}")

    # Download original figures referenced by relative <img src>.
    images_dir = out_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[str] = []
    for raw_src in _IMG_SRC.findall(body):
        if not _is_local_ref(raw_src):
            continue
        src = raw_src.decode("utf-8", "ignore")
        fname = Path(src).name
        img_status, img_body = http(f"{base_url}/{src}")
        if img_status == 200 and img_body:
            (images_dir / fname).write_bytes(img_body)
            downloaded.append(fname)

    # Write fetched HTML, then convert HTML -> GFM with pandoc (MathML -> LaTeX).
    html_path = out_dir / "_tier1.html"
    html_path.write_bytes(body)
    md_name = "paper.md"
    argv = [
        "pandoc",
        "--from",
        "html",
        "--to",
        "gfm",
        str(html_path.name),
        "-o",
        md_name,
    ]
    result = run_cli(argv, str(out_dir))
    if getattr(result, "returncode", 1) != 0:
        raise Tier1Unavailable(f"pandoc_failed: rc={getattr(result, 'returncode', '?')}")

    md_path = out_dir / md_name
    if not md_path.exists():
        raise Tier1Unavailable("pandoc_no_output")
    md_text = md_path.read_text(encoding="utf-8")
    html_had_math = bool(_HTML_MATH.search(body))
    return Tier1Output(md_text=md_text, images=downloaded, html_had_math=html_had_math)
