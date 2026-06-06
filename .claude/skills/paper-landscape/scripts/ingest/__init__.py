"""Ingest layer: 2-tier PDF->MD with MD-only contract (摄取-D1 + 吸收-D6)."""

from scripts.ingest.contract import MdContract, count_equation_blocks, sha256_bytes, sha256_file
from scripts.ingest.ingest import IngestFailed, IngestResult, ingest, quarantine, short_name

__all__ = [
    "ingest",
    "IngestResult",
    "IngestFailed",
    "quarantine",
    "short_name",
    "MdContract",
    "count_equation_blocks",
    "sha256_bytes",
    "sha256_file",
]
