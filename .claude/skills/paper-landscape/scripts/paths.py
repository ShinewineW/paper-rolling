# .claude/skills/paper-landscape/scripts/paths.py
"""Cross-module on-disk layout constants for the paper-rolling workspace.

Centralizes only the layout facts shared across engine modules: the output-branch
SET (the vault branches a "done" paper is promoted to) and the failure-class
constants the ledger + spoke record. It is NOT the vault-keying authority — the
single live vault-key authority is `scripts.output.naming.vault_key` (paths.py
cannot delegate to output.naming without an import cycle, since output imports
paths).

Layout (基调-D2 / 双输出-D5 / 中枢-D2):
    <root>/
      corpus/{ID}/            source + intermediate ({ID}.md tracked; pdf/images/
                              content_list.json gitignored; .md_contract.json tracked)
      _ledger/                processed_ledger.yaml (single-writer) + .lock
      person_vault/{key}/     human-facing reports (branch1)
      ai_package/{key}/       AI-facing ARA knowledge packs (branch2)
      landscapes/             cross-paper synthesis reports
      _failed/                per-paper failure records (中枢-D2)
      config/campaign.yaml    locked campaign params (吸收-D4)
      .cache/citations.db     SQLite citation cache (gitignored)

Each directory name is written by its owning module (ledger/store.py,
output/produce.py, landscapes.py, …) close to use; the only names promoted here
are those iterated cross-module via VAULT_BRANCHES below.
"""

from __future__ import annotations

from pathlib import Path

PERSON_VAULT_DIRNAME = "person_vault"
AI_PACKAGE_DIRNAME = "ai_package"


# --- output-branch set (双输出 / ADR-0002) ---------------------------------
# A fully-processed ("done") paper is promoted to these vault branches, all
# under the SAME output.naming vault_key. Centralized so the completeness checks
# — the ledger LS-4 self-heal (store.consistency_check) and the watchdog
# false-done detection (hub._is_truly_done) — iterate this set instead of
# hardcoding person+ai across files.
#
# The producer's staging/promotion is intentionally NOT generalized (rule-of-
# three: only 2 branches exist; a 3rd's shape is unknown). Adding a co-promoted
# branch: see docs/guides/EXTENDING.md + ADR-0002.
#
# NOTE: the vault entry NAME is the output.naming vault_key, which DIFFERS from
# the ledger ROW key (hub._candidate_key). Completeness is therefore checked via
# the row's RECORDED path fields below, never derived from the row key.
VAULT_BRANCHES: tuple[tuple[str, str], ...] = (
    (PERSON_VAULT_DIRNAME, "person_vault_path"),
    (AI_PACKAGE_DIRNAME, "ai_package_path"),
)
# The ledger-row field recording each branch's absolute path (one per branch).
VAULT_BRANCH_PATH_FIELDS: tuple[str, ...] = tuple(field for _, field in VAULT_BRANCHES)


# --- failure-class constants (recorded verbatim by spoke + hub on the row) ---

FAILURE_CONVERT_ERROR = "convert_error"  # both ingest tiers failed
FAILURE_AUDIT_BLOCK = "audit_block"  # G2/G3 hard block, N rounds unmet
FAILURE_STALLED = "stalled"  # spoke exceeded the wall-clock budget or crashed (中枢-D2)


def repo_root() -> Path:
    """Return the paper-rolling repo root (used by the scaffold/campaign tests).

    <root>/.claude/skills/paper-landscape/scripts/paths.py -> parents[4].
    """
    return Path(__file__).resolve().parents[4]
