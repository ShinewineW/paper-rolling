# tests/test_paths.py
"""Contract tests for the on-disk layout interface (scripts/paths.py).

Every other engine module depends on these names and helpers, so this is the
load-bearing interface test. Covers: directory-name constants, path builders,
and the STATUS_*/FAILURE_* enums. Vault keying is NOT here — the single live
vault-key authority is `scripts.output.naming.vault_key` (tested under
tests/output/).
"""

from pathlib import Path

import scripts.paths as paths


def test_dirname_constants_are_exact():
    # These strings are the contract; other chunks hardcode-match against them.
    assert paths.CORPUS_DIRNAME == "corpus"
    assert paths.LEDGER_DIRNAME == "_ledger"
    assert paths.PERSON_VAULT_DIRNAME == "person_vault"
    assert paths.AI_PACKAGE_DIRNAME == "ai_package"
    assert paths.LANDSCAPES_DIRNAME == "landscapes"
    assert paths.FAILED_DIRNAME == "_failed"
    assert paths.CONFIG_DIRNAME == "config"
    assert paths.CACHE_DIRNAME == ".cache"


def test_path_builders_join_under_root():
    root = Path("/tmp/pr")
    assert paths.corpus_dir(root) == root / "corpus"
    assert paths.ledger_dir(root) == root / "_ledger"
    assert paths.ledger_file(root) == root / "_ledger" / "processed_ledger.yaml"
    assert paths.ledger_lock(root) == root / "_ledger" / ".lock"
    assert paths.person_vault_dir(root) == root / "person_vault"
    assert paths.ai_package_dir(root) == root / "ai_package"
    assert paths.landscapes_dir(root) == root / "landscapes"
    assert paths.failed_dir(root) == root / "_failed"
    assert paths.config_dir(root) == root / "config"
    assert paths.campaign_file(root) == root / "config" / "campaign.yaml"
    assert paths.cache_dir(root) == root / ".cache"
    assert paths.citations_db(root) == root / ".cache" / "citations.db"
    assert paths.corpus_paper_dir(root, "1706.03762v5_Transformer") == (
        root / "corpus" / "1706.03762v5_Transformer"
    )


def test_status_and_failure_enums_exist():
    assert paths.STATUS_DISCOVERED == "discovered"
    assert paths.STATUS_CONVERTED == "converted"
    assert paths.STATUS_ANALYZED == "analyzed"
    assert paths.STATUS_DONE == "done"
    assert paths.STATUS_FAILED == "failed"
    assert paths.STATUS_DEFERRED == "deferred"
    assert paths.FAILURE_NOT_INDEXED_YET == "not_indexed_yet"
    assert paths.FAILURE_CONVERT_ERROR == "convert_error"
    assert paths.FAILURE_AUDIT_BLOCK == "audit_block"
    assert paths.FAILURE_DOWNLOAD_ERROR == "download_error"
