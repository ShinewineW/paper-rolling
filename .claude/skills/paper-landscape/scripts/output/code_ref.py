"""Shallow code analysis with clone-delete-pointer hygiene (分析-D1/D2/D3).

We do NOT keep a runnable copy of the source repo. We clone it shallow to a
temp location, resolve the pinned commit SHA, locate each innovation to a
`file:line` position by grep, write a self-contained pointer
(`branch2/src/code_ref.md` = GitHub URL + pinned SHA + innovation→file:line
map), then DELETE the entire clone. To re-run, a reader re-clones at the SHA.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


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
        if not path.is_file() or path.stat().st_size > 2_000_000:
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


def _render(
    github_repo: str | None, sha: str | None, located: list[tuple[Innovation, str | None]]
) -> str:
    lines = ["# Code Reference", ""]
    if github_repo is None:
        lines += ["**No public repository** — closed-source paper; code locations unavailable.", ""]
    else:
        lines += [
            f"- **Repository**: {github_repo}",
            f"- **Pinned commit**: `{sha}`",
            "- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.",  # noqa: E501
            "",
            "## Innovation → code location",
            "",
            "| Innovation | Location (`file:line`) |",
            "|---|---|",
        ]
        for innov, loc in located:
            lines.append(f"| {innov.name} | {loc if loc else '_not found_'} |")
        lines.append("")
    return "\n".join(lines)


def build_code_ref(
    github_repo: str | None,
    innovations: list[Innovation],
    out_path: Path,
    clone_root: Path,
    idbase: str,
) -> None:
    """Clone shallow, locate innovations, write pointer, delete clone.

    Args:
        github_repo: GitHub URL, or None for closed-source.
        innovations: Innovations to locate.
        out_path: Where to write `code_ref.md`.
        clone_root: Temp root for clones (gitignored, e.g. /tmp/paper-repos).
        idbase: Paper identity base used as the clone subdir name.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if github_repo is None:
        out_path.write_text(_render(None, None, []), encoding="utf-8")
        return

    repo_dir = clone_root / idbase
    if repo_dir.exists():
        shutil.rmtree(repo_dir, ignore_errors=True)
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    sha: str | None = None
    located: list[tuple[Innovation, str | None]] = []
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", github_repo, str(repo_dir)],
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
        sha = rev.stdout.strip()
        located = [(innov, _locate(repo_dir, innov.grep)) for innov in innovations]
    finally:
        shutil.rmtree(repo_dir, ignore_errors=True)

    out_path.write_text(_render(github_repo, sha, located), encoding="utf-8")
