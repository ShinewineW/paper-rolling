# tests/test_paths.py
"""Contract tests for the cross-module layout constants (scripts/paths.py).

Covers only what production actually consumes: the output-branch set (which
store.consistency_check + hub iterate) and the failure-class constants spoke +
hub record on the ledger row. Vault keying is NOT here — the single live
authority is scripts.output.naming.vault_key (tested under tests/output/).
"""

import scripts.paths as paths


def test_vault_branch_set_is_the_person_ai_pair():
    # store.consistency_check + hub._is_truly_done iterate this set.
    assert paths.VAULT_BRANCHES == (
        ("person_vault", "person_vault_path"),
        ("ai_package", "ai_package_path"),
    )
    assert paths.VAULT_BRANCH_PATH_FIELDS == ("person_vault_path", "ai_package_path")


def test_failure_class_constants_are_exact():
    # spoke.py + hub.py record these strings verbatim on the ledger row.
    assert paths.FAILURE_CONVERT_ERROR == "convert_error"
    assert paths.FAILURE_AUDIT_BLOCK == "audit_block"
    assert paths.FAILURE_STALLED == "stalled"


def test_repo_root_resolves_to_workspace_root():
    root = paths.repo_root()
    assert (root / ".claude" / "skills" / "paper-landscape").is_dir()
