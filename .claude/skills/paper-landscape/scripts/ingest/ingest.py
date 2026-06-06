"""Ingest orchestrator: 2-tier PDF->MD with the MD-only contract.

Public entry point `ingest(candidate, corpus_dir)`:
  Tier-1 (arXiv HTML -> pandoc GFM)  --[unavailable | equation-gate demote]-->
  Tier-2 (PDF download -> MinerU CPU)  --[both fail]--> raise IngestFailed.

On success writes corpus/{ID}/{ID}.md + images/ + .md_contract.json and returns
IngestResult. The HUB caller catches IngestFailed and calls quarantine() to write
the _failed/ record (中枢-D2). Downstream reads ONLY {ID}.md (MD-only contract).
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from scripts.ingest.contract import (
    MdContract,
    count_equation_blocks,
    sha256_bytes,
    write_contract,
)
from scripts.ingest.tier1_html import Tier1Unavailable, run_tier1
from scripts.ingest.tier2_mineru import Tier2Failed, run_tier2

# pinned converter versions surfaced in the contract; the HUB can override.
PANDOC_VERSION = "3.1.2"
MINERU_VERSION = "2.0.0"

_NONWORD = re.compile(r"[^0-9A-Za-z]+")


class IngestFailed(Exception):
    """Both tiers failed for this candidate -> caller must quarantine()."""


@dataclass
class IngestResult:
    md_path: Path
    contract: MdContract
    tier: int
    images_dir: Path
    # Tier-2 (MinerU) emits content_list.json (typed formula blocks for the G3
    # equation gate); tier-1 (pandoc) emits none, so the spoke synthesizes one.
    content_list_path: Path | None = None

    # dict-style access for callers that prefer it (analysis/audit slices).
    def __getitem__(self, key: str):
        return getattr(self, key)


def _default_now() -> str:
    return datetime.now(UTC).isoformat()


def short_name(title: str, *, max_len: int = 40) -> str:
    """Deterministic CamelCase short name from a title (OT-3: no LLM naming).

    Strips non-word chars, CamelCases tokens, truncates. Stable across runs.

    NOTE: deliberately DISTINCT from `scripts.output.naming.derive_name` — this
    derives the corpus `{ID}` dir (full-title slug, max 40), while derive_name
    derives the vault `{key}` (short-name-before-first-colon, max 60). They are
    two separate stable ID spaces on purpose; do NOT consolidate them.
    """
    tokens = [t for t in _NONWORD.split(title) if t]
    camel = "".join(w[:1].upper() + w[1:] for w in tokens)
    return camel[:max_len] if camel else "Untitled"


def _paper_id(candidate: dict) -> str:
    """Stable corpus ID. arXiv: ``{arxiv_id}{version}_{ShortName}`` (spec §2.3).

    Non-arXiv (DOI-only, e.g. an OpenAlex venue paper with no arXiv id): use the
    shared DOI-hash identity ``{doi-hash}_{ShortName}`` — never ``None_...``,
    which would be a broken, collision-prone identity (Codex R21).
    """
    name = short_name(candidate["title"])
    aid = candidate.get("arxiv_id")
    if aid:
        return f"{aid}{candidate.get('arxiv_version') or ''}_{name}"
    doi = candidate.get("doi")
    if doi:
        from scripts.output.naming import identity_base

        return f"{identity_base(None, doi)}_{name}"
    return name  # degenerate: neither arxiv_id nor doi (identity from title only)


def _finalize(
    paper_dir: Path,
    paper_id: str,
    md_text: str,
    images: list[str],
    *,
    converter: str,
    converter_version: str,
    source_pdf_sha256: str | None,
    content_list_path: Path | None = None,
) -> IngestResult:
    """Write {ID}.md + .md_contract.json and return the result."""
    md_path = paper_dir / f"{paper_id}.md"
    md_path.write_text(md_text, encoding="utf-8")
    images_dir = paper_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    tier = 1 if converter == "pandoc" else 2
    contract = MdContract(
        source_pdf_sha256=source_pdf_sha256,
        converter=converter,
        converter_version=converter_version,
        md_sha256=sha256_bytes(md_text.encode("utf-8")),
        image_count=len(images),
        equation_block_count=count_equation_blocks(md_text),
    )
    write_contract(contract, paper_dir / ".md_contract.json")
    return IngestResult(
        md_path=md_path,
        contract=contract,
        tier=tier,
        images_dir=images_dir,
        content_list_path=content_list_path,
    )


def ingest(
    candidate: dict,
    corpus_dir: Path,
    *,
    http,
    run_cli,
    now=None,
) -> IngestResult:
    """Ingest one candidate into corpus/{ID}/. Raises IngestFailed if both tiers fail."""
    corpus_dir = Path(corpus_dir)
    paper_id = _paper_id(candidate)
    paper_dir = corpus_dir / "corpus" / paper_id
    paper_dir.mkdir(parents=True, exist_ok=True)

    aid = candidate.get("arxiv_id")
    ver = candidate.get("arxiv_version") or ""
    tier1_reason: str | None = None

    # SEAM (ADR-0002, deferred): the tier chain below is a hardcoded
    # Tier-1 -> Tier-2 -> raise sequence (n=2, kept concrete). To add a Tier-3
    # converter, insert another try/except after Tier-2 — see docs/EXTENDING.md.
    # --- Tier 1: arXiv HTML -> pandoc GFM (only when we have an arXiv id) ---
    if aid:
        try:
            t1 = run_tier1(
                aid, ver, paper_dir, http=http, run_cli=run_cli, pandoc_version=PANDOC_VERSION
            )
            eq_blocks = count_equation_blocks(t1.md_text)
            # Equation-count gate (摄取-D1): HTML had math but pandoc dropped all
            # display equations -> the conversion is untrustworthy -> demote.
            if t1.html_had_math and eq_blocks == 0:
                tier1_reason = "equation_gate: html had math but 0 $$ blocks emitted"
            else:
                return _finalize(
                    paper_dir,
                    paper_id,
                    t1.md_text,
                    t1.images,
                    converter="pandoc",
                    converter_version=PANDOC_VERSION,
                    source_pdf_sha256=None,
                )
        except Tier1Unavailable as exc:
            tier1_reason = str(exc)
    else:
        # Non-arXiv (DOI-only) paper: Tier-1 is arXiv-HTML-only, so skip straight
        # to the PDF/MinerU path (Codex R21).
        tier1_reason = "skipped: non-arXiv candidate (no arxiv_id)"

    # --- Tier 2: PDF download -> MinerU (CPU) ---
    pdf_url = candidate.get("oa_pdf_url")  # Round 1 F7: canonical PDF field is oa_pdf_url
    if not pdf_url and aid:
        # Some sources (e.g. HF Papers) omit oa_pdf_url though the paper is on
        # arXiv — derive the arXiv PDF URL rather than fail (Codex R21).
        pdf_url = f"https://arxiv.org/pdf/{aid}{ver}"
    if not pdf_url:
        raise IngestFailed(
            f"{paper_id}: tier1={tier1_reason}; tier2=no PDF URL "
            "(oa_pdf_url is None and no arxiv id to derive one)"
        )
    try:
        t2 = run_tier2(
            pdf_url, paper_dir, http=http, run_cli=run_cli, mineru_version=MINERU_VERSION
        )
    except Tier2Failed as exc:
        raise IngestFailed(f"{paper_id}: tier1={tier1_reason}; tier2={exc}") from exc

    # Move MinerU images into the canonical paper_dir/images/.
    images_dir = paper_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    mineru_images = t2.content_list_path.parent / "images"
    if mineru_images.is_dir():
        for img in mineru_images.iterdir():
            if img.is_file():
                shutil.copy2(img, images_dir / img.name)

    return _finalize(
        paper_dir,
        paper_id,
        t2.md_text,
        t2.images,
        converter="mineru",
        converter_version=MINERU_VERSION,
        source_pdf_sha256=t2.source_pdf_sha256,
        content_list_path=t2.content_list_path,
    )


def quarantine(
    candidate: dict,
    corpus_dir: Path,
    *,
    reason: str,
    attempted_tiers: list[int],
    now=None,
) -> Path:
    """Write a _failed/{ID}.json failure record (中枢-D2). Returns the record path."""
    now = now or _default_now
    corpus_dir = Path(corpus_dir)
    failed_dir = corpus_dir / "_failed"
    failed_dir.mkdir(parents=True, exist_ok=True)
    paper_id = _paper_id(candidate)
    record = {
        "arxiv_id": candidate["arxiv_id"],
        "arxiv_version": candidate.get("arxiv_version"),
        "doi": candidate.get("doi"),
        "title": candidate["title"],
        "source_url": candidate.get("oa_pdf_url"),
        "attempted_tiers": attempted_tiers,
        "reason": reason,
        "failed_at": now(),
    }
    rec_path = failed_dir / f"{paper_id}.json"
    rec_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    return rec_path
