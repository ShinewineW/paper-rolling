# tests/test_paths.py
"""Contract tests for the on-disk layout interface (scripts/paths.py).

Every other engine module depends on these names and helpers, so this is the
load-bearing interface test. Covers: directory-name constants, path builders,
deterministic vault keying (OT-3 no-LLM naming), and the OT-1 collision-proof
vault key.
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


def test_short_name_is_deterministic_and_sanitized():
    # OT-3: fixed deterministic algorithm, never LLM. Strip special chars,
    # CamelCase the significant words, truncate.
    assert paths.short_name("Attention Is All You Need") == "AttentionIsAllYouNeed"
    # Punctuation / colons / hyphens stripped, not turned into word breaks oddly.
    assert paths.short_name("DiffusionDrive: End-to-End Driving") == "DiffusionDriveEndToEndDriving"
    # Empty / junk title falls back to a stable token, never empty.
    assert paths.short_name("   ???   ") == "Untitled"
    # Same input always yields the same output (idempotent).
    title = "Denoising Diffusion Probabilistic Models"
    assert paths.short_name(title) == paths.short_name(title)


def test_short_name_truncates_long_titles():
    long_title = "A " * 100 + "VeryLongTrailingWord"
    name = paths.short_name(long_title)
    assert len(name) <= paths.MAX_SHORT_NAME_LEN
    assert name  # never empty


def test_vault_key_arxiv_includes_base_id_for_collision_safety():
    # OT-1: key = {intake_date}_{Name}_{arxivid_base} -> same day + same short
    # name no longer collide because the arxiv base id disambiguates.
    key = paths.vault_key(
        intake_date="2026-06-05",
        title="DiffusionDrive: End-to-End Driving",
        arxiv_base="2411.15139",
        doi=None,
    )
    assert key == "2026-06-05_DiffusionDriveEndToEndDriving_2411.15139"


def test_vault_key_non_arxiv_uses_doi_short_hash():
    # Non-arXiv paper -> DOI short hash disambiguator (OT-1).
    key = paths.vault_key(
        intake_date="2026-06-05",
        title="Some Closed Venue Paper",
        arxiv_base=None,
        doi="10.1109/CVPR.2026.01234",
    )
    prefix = "2026-06-05_SomeClosedVenuePaper_"
    assert key.startswith(prefix)
    suffix = key[len(prefix) :]
    assert len(suffix) == paths.DOI_HASH_LEN
    assert all(c in "0123456789abcdef" for c in suffix)
    # Deterministic for the same DOI.
    key2 = paths.vault_key(
        intake_date="2026-06-05",
        title="Some Closed Venue Paper",
        arxiv_base=None,
        doi="10.1109/CVPR.2026.01234",
    )
    assert key == key2


def test_vault_key_requires_an_identity():
    # Identity = arxiv_base || doi (per "同篇判定" identity rule). Neither -> error.
    import pytest

    with pytest.raises(ValueError):
        paths.vault_key(intake_date="2026-06-05", title="x", arxiv_base=None, doi=None)


def test_vault_entry_glob_matches_identity_ignoring_date_prefix():
    # OT-2: reprocessing locates the existing entry by identity, ignoring the
    # date prefix, so the old entry can be deleted and rewritten.
    g = paths.vault_entry_glob(arxiv_base="2411.15139", doi=None)
    assert g == "*_2411.15139"
    g_doi = paths.vault_entry_glob(arxiv_base=None, doi="10.1109/CVPR.2026.01234")
    # DOI glob uses the same short hash suffix as vault_key.
    assert g_doi.startswith("*_")
    assert g_doi.endswith(paths.doi_short_hash("10.1109/CVPR.2026.01234"))


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
