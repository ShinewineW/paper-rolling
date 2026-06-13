"""Shallow code analysis with clone-delete-pointer hygiene (分析-D1/D2/D3).

We do NOT keep a runnable copy of the source repo. Given an ORDERED list of repo
candidates (see `repo_resolve.resolve_repo_candidates`), we clone each shallow to
a temp location, resolve the pinned commit SHA, and locate each innovation to a
`file:line` position by grep. The FIRST candidate that passes verification wins:

  * trust="official" (Papers-with-Code is_official) → accept on clone success;
  * trust="search"   (paper text / discovery / web) → accept only if a real match
    is found (an innovation symbol located, or the arxiv_id/title present in the
    repo) — this rejects look-alike reimplementations and cited-baseline repos.

We then write a self-contained pointer (`branch2/src/code_ref.md`) and DELETE the
clone. The pointer is THREE-STATE and never conflates "not found" with "closed":
  * found                     — repo + pinned SHA + innovation→file:line, + source.
                                file:line is SOURCE-only (no README/doc/config cites);
                                innovations that don't resolve are OMITTED, not faked;
  * searched, not found       — every tier ran, nothing verified (NOT closed-source);
  * author-declared closed    — only when the paper explicitly says code won't ship.
A DECLARED repo that is unreachable (clone failed) is recorded with provenance +
an "unavailable" note rather than crashing the paper (中枢-D2 / Codex R17).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from scripts.output.repo_resolve import RepoCandidate

# A "code location" must point at SOURCE, not prose/config. Restricting _locate to
# these suffixes kills the README.md:N / docs/*.rst / *.yaml false "locations" that
# made the innovation→file:line map untrustworthy (e.g. the bogus 'README.md:28').
# Acceptance is unaffected: a README-only match still verifies via _repo_mentions.
_CODE_EXT = frozenset(
    {
        ".py",
        ".pyx",
        ".ipynb",
        ".cpp",
        ".cc",
        ".cxx",
        ".c",
        ".h",
        ".hpp",
        ".cuh",
        ".cu",
        ".java",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".go",
        ".rs",
        ".scala",
        ".lua",
        ".m",
        ".mm",
        ".swift",
        ".kt",
        ".sh",
        ".rb",
        ".jl",
    }
)


@dataclass(frozen=True)
class Innovation:
    """One innovation/highlight to locate in the code.

    Attributes:
        name: Human label (e.g. "Truncated diffusion loss").
        grep: A literal substring (class/function/symbol) to search for.
    """

    name: str
    grep: str


def _locate(repo_dir: Path, needle: str) -> str | None:
    """Return the first `relpath:line` whose line contains `needle`, else None."""
    for path in sorted(repo_dir.rglob("*")):
        # Skip VCS internals (.git/index etc.): binary blobs yield garbage
        # "matches" for short needles, polluting the trace layer's credibility.
        if ".git" in path.parts:
            continue
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        # A code location must be SOURCE, not a README/doc/config match (honesty:
        # don't report 'README.md:28' as where an innovation lives).
        if path.suffix.lower() not in _CODE_EXT:
            continue
        try:
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
            ):
                if needle in line:
                    return f"{path.relative_to(repo_dir).as_posix()}:{lineno}"
        except OSError:
            continue
    return None


def _repo_mentions(repo_dir: Path, needles: list[str]) -> bool:
    """True if any needle (arxiv_id / title) appears in README* or a top-level .md.

    Cheap verification signal for a "search" candidate: an OFFICIAL repo's README
    almost always cites its own arxiv id or paper title; a reimplementation or a
    cited-baseline repo usually does not. Bounded to docs to stay fast (symbol
    location already does the full-tree scan).
    """
    needles_l = [n.lower() for n in needles if n]
    if not needles_l:
        return False
    docs = sorted(repo_dir.glob("README*")) + sorted(repo_dir.glob("*.md"))
    for path in docs:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if any(n in text for n in needles_l):
            return True
    return False


@dataclass(frozen=True)
class _Probe:
    """Result of cloning + probing one candidate."""

    sha: str | None
    located: list[tuple[Innovation, str | None]]
    clone_error: str | None


def _clone_and_probe(url: str, innovations: list[Innovation], repo_dir: Path) -> _Probe:
    """Shallow-clone `url` into `repo_dir`, resolve SHA, locate innovations.

    Caller owns `repo_dir` lifecycle (rmtree before/after). Returns clone_error
    (exception class name) instead of raising, so one bad candidate never crashes
    the paper.
    """
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(repo_dir)],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        rev = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        located = [(innov, _locate(repo_dir, innov.grep)) for innov in innovations]
        return _Probe(sha=rev.stdout.strip(), located=located, clone_error=None)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        return _Probe(sha=None, located=[], clone_error=type(exc).__name__)


def _accepts(
    cand: RepoCandidate, probe: _Probe, *, arxiv_id: str | None, title: str | None, repo_dir: Path
) -> bool:
    """Verification gate: should this cloned candidate be accepted as THE repo?"""
    if cand.trust == "official":
        return True  # Papers-with-Code is_official — accept on a clean clone.
    if any(loc for _, loc in probe.located):
        return True  # an innovation symbol resolved -> this is (almost surely) the repo.
    return _repo_mentions(repo_dir, [n for n in (arxiv_id, title) if n])


def _render_found(
    cand: RepoCandidate, sha: str | None, located: list[tuple[Innovation, str | None]]
) -> str:
    verified = "official-flagged" if cand.trust == "official" else "verified"
    lines = [
        "# Code Reference",
        "",
        f"- **Repository**: {cand.url}",
        f"- **Pinned commit**: `{sha}`",
        f"- **Source**: {cand.source} ({verified})",
        "- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.",  # noqa: E501
        "",
    ]
    # Honesty: only render innovations that mechanically RESOLVED to a source location.
    # A table full of '_not found_' rows (or fabricated doc-file cites) is worse than
    # silence — omit the map entirely and say so, keeping the verified repo + SHA.
    resolved = [(innov, loc) for innov, loc in located if loc]
    if resolved:
        lines += [
            "## Innovation → code location",
            "",
            "| Innovation | Location (`file:line`) |",
            "|---|---|",
        ]
        lines += [f"| {innov.name} | {loc} |" for innov, loc in resolved]
        lines.append("")
    else:
        lines += [
            "- **Innovation → code location**: not mechanically resolved at this commit "
            "(symbols not located in source); see the repo at the pinned SHA.",
            "",
        ]
    return "\n".join(lines)


def _render_unreachable(cand: RepoCandidate, clone_error: str) -> str:
    return "\n".join(
        [
            "# Code Reference",
            "",
            f"- **Repository (declared)**: {cand.url}",
            f"- **Source**: {cand.source}",
            f"- **Status**: unavailable — clone failed (`{clone_error}`); "
            "code locations could not be resolved.",
            "- **Note**: the link is recorded for provenance; re-resolve when reachable.",
            "",
        ]
    )


def _render_none(*, declared_closed: bool) -> str:
    lines = ["# Code Reference", ""]
    if declared_closed:
        lines += [
            "**Author-declared closed-source** — the paper states the code will not be "
            "released; there is no repository to link.",
            "",
        ]
    else:
        lines += [
            "**No public repository found** — searched the paper text and the "
            "Papers-with-Code official-repo index; nothing was found or passed "
            "verification. This is NOT a closed-source determination.",
            "",
        ]
    return "\n".join(lines)


def build_code_ref(
    candidates: list[RepoCandidate],
    innovations: list[Innovation],
    out_path: Path,
    clone_root: Path,
    idbase: str,
    *,
    arxiv_id: str | None = None,
    title: str | None = None,
    declared_closed: bool = False,
) -> None:
    """Clone-verify candidates in order, write a three-state pointer, delete clones.

    Args:
        candidates: Ordered repo candidates (see resolve_repo_candidates). Empty ->
            "searched, not found" (or "author-declared closed" if declared_closed).
        innovations: Innovations to locate (also a verification signal).
        out_path: Where to write `code_ref.md`.
        clone_root: Temp root for clones (gitignored, e.g. /tmp/paper-repos).
        idbase: Paper identity base used as the clone subdir name.
        arxiv_id, title: Used by the verification gate to confirm a "search" repo.
        declared_closed: True only if the paper explicitly declares closed-source.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not candidates:
        out_path.write_text(_render_none(declared_closed=declared_closed), encoding="utf-8")
        return

    repo_dir = clone_root / idbase
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    unreachable: tuple[RepoCandidate, str] | None = None
    try:
        for cand in candidates:
            if repo_dir.exists():
                shutil.rmtree(repo_dir, ignore_errors=True)
            probe = _clone_and_probe(cand.url, innovations, repo_dir)
            if probe.clone_error is not None:
                # A DECLARED repo (not a speculative web hit) that won't clone is
                # recorded with provenance if nothing better is accepted later.
                if cand.source != "websearch" and unreachable is None:
                    unreachable = (cand, probe.clone_error)
                continue
            if _accepts(cand, probe, arxiv_id=arxiv_id, title=title, repo_dir=repo_dir):
                out_path.write_text(_render_found(cand, probe.sha, probe.located), encoding="utf-8")
                return
        # Nothing accepted: an unreachable declared repo beats a bare "not found".
        if unreachable is not None:
            out_path.write_text(_render_unreachable(*unreachable), encoding="utf-8")
        else:
            out_path.write_text(_render_none(declared_closed=declared_closed), encoding="utf-8")
    finally:
        shutil.rmtree(repo_dir, ignore_errors=True)
