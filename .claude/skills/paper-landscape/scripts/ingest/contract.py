"""MD-only contract: provenance record + content hashing + equation-block counting.

Contract fields (摄取-D1 / spec §2.3): source_pdf_sha256, converter,
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
