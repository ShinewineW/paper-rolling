"""OT-3 deterministic Name derivation + OT-1 vault key + key helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Import the engine module by file path (greenfield package not yet installed).
_NAMING = (
    Path(__file__).resolve().parents[2] / ".claude/skills/paper-landscape/scripts/ledger/naming.py"
)
_spec = importlib.util.spec_from_file_location("naming", _NAMING)
naming = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(naming)


def test_derive_name_strips_and_camelcases():
    assert naming.derive_name("Attention Is All You Need") == "AttentionIsAllYouNeed"


def test_derive_name_dehyphenates():
    # OT-3: de-hyphenate — hyphenated tokens fuse into camel segments.
    assert naming.derive_name("End-to-End Object Detection") == "EndToEndObjectDetection"


def test_derive_name_drops_special_chars():
    assert (
        naming.derive_name("DiffusionDrive: Truncated Diffusion!")
        == "DiffusionDriveTruncatedDiffusion"
    )


def test_derive_name_truncates_at_40():
    long = "A " * 60  # 60 single-letter words → far over the cap
    out = naming.derive_name(long)
    assert len(out) <= 40
    assert out == "A" * 40


def test_derive_name_is_deterministic_across_calls():
    title = "Scaling Laws for Neural Language Models"
    assert naming.derive_name(title) == naming.derive_name(title)


def test_derive_name_empty_fallback():
    # All-special input must not produce an empty key (breaks vault paths).
    assert naming.derive_name("!!! @@@ ###") == "Untitled"


def test_identity_key_strips_arxiv_version():
    assert naming.identity_key(arxiv_id="2306.07349v3", doi=None) == "2306.07349"
    assert naming.identity_key(arxiv_id="2306.07349", doi=None) == "2306.07349"


def test_identity_key_doi_fallback_short_hash():
    k = naming.identity_key(arxiv_id=None, doi="10.1109/CVPR52688.2022.01164")
    assert k.startswith("doi-")
    assert len(k) == len("doi-") + 12  # 12-char short hash, OT-1


def test_version_key_keeps_version():
    assert naming.version_key("2306.07349", "v3", None) == "2306.07349v3"
    assert naming.version_key("2306.07349", "v1", None) == "2306.07349v1"


def test_version_key_doi_fallback():
    assert naming.version_key(None, None, "10.5555/x") == "10.5555/x"


def test_vault_entry_name_format():
    # OT-1: {ingest_date}_{Name}_{arxivid_base}
    name = naming.vault_entry_name(
        ingest_date="2026-06-05",
        title="DiffusionDrive: Truncated Diffusion",
        arxiv_id="2411.15139v2",
        doi=None,
    )
    assert name == "2026-06-05_DiffusionDriveTruncatedDiffusion_2411.15139"
