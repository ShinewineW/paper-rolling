"""MD-only contract: provenance record + content hashing + equation-block counting.

Contract fields (摄取-D1): source_pdf_sha256, converter,
converter_version, md_sha256, image_count, equation_block_count.
Tier-1 (arXiv HTML, no PDF download) leaves source_pdf_sha256 = None.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

# A display equation block is an opening "$$" and its matching closing "$$".
# We pair fences greedily: every 2 occurrences of a "$$" fence = one block.
# Inline math uses single "$"; a dangling unpaired "$$" does not complete a pair.
_FENCE = re.compile(r"\$\$")
# A GFM table carries exactly one header-separator row (| --- | --- |), so
# counting separator rows counts emitted tables (ROADMAP A2 table-fidelity gate).
_TABLE_SEP = re.compile(r"^\|[\s:|-]+\|$")


def sha256_bytes(data: bytes) -> str:
    """Return the hex SHA-256 digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a file's contents (streamed)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def count_equation_blocks(md: str) -> int:
    """Count paired display-equation fences ($$...$$) in GFM markdown.

    Inline math ($x$) is ignored; a dangling unpaired $$ does not count.
    """
    return len(_FENCE.findall(md)) // 2


def count_table_blocks(md: str) -> int:
    """Count GFM tables in markdown — one per `| --- |` header-separator row."""
    return sum(1 for line in md.splitlines() if _TABLE_SEP.match(line.strip()))


@dataclass(frozen=True)
class MdContract:
    """Provenance record written to .md_contract.json (one per ingested paper)."""

    source_pdf_sha256: str | None
    converter: str
    converter_version: str
    md_sha256: str
    image_count: int
    equation_block_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def write_contract(contract: MdContract, path: Path) -> None:
    """Serialize a contract to JSON at `path` (2-space indent, stable key order)."""
    path.write_text(json.dumps(contract.to_dict(), indent=2, ensure_ascii=False) + "\n")


def corpus_readiness_problems(md_path: Path) -> list[str]:
    """Mechanical completeness check of a corpus entry against its `.md_contract.json`.

    Returns a list of human-readable gaps; empty == ready. A fresh `ingest()` writes
    MD + images/ + contract atomically, so it is always ready; this catches the REUSE
    path (revival) on a checkout where the gitignored `corpus/**/images/` were never
    pulled — so we bail to manual (re-ingest) BEFORE burning any LLM token instead of
    failing at the terminal branch1 figure gate after analyzer + G2 + writer ran.

    No contract → returns [] (nothing to verify against; that is a different concern).
    """
    md_path = Path(md_path)
    if not md_path.is_file():
        return [f"MD missing: {md_path}"]
    contract_path = md_path.parent / ".md_contract.json"
    if not contract_path.is_file():
        return []
    c = json.loads(contract_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    want_sha = c.get("md_sha256")
    if want_sha and sha256_file(md_path) != want_sha:
        problems.append("md_sha256 drift (MD corrupted/truncated vs contract)")
    want_imgs = int(c.get("image_count") or 0)
    if want_imgs > 0:
        images_dir = md_path.parent / "images"
        have = sum(1 for p in images_dir.iterdir() if p.is_file()) if images_dir.is_dir() else 0
        if have < want_imgs:
            problems.append(
                f"images incomplete: contract={want_imgs} present={have} (re-ingest needed)"
            )
    return problems
