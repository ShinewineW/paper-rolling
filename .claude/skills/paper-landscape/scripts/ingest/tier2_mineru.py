"""Tier-2 ingest: download PDF + MinerU CLI (CPU backend) -> MD + images + content_list.

摄取-D1 / 吸收-D6: fallback when arXiv HTML is missing/broken or non-arXiv PDFs
(CVF/OpenReview). MinerU is an external CLI runtime dep (NOT a per-skill venv,
spec §8 R1) invoked as a subprocess via the injected run_cli seam. CPU/pipeline
backend on Apple Silicon (MPS slower than CPU, spec §2.2).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.ingest.contract import sha256_bytes


class Tier2Failed(Exception):
    """Hard failure in Tier-2: download or MinerU CLI failed -> quarantine."""


@dataclass
class Tier2Output:
    md_text: str
    images: list[str]
    content_list_path: Path
    source_pdf_sha256: str


def run_tier2(
    pdf_url: str,
    out_dir: Path,
    *,
    http,
    run_cli,
    mineru_version: str,
) -> Tier2Output:
    """Download PDF then run MinerU -> Tier2Output. Raises Tier2Failed on any failure.

    `mineru_version` is surfaced by the orchestrator into the contract.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    status, pdf_bytes = http(pdf_url)
    if status != 200 or not pdf_bytes:
        raise Tier2Failed(f"pdf_download: {pdf_url} status={status}")
    pdf_path = out_dir / "source.pdf"
    pdf_path.write_bytes(pdf_bytes)
    pdf_sha = sha256_bytes(pdf_bytes)

    mineru_out = "mineru"
    # `-b pipeline` selects the CPU pipeline backend (摄取-D1: CPU on Mac).
    argv = ["mineru", "-p", pdf_path.name, "-o", mineru_out, "-b", "pipeline"]
    result = run_cli(argv, str(out_dir))
    if getattr(result, "returncode", 1) != 0:
        raise Tier2Failed(
            f"mineru_failed: rc={getattr(result, 'returncode', '?')} "
            f"stderr={getattr(result, 'stderr', '')[:200]}"
        )

    mineru_dir = out_dir / mineru_out
    md_path = mineru_dir / "paper.md"
    content_list = mineru_dir / "content_list.json"
    if not md_path.exists() or not content_list.exists():
        raise Tier2Failed("mineru_incomplete: missing paper.md or content_list.json")

    images_dir = mineru_dir / "images"
    images = (
        sorted(p.name for p in images_dir.iterdir() if p.is_file()) if images_dir.is_dir() else []
    )
    return Tier2Output(
        md_text=md_path.read_text(encoding="utf-8"),
        images=images,
        content_list_path=content_list,
        source_pdf_sha256=pdf_sha,
    )
