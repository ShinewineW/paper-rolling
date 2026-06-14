"""Deterministic vault naming + identity keys.

OT-3: `{Name}` derives from the arXiv title by a FIXED algorithm — no LLM
improvisation — so keys stay stable across runs and branch1↔branch2 pairing
never breaks. OT-1: vault key = `{intake_date}_{Name}_{idbase}` is unique even
when same-day same-shortname collide. OT-2: re-processing locates the prior
entry by identity (arxiv base id || DOI short-hash), ignoring its date prefix.
"""

from __future__ import annotations

import datetime
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

_KEEP = re.compile(r"[A-Za-z0-9]+")
_NAME_MAX = 60


def derive_name(title: str) -> str:
    """Derive a stable CamelCase `{Name}` from a paper title.

    Algorithm: take the substring before the first colon (the conventional
    paper short-name), tokenize on any non-alphanumeric run, CamelCase the
    tokens, truncate to 60 chars. Deterministic and idempotent.

    Args:
        title: Raw paper title.

    Returns:
        CamelCase identifier, never empty.

    Raises:
        ValueError: If the title yields no alphanumeric tokens.
    """
    head = title.split(":", 1)[0]
    tokens = _KEEP.findall(head)
    if not tokens:
        tokens = _KEEP.findall(title)
    if not tokens:
        raise ValueError(f"title yields empty Name: {title!r}")
    name = "".join(tok[:1].upper() + tok[1:] for tok in tokens)
    return name[:_NAME_MAX]


def identity_base(arxiv_id: str | None, doi: str | None) -> str:
    """Canonical paper-identity key: arXiv base id, else DOI short hash.

    The arXiv id is taken WITHOUT version suffix (identity, not idempotency).
    """
    if arxiv_id:
        # Strip ONLY a trailing version (v\d+$). A naive split("v") would also cut
        # old-style IDs like "solv-int/9901001v1" at the first 'v' → "sol" (Codex R16).
        return re.sub(r"v\d+$", "", arxiv_id)
    if doi:
        digest = hashlib.sha256(doi.strip().lower().encode("utf-8")).hexdigest()[:8]
        return f"doi-{digest}"
    raise ValueError("identity_base requires arxiv_id or doi")


def vault_key(
    intake: datetime.date,
    title: str,
    arxiv_id: str | None,
    doi: str | None,
) -> str:
    """Build the unique vault entry key `{YYYY-MM-DD}_{Name}_{idbase}` (OT-1)."""
    return f"{intake.isoformat()}_{derive_name(title)}_{identity_base(arxiv_id, doi)}"


def find_existing_entries(
    vault_dir: Path,
    arxiv_id: str | None,
    doi: str | None,
) -> list[Path]:
    """Locate prior vault entries for this identity, ignoring date prefix (OT-2).

    Matches any `*_{idbase}` directory so an earlier-dated entry of the same
    paper can be deleted and rewritten with the current intake date.
    """
    if not vault_dir.exists():
        return []
    idbase = identity_base(arxiv_id, doi)
    return sorted(p for p in vault_dir.iterdir() if p.is_dir() and p.name.endswith(f"_{idbase}"))


# --------------------------------------------------------------------------- #
# idbase -> on-disk product paths (the SINGLE external resolver)               #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class PaperPaths:
    """Every on-disk product path for one paper, resolved from its idbase.

    A paper's products span THREE dirs under TWO key schemes — `corpus/{idbase}_{Slug}`
    (the ingest `corpus_id`, full-title slug ≤40) and `person_vault|ai_package/
    {date}_{Name}_{idbase}` (the `vault_key`, before-colon name ≤60). NONE is keyed by
    bare idbase, and the corpus Slug differs from the vault Name — so the date prefix and
    both slugs are NOT recoverable from an idbase alone. Resolution is therefore by disk
    SCAN, not name recomputation. Each field is the resolved Path, or None if that product
    is absent (report_md/report_html/ara_dir are built from the found dir even if the file
    itself is not yet written, so a writer/REVISE caller gets the target path).
    """

    idbase: str
    corpus_dir: Path | None
    corpus_md: Path | None
    person_vault_dir: Path | None
    report_md: Path | None
    report_html: Path | None
    ai_package_dir: Path | None
    ara_dir: Path | None


def _one_dir(parent: Path, *, prefix: str = "", suffix: str = "") -> Path | None:
    """The single sub-dir of `parent` matching `prefix`/`suffix`, else None.

    None if `parent` is absent or nothing matches; the first (sorted) on the rare
    same-idbase collision the vault keying is designed to avoid.
    """
    if not parent.is_dir():
        return None
    hits = sorted(
        p
        for p in parent.iterdir()
        if p.is_dir() and p.name.startswith(prefix) and p.name.endswith(suffix)
    )
    return hits[0] if hits else None


def resolve_paper_paths(workspace: Path, idbase: str) -> PaperPaths:
    """Resolve every on-disk product path for `idbase` — the SINGLE authority for
    "idbase -> product paths". External callers (status, final-review orchestration,
    tooling) MUST use this instead of hand-globbing corpus/vault dirs, since the two
    key schemes (corpus_id vs vault_key) make ad-hoc reconstruction error-prone.

    `idbase` is the identity key (arXiv base id sans version, or `doi-<hash>`) — i.e.
    `identity_base(...)`, the same key vault dirs end with and corpus dirs start with.
    """
    ws = Path(workspace)
    corpus_dir = _one_dir(ws / "corpus", prefix=f"{idbase}_")
    corpus_md: Path | None = None
    if corpus_dir is not None:
        cand = corpus_dir / f"{corpus_dir.name}.md"
        if not cand.is_file():
            mds = sorted(corpus_dir.glob("*.md"))
            cand = mds[0] if mds else None
        corpus_md = cand
    pv = _one_dir(ws / "person_vault", suffix=f"_{idbase}")
    ai = _one_dir(ws / "ai_package", suffix=f"_{idbase}")
    return PaperPaths(
        idbase=idbase,
        corpus_dir=corpus_dir,
        corpus_md=corpus_md,
        person_vault_dir=pv,
        report_md=(pv / "report.md") if pv else None,
        report_html=(pv / "report.html") if pv else None,
        ai_package_dir=ai,
        ara_dir=(ai / "ara") if ai else None,
    )
