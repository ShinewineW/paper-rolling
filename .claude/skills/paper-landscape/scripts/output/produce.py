"""Atomic dual-output orchestrator (OT-5) — public entrypoint.

`produce_outputs(md_path, candidate, ledger)` builds branch2 (ai_package) FIRST,
then branch1 (person_vault) DERIVED from it, in a STAGING directory; runs the
ARA Seal-1 validator + the three-layer anchor gate; and only on full success
moves BOTH into their vaults under one shared key (OT-5: both or neither).
Re-processing the same paper-identity deletes any prior same-identity entries
first (OT-2). Naming is deterministic (OT-3).

The hub (Chunk 3/5) supplies the analyzer bundle via `resolve_analysis`; tests
patch it. The contract is `produce_outputs(md_path, candidate, ledger) ->
ProduceResult(key=...)`.
"""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch1_report import write_branch1
from scripts.output.branch2_ara import write_branch2
from scripts.output.naming import find_existing_entries, vault_key


@dataclass(frozen=True)
class ProduceResult:
    """Outcome of one dual-output run."""

    key: str
    person_path: Path
    ai_path: Path


def resolve_analysis(md_path: Path, candidate: Any) -> dict:  # pragma: no cover
    """Return the analyzer-spoke bundle for this paper.

    Overridden by the hub (Chunk 3) at runtime and patched in tests. Importing
    the analyzer here would create a cross-chunk dependency, so the seam is a
    module-level function the caller injects.
    """
    raise NotImplementedError(
        "resolve_analysis must be provided by the hub (Chunk 3) before produce_outputs runs"
    )


def produce_outputs(
    md_path: Path,
    candidate: Any,
    ledger: Any,
    root: Path | None = None,
) -> ProduceResult:
    """Produce branch2 + branch1 atomically into the two top-level vaults.

    Args:
        md_path: Frozen {ID}.md (the MD-only truth base + anchor target).
        candidate: Discovery record (carries identity + metadata).
        ledger: Ledger; provides `intake_date()` and `record_code_ref(key, path)`.
        root: Workspace root containing `person_vault/` and `ai_package/`.
              Defaults to the current working directory.

    Returns:
        ProduceResult with the shared vault key and both final paths.

    Raises:
        Exception: Any failure aborts BEFORE either vault is touched (OT-5).
    """
    root = (root or Path.cwd()).resolve()
    person_vault = root / "person_vault"
    ai_package = root / "ai_package"

    key = vault_key(
        intake=ledger.intake_date(),
        title=candidate["title"],
        arxiv_id=candidate["arxiv_id"],
        doi=candidate["doi"],
    )
    analysis = resolve_analysis(md_path, candidate)

    # Stage everything in a temp dir; promote only after both gates pass.
    staging = Path(tempfile.mkdtemp(prefix="paper-rolling-stage-"))
    try:
        stage_ai = staging / "ai" / "ara"
        stage_person = staging / "person"
        write_branch2(stage_ai, candidate, analysis)

        ara_errors = validate_ara_tree(stage_ai)
        if ara_errors:
            raise ValueError(f"branch2 failed Seal-1: {'; '.join(ara_errors[:5])}")

        # branch1 derives from branch2 and self-gates on the anchor lint;
        # any unanchored empirical claim raises AnchorGateError here.
        write_branch1(stage_person, candidate, stage_ai, md_path, analysis)

        # Both gates passed → promote atomically. Remove prior same-identity
        # entries first (OT-2), then move staging into place.
        person_dest = person_vault / key
        ai_dest = ai_package / key
        person_vault.mkdir(parents=True, exist_ok=True)
        ai_package.mkdir(parents=True, exist_ok=True)
        for prior in find_existing_entries(person_vault, candidate["arxiv_id"], candidate["doi"]):
            shutil.rmtree(prior, ignore_errors=True)
        for prior in find_existing_entries(ai_package, candidate["arxiv_id"], candidate["doi"]):
            shutil.rmtree(prior, ignore_errors=True)
        if person_dest.exists():
            shutil.rmtree(person_dest)
        if ai_dest.exists():
            shutil.rmtree(ai_dest)
        shutil.move(str(stage_person), str(person_dest))
        shutil.move(str(staging / "ai"), str(ai_dest))

        ledger.record_code_ref(key, str(ai_dest / "ara" / "src/code_ref.md"))
        return ProduceResult(key=key, person_path=person_dest, ai_path=ai_dest)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
