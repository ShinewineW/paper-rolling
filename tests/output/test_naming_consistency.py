"""Vault-key authority is unambiguous: the LIVE pipeline uses output.naming.

FIX C guard. Three near-identical `vault_key`-shaped helpers exist
(`scripts.paths`, `scripts.ledger.naming`, `scripts.output.naming`) with
DIFFERENT colon-splitting semantics. Only `scripts.output.naming.vault_key` is
the live authority: `produce_outputs` builds the key with it and returns the
EXACT on-disk vault paths, which the spoke/hub record verbatim. This test pins
that contract so a future caller can't silently pick a divergent helper.

Note: this file lives under tests/output/ to inherit the candidate/ledger/
md_path/analysis fixtures (+ the autouse analyzer patch) from the output
conftest; the consistency claim it pins is naming-wide, not output-local.
"""

from __future__ import annotations

import scripts.ledger.naming as ledger_naming
import scripts.paths as paths
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


def test_dead_duplicate_helpers_diverge_from_live_authority(candidate, ledger):
    """The dead duplicates yield a DIFFERENT name on colon titles — the footgun
    the docstring NOTEs warn about. This pins WHY output.naming is authoritative.
    """
    title = candidate["title"]  # "DiffusionDrive: Truncated Diffusion ..."
    intake = ledger.intake_date()

    live = vault_key(intake=intake, title=title, arxiv_id=candidate["arxiv_id"], doi=None)
    # Live authority splits on ':' -> short paper-name only.
    assert "_DiffusionDrive_" in live

    # paths.vault_key / ledger.naming.vault_entry_name do NOT split on ':' -> the
    # full title camel-cased. Same identity suffix, but a divergent {Name}.
    paths_key = paths.vault_key(
        intake_date=intake.isoformat(),
        title=title,
        arxiv_base=candidate["arxiv_id"],
        doi=None,
    )
    ledger_key = ledger_naming.vault_entry_name(
        ingest_date=intake.isoformat(),
        title=title,
        arxiv_id=candidate["arxiv_id"],
        doi=None,
    )
    # Both dead helpers keep the full title camel-name (no ':' split) -> diverge
    # from the live authority. (They also differ from EACH OTHER on truncation
    # bound — paths caps at 48, ledger at 40 — underscoring there is exactly one
    # authority, not three interchangeable ones.)
    assert paths_key != live
    assert ledger_key != live
    assert "_DiffusionDriveTruncated" in paths_key
    assert "_DiffusionDriveTruncated" in ledger_key
