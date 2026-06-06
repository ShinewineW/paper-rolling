# .claude/skills/paper-landscape/scripts/paths.py
"""On-disk layout for the paper-rolling workspace — the single source of truth.

Every engine module (discovery, ledger, ingest, dual-output, audit) imports the
directory-name constants and path builders from here so the on-disk-layout
contract is defined exactly once. This module is the on-disk-layout +
status-enum source of truth. It is NOT the vault-keying authority: the single
live vault-key authority is `scripts.output.naming.vault_key` (paths.py cannot
delegate to output.naming because output imports paths — that would be an import
cycle — so vault-keying lives entirely in output.naming).

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

Vault keying (双输出-D5 / OT-1 / OT-3): the entry name is
    {intake_date}_{Name}_{identity}
built by `scripts.output.naming.vault_key` (the sole authority). See that module
for the deterministic CamelCase Name derivation and the arxiv-base / DOI-hash
identity suffix.
"""

from __future__ import annotations

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
