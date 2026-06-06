# .claude/skills/paper-landscape/scripts/paths.py
"""On-disk layout for the paper-rolling workspace — the single source of truth.

Every engine module (discovery, ledger, ingest, dual-output, audit) imports the
directory-name constants, path builders, and vault-keying helpers from here so
the layout contract is defined exactly once.

Layout (基调-D2 / 双输出-D5 / 中枢-D2):
    <root>/
      corpus/{ID}/            source + intermediate zone: {ID}.md (tracked),
                              {ID}.pdf + images/ + content_list.json (gitignored),
                              .md_contract.json (tracked)
      _ledger/                processed_ledger.yaml (single-writer) + .lock
      person_vault/{key}/     human-facing reports (was branch1)
      ai_package/{key}/       AI-facing ARA knowledge packs (was branch2)
      landscapes/             cross-paper synthesis reports
      _failed/                per-paper failure records (中枢-D2)
      config/campaign.yaml    locked campaign params (吸收-D4)
      .cache/citations.db     SQLite citation cache (gitignored)

Vault keying (双输出-D5 / OT-1 / OT-3): entry name =
    {intake_date}_{Name}_{identity}
where Name is a DETERMINISTIC CamelCase slug of the title (never LLM-named) and
identity is the arxiv base id, or a short hash of the DOI for non-arXiv papers.
This makes same-day same-title entries collision-free and lets reprocessing find
the existing entry by identity, ignoring the date prefix (OT-2).
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

# --- directory-name constants (the contract) -------------------------------

CORPUS_DIRNAME = "corpus"
LEDGER_DIRNAME = "_ledger"
PERSON_VAULT_DIRNAME = "person_vault"
AI_PACKAGE_DIRNAME = "ai_package"
LANDSCAPES_DIRNAME = "landscapes"
FAILED_DIRNAME = "_failed"
CONFIG_DIRNAME = "config"
CACHE_DIRNAME = ".cache"

LEDGER_FILENAME = "processed_ledger.yaml"
LEDGER_LOCK_FILENAME = ".lock"  # LS-1 concurrency lock
CAMPAIGN_FILENAME = "campaign.yaml"
CITATIONS_DB_FILENAME = "citations.db"
MD_CONTRACT_FILENAME = ".md_contract.json"

# --- vault-keying knobs -----------------------------------------------------

MAX_SHORT_NAME_LEN = 48  # OT-3 truncation bound
DOI_HASH_LEN = 8  # OT-1 DOI disambiguator length
_FALLBACK_NAME = "Untitled"


# --- root resolution --------------------------------------------------------


def repo_root() -> Path:
    """Return the paper-rolling repo root.

    Resolved relative to this file's location:
    <root>/.claude/skills/paper-landscape/scripts/paths.py -> parents[4].
    """
    return Path(__file__).resolve().parents[4]


# --- path builders (root-parameterized so tests/callers stay explicit) ------


def corpus_dir(root: Path) -> Path:
    return Path(root) / CORPUS_DIRNAME


def corpus_paper_dir(root: Path, paper_id: str) -> Path:
    """Source/intermediate dir for one paper, keyed by {arxiv_id}v{N}_{ShortName}."""
    return corpus_dir(root) / paper_id


def ledger_dir(root: Path) -> Path:
    return Path(root) / LEDGER_DIRNAME


def ledger_file(root: Path) -> Path:
    return ledger_dir(root) / LEDGER_FILENAME


def ledger_lock(root: Path) -> Path:
    return ledger_dir(root) / LEDGER_LOCK_FILENAME


def person_vault_dir(root: Path) -> Path:
    return Path(root) / PERSON_VAULT_DIRNAME


def ai_package_dir(root: Path) -> Path:
    return Path(root) / AI_PACKAGE_DIRNAME


def landscapes_dir(root: Path) -> Path:
    return Path(root) / LANDSCAPES_DIRNAME


def failed_dir(root: Path) -> Path:
    return Path(root) / FAILED_DIRNAME


def config_dir(root: Path) -> Path:
    return Path(root) / CONFIG_DIRNAME


def campaign_file(root: Path) -> Path:
    return config_dir(root) / CAMPAIGN_FILENAME


def cache_dir(root: Path) -> Path:
    return Path(root) / CACHE_DIRNAME


def citations_db(root: Path) -> Path:
    return cache_dir(root) / CITATIONS_DB_FILENAME


# --- deterministic vault keying (OT-1 / OT-3) -------------------------------

_NON_ALNUM = re.compile(r"[^0-9A-Za-z]+")


def short_name(title: str) -> str:
    """Deterministic CamelCase slug of a paper title (OT-3: never LLM-named).

    Splits on any run of non-alphanumeric characters, capitalizes each token's
    first letter, concatenates, and truncates to MAX_SHORT_NAME_LEN. Returns a
    stable fallback for empty/junk titles so the result is never empty.
    """
    tokens = [t for t in _NON_ALNUM.split(title or "") if t]
    if not tokens:
        return _FALLBACK_NAME
    camel = "".join(t[0].upper() + t[1:] for t in tokens)
    return camel[:MAX_SHORT_NAME_LEN]


def doi_short_hash(doi: str) -> str:
    """Stable short hex hash of a DOI for vault-key disambiguation (OT-1)."""
    digest = hashlib.sha256(doi.strip().lower().encode("utf-8")).hexdigest()
    return digest[:DOI_HASH_LEN]


def _identity_suffix(arxiv_base: str | None, doi: str | None) -> str:
    """Identity disambiguator: arxiv base id, else DOI short hash.

    Identity = arxiv_id(base) || DOI per the '同篇判定' rule. Raises if neither
    is present, because a paper with no canonical identity cannot be keyed.
    """
    if arxiv_base:
        return arxiv_base
    if doi:
        return doi_short_hash(doi)
    raise ValueError("vault_key requires an identity: arxiv_base or doi must be set")


def vault_key(
    intake_date: str,
    title: str,
    arxiv_base: str | None = None,
    doi: str | None = None,
) -> str:
    """Build the collision-proof vault entry name (OT-1).

    Format: {intake_date}_{ShortName}_{identity}, e.g.
        2026-06-05_DiffusionDriveEndToEndDriving_2411.15139

    intake_date is the ingest day (not the publication date) per 双输出-D5.
    """
    suffix = _identity_suffix(arxiv_base, doi)
    return f"{intake_date}_{short_name(title)}_{suffix}"


def vault_entry_glob(arxiv_base: str | None = None, doi: str | None = None) -> str:
    """Glob that matches an existing vault entry by identity, ignoring the date
    prefix and short name (OT-2 reprocessing: delete-old + write-new)."""
    suffix = _identity_suffix(arxiv_base, doi)
    return f"*_{suffix}"


# --- status + failure-class enums (used by ledger + audit slices) ----------

STATUS_DISCOVERED = "discovered"
STATUS_CONVERTED = "converted"
STATUS_ANALYZED = "analyzed"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_DEFERRED = "deferred"

FAILURE_NOT_INDEXED_YET = "not_indexed_yet"  # preprint, retry after OpenAlex lag
FAILURE_CONVERT_ERROR = "convert_error"  # both ingest tiers failed
FAILURE_DOWNLOAD_ERROR = "download_error"  # PDF/HTML fetch failed
FAILURE_AUDIT_BLOCK = "audit_block"  # G2/G3 hard block, N rounds unmet
