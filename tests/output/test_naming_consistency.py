"""Vault-key authority is unambiguous: the LIVE pipeline uses output.naming.

There is now exactly ONE vault-key authority — `scripts.output.naming.vault_key`.
The divergent duplicates that used to live in `scripts.paths` and
`scripts.ledger.naming` were removed (zero live callers). This test pins the
single-authority contract: `produce_outputs` builds the key with
`output.naming.vault_key` and returns the EXACT on-disk vault paths, which the
spoke/hub record verbatim — so a future caller cannot silently pick a divergent
helper (there is none to pick).

Note: this file lives under tests/output/ to inherit the candidate/ledger/
md_path/analysis fixtures (+ the autouse analyzer patch) from the output
conftest; the consistency claim it pins is naming-wide, not output-local.
"""

from __future__ import annotations

from scripts.output.naming import vault_key
from scripts.output.produce import produce_outputs


def test_live_authority_key_matches_output_naming(tmp_path, candidate, ledger, md_path, analysis):
    """produce_outputs' returned key == output.naming.vault_key for same inputs."""
    produced = produce_outputs(md_path, candidate, ledger, root=tmp_path)

    expected = vault_key(
        intake=ledger.intake_date(),
        title=candidate["title"],
        arxiv_id=candidate["arxiv_id"],
        doi=candidate["doi"],
    )
    assert produced.key == expected


def test_ledger_recorded_path_equals_on_disk_vault_dir(
    tmp_path, candidate, ledger, md_path, analysis
):
    """The recorded vault paths are the EXACT on-disk dirs (no re-derivation)."""
    produced = produce_outputs(md_path, candidate, ledger, root=tmp_path)

    # produce_outputs returns the dirs it actually created.
    assert produced.person_path.is_dir()
    assert produced.ai_path.is_dir()
    # And those are literally root/<vault>/<key> — the live key, on disk.
    assert produced.person_path == tmp_path / "person_vault" / produced.key
    assert produced.ai_path == tmp_path / "ai_package" / produced.key


def test_output_naming_is_the_sole_vault_key_authority():
    """The divergent duplicates are gone: scripts.paths and scripts.ledger.naming
    no longer expose any vault-NAMING helper, so output.naming.vault_key is the
    only authority a caller can reach (no silent divergence is possible).
    """
    import scripts.ledger.naming as ledger_naming
    import scripts.paths as paths

    assert not hasattr(paths, "vault_key")
    assert not hasattr(paths, "short_name")
    assert not hasattr(paths, "vault_entry_glob")
    assert not hasattr(ledger_naming, "vault_entry_name")
    assert not hasattr(ledger_naming, "derive_name")
    # The surviving ledger helpers are version/identity keys, a different concern.
    assert hasattr(ledger_naming, "identity_key")
    assert hasattr(ledger_naming, "version_key")
