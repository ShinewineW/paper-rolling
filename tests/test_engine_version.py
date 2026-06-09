from pathlib import Path

from scripts.engine_version import current_commit


def test_current_commit_real_repo_short_hash():
    assert isinstance(current_commit(Path(".")), str) and len(current_commit(Path("."))) >= 3


def test_current_commit_non_git_unknown(tmp_path):
    assert current_commit(tmp_path) == "unknown"
