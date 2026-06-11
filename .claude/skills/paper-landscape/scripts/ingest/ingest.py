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
    corpus_readiness_problems,
    count_equation_blocks,
    count_table_blocks,
    sha256_bytes,
    write_contract,
)
from scripts.ingest.tier1_html import Tier1Unavailable, run_tier1
from scripts.ingest.tier2_mineru import Tier2Failed, run_tier2

# pinned converter versions surfaced in the contract; the HUB can override.
PANDOC_VERSION = "3.1.2"
MINERU_VERSION = "2.0.0"

# Fidelity gates (摄取-D1 / ROADMAP A1+A2): a Tier-1 conversion must preserve at
# least this fraction of the source's DISPLAY equations / data tables, else it is
# demoted to Tier-2 (MinerU). Catches PARTIAL loss (e.g. 50 source equations, 5
# survive; or 8 tables, 1 survives), not just the all-or-nothing case.
EQUATION_SURVIVAL_RATIO = 0.5
TABLE_SURVIVAL_RATIO = 0.5

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
    """Stable corpus ID. arXiv: ``{arxiv_id}{version}_{ShortName}``.

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


def _reuse_ready_corpus(paper_dir: Path, paper_id: str) -> IngestResult | None:
    """Reuse an already-converted, ready corpus entry instead of re-converting.

    The converted ``{ID}.md`` is the tracked SSOT (基调-D2); downstream reads only it.
    When it AND a consistent ``.md_contract.json`` are already present (and
    ``corpus_readiness_problems`` is clean), re-running Tier-1/Tier-2 would only
    overwrite that SSOT with a fresh conversion — and for a Tier-2 paper whose MD was
    built off-box because local MinerU can't run it (e.g. OOM), it would DESTROY the
    only good copy. So reuse it and never invoke the converter seams.

    Escape hatch to force a fresh conversion: delete ``{ID}.md`` or ``.md_contract.json``
    (or let the MD drift from its contract) — any of those makes this return None.
    """
    md_path = paper_dir / f"{paper_id}.md"
    contract_path = paper_dir / ".md_contract.json"
    if not (md_path.is_file() and contract_path.is_file()):
        return None
    if corpus_readiness_problems(md_path):
        return None
    c = json.loads(contract_path.read_text(encoding="utf-8"))
    converter = c.get("converter", "")
    content_list = paper_dir / "content_list.json"
    return IngestResult(
        md_path=md_path,
        contract=MdContract(
            source_pdf_sha256=c.get("source_pdf_sha256"),
            converter=converter,
            converter_version=c.get("converter_version", ""),
            md_sha256=c.get("md_sha256", ""),
            image_count=int(c.get("image_count") or 0),
            equation_block_count=int(c.get("equation_block_count") or 0),
        ),
        tier=1 if converter == "pandoc" else 2,
        images_dir=paper_dir / "images",
        content_list_path=content_list if content_list.is_file() else None,
    )


def ingest(
    candidate: dict,
    corpus_dir: Path,
    *,
    http,
    run_cli,
    now=None,
) -> IngestResult:
    """Ingest one candidate into corpus/{ID}/. Raises IngestFailed if both tiers fail.

    Fast path: a ready, already-converted corpus entry is reused verbatim (no
    download, no converter) — see ``_reuse_ready_corpus``.
    """
    corpus_dir = Path(corpus_dir)
    aid = candidate.get("arxiv_id")
    ver = candidate.get("arxiv_version") or ""
    paper_id = _paper_id(candidate)
    paper_dir = corpus_dir / "corpus" / paper_id

    # Reuse an already-committed corpus entry keyed by the STABLE identity (arxiv_id),
    # not the title-derived dir name (ADR-0010 指定列表): an operator's force_include entry
    # may carry only an arxiv_id or a differently-spelled title, so `_paper_id`'s
    # title-derived dir may not match the committed `corpus/{aid}_{ShortName}/`. When the
    # title-derived dir is absent but EXACTLY ONE `corpus/{aid}_*` exists, reuse THAT — so a
    # list-mode run reuses the committed MD instead of re-fetching + re-converting (Tier-2
    # MinerU OOMs on big PDFs). A genuinely new paper has no such dir → ingest fresh below.
    if aid and not paper_dir.is_dir():
        matches = sorted((corpus_dir / "corpus").glob(f"{aid}_*"))
        if len(matches) == 1:
            paper_dir, paper_id = matches[0], matches[0].name

    reused = _reuse_ready_corpus(paper_dir, paper_id)
    if reused is not None:
        return reused

    paper_dir.mkdir(parents=True, exist_ok=True)
    tier1_reason: str | None = None

    # SEAM (ADR-0002, deferred): the tier chain below is a hardcoded
    # Tier-1 -> Tier-2 -> raise sequence (n=2, kept concrete). To add a Tier-3
    # converter, insert another try/except after Tier-2 — see docs/guides/EXTENDING.md.
    # --- Tier 1: arXiv HTML -> pandoc GFM (only when we have an arXiv id) ---
    if aid:
        try:
            t1 = run_tier1(
                aid, ver, paper_dir, http=http, run_cli=run_cli, pandoc_version=PANDOC_VERSION
            )
            # Fidelity gates (摄取-D1 / ROADMAP A1+A2): the conversion is
            # untrustworthy if pandoc dropped more than half of the source's
            # DISPLAY equations OR data tables — demote to Tier-2. Catches PARTIAL
            # loss, not just all-or-nothing. Uses DISPLAY-equation / <table> counts
            # so inline-only-math papers (legitimately 0 `$$`) are not falsely
            # demoted.
            eq_blocks = count_equation_blocks(t1.md_text)
            tbl_blocks = count_table_blocks(t1.md_text)
            src_eq, src_tbl = t1.html_math_count, t1.html_table_count
            if src_eq > 0 and eq_blocks < src_eq * EQUATION_SURVIVAL_RATIO:
                tier1_reason = (
                    f"equation_gate: only {eq_blocks}/{src_eq} display equations "
                    f"survived (< {EQUATION_SURVIVAL_RATIO:.0%})"
                )
            elif src_tbl > 0 and tbl_blocks < src_tbl * TABLE_SURVIVAL_RATIO:
                tier1_reason = (
                    f"table_gate: only {tbl_blocks}/{src_tbl} tables survived "
                    f"(< {TABLE_SURVIVAL_RATIO:.0%})"
                )
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
