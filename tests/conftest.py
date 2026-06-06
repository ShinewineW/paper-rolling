# tests/conftest.py
"""Pytest bootstrap: put the skill ROOT on sys.path so the `scripts` package
imports resolve (`import scripts.paths`, `from scripts.discovery... import ...`)
without an install. Round 2 F1: the canonical namespace is `scripts.*`, so the
skill root (parent of `scripts/`) goes on the path — NOT the `scripts/` dir.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".claude" / "skills" / "paper-landscape"

if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

# Chunk 2 (ingest): make `from conftest import ...` resolve from test modules by
# putting this tests/ dir on sys.path (tests/__init__.py from Chunk 0 otherwise
# keeps the rootdir, not tests/, on the path under pytest's prepend import mode).
_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


# --- Chunk 2 (ingest) shared fixtures: offline HTTP seam, fake CLI runner, sample candidate ---

from dataclasses import dataclass, field  # noqa: E402

import pytest  # noqa: E402


@dataclass
class FakeHTTP:
    """Maps URL -> (status, body bytes). Records every requested URL."""

    routes: dict[str, tuple[int, bytes]] = field(default_factory=dict)
    requested: list[str] = field(default_factory=list)

    def add(self, url: str, status: int, body: bytes) -> None:
        self.routes[url] = (status, body)

    def __call__(self, url: str) -> tuple[int, bytes]:
        self.requested.append(url)
        if url in self.routes:
            return self.routes[url]
        return (404, b"")


@dataclass
class CliCall:
    argv: list[str]
    cwd: str


@dataclass
class FakeCliResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


class FakeCli:
    """Fake CLI runner. Register a side_effect to drop files like the real tool."""

    def __init__(self) -> None:
        self.calls: list[CliCall] = []
        self._side_effect = None
        self._returncode = 0
        self._stderr = ""

    def program(self, *, returncode: int = 0, stderr: str = "", side_effect=None):
        self._returncode = returncode
        self._stderr = stderr
        self._side_effect = side_effect
        return self

    def __call__(self, argv: list[str], cwd: str) -> FakeCliResult:
        self.calls.append(CliCall(argv=list(argv), cwd=str(cwd)))
        if self._side_effect is not None:
            self._side_effect(argv, cwd)
        return FakeCliResult(returncode=self._returncode, stderr=self._stderr)


@pytest.fixture
def fake_http() -> FakeHTTP:
    return FakeHTTP()


@pytest.fixture
def fake_cli() -> FakeCli:
    return FakeCli()


@pytest.fixture
def candidate() -> dict:
    """A discovery-layer candidate (corpus.jsonl record subset, Chunk 1 output)."""
    return {
        "arxiv_id": "1706.03762",
        "arxiv_version": "v5",
        "doi": "10.5555/3295222.3295349",
        "title": "Attention Is All You Need",
        "oa_pdf_url": "https://arxiv.org/pdf/1706.03762v5",
    }


def write_mineru_output(out_dir: Path, *, md: str, images: list[str], content_list: str):
    """Helper a test can wire as fake_cli side_effect to emulate MinerU's drop."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "paper.md").write_text(md)
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)
    for name in images:
        (img_dir / name).write_bytes(b"\x89PNG\r\n")
    (out_dir / "content_list.json").write_text(content_list)


# --- Chunk 3 (ledger): make frozen dataclasses resolve under file-path imports ---
# The ledger tests load their engine modules via
# importlib.util.spec_from_file_location(...) + exec_module(...) WITHOUT
# registering the result in sys.modules. On Python 3.13, dataclasses'
# annotation resolver (_is_type) does sys.modules.get(cls.__module__).__dict__,
# which raises AttributeError: 'NoneType' has no '__dict__' for a frozen
# dataclass defined in an unregistered module (e.g. CorpusRecord in "corpus").
# Pre-register placeholder modules under the names those tests use so the
# resolver finds a real (empty) namespace. Conftest is imported before the test
# modules, so these placeholders are in place by exec_module time.
import types as _types  # noqa: E402

for _engine_mod_name in ("naming", "corpus", "store"):
    sys.modules.setdefault(_engine_mod_name, _types.ModuleType(_engine_mod_name))
