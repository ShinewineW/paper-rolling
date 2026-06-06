"""Shared fixtures for output-engine tests."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path

import pytest

# Round 2 F7: candidate is a plain dict (the discovery-layer output), not an object.
_CANDIDATE = {
    "arxiv_id": "2411.15139",
    "arxiv_version": "v1",
    "doi": None,
    "title": "DiffusionDrive: Truncated Diffusion for Real-Time Planning",
    "authors": ["Liao et al."],
    "year": 2026,
    "venue": "CVPR",
    "cited_by_count": 12,
    "github_repo": None,
    "github_stars": 0,
    "oa_pdf_url": "https://arxiv.org/pdf/2411.15139v1",
    "discovery_tier": "B",
    "discovery_sources": ["openalex"],
}


@dataclass
class FakeLedger:
    _intake: datetime.date = datetime.date(2026, 6, 5)
    code_refs: dict = field(default_factory=dict)

    def intake_date(self) -> datetime.date:
        return self._intake

    def record_code_ref(self, key: str, path: str) -> None:
        self.code_refs[key] = path


@pytest.fixture
def candidate() -> dict:
    return dict(_CANDIDATE)


@pytest.fixture
def ledger() -> FakeLedger:
    return FakeLedger()


@pytest.fixture
def md_path(tmp_path: Path) -> Path:
    """A minimal but realistic {ID}.md the report can anchor into."""
    p = tmp_path / "2411.15139v1_DiffusionDrive.md"
    p.write_text(
        "# DiffusionDrive\n\n"
        "## Abstract\n"
        "We propose a truncated diffusion policy that reaches 0.61 NDS on nuScenes, "
        "improving over the baseline by 3.2 points while running in real time.\n\n"
        "## Method\n"
        "The loss is a denoising objective $$L = \\mathbb{E}\\|x - \\hat{x}\\|^2$$ truncated to k steps.\n\n"  # noqa: E501
        "## Experiments\n"
        "Table 1 reports 0.61 NDS and 0.52 mAP on the nuScenes validation split.\n",
        encoding="utf-8",
    )
    return p


@pytest.fixture
def analysis() -> dict:
    """The analyzer-spoke bundle (Chunk 3 contract) for one paper."""
    return {
        "overview": "A truncated-diffusion planning policy.",
        "problem": {
            "observations": [
                {
                    "id": "O1",
                    "statement": "Diffusion planners are slow.",
                    "evidence": "§1",
                    "implication": "Not real-time.",
                }
            ],
            "gaps": [
                {
                    "id": "G1",
                    "statement": "No real-time diffusion planner.",
                    "caused_by": "O1",
                    "attempts": "full-chain sampling",
                    "why_fail": "too many steps",
                }
            ],
            "insight": {
                "statement": "Truncate the diffusion chain.",
                "derived_from": "O1",
                "enables": "real-time planning",
            },
            "assumptions": ["A1: validation split is representative."],
        },
        "claims": [
            {
                "id": "C01",
                "title": "Real-time accuracy",
                "statement": "Reaches 0.61 NDS in real time.",
                "status": "supported",
                "falsification": "NDS < baseline",
                "proof": ["E01"],
                "evidence_basis": "Table 1 NDS column",
                "interpretation": "",
                "tags": "planning",
            },
        ],
        "concepts": [
            {
                "name": "Truncated diffusion",
                "notation": "$k$-step",
                "definition": "Stop denoising at step k.",
                "boundary": "k>0",
                "related": "DDPM",
            },
            {
                "name": "NDS",
                "notation": "NDS",
                "definition": "nuScenes detection score.",
                "boundary": "nuScenes",
                "related": "mAP",
            },
            {
                "name": "Denoising loss",
                "notation": "$L$",
                "definition": "MSE on the clean signal.",
                "boundary": "Gaussian noise",
                "related": "score matching",
            },
            {
                "name": "Planning policy",
                "notation": "$\\pi$",
                "definition": "Maps state to trajectory.",
                "boundary": "ego frame",
                "related": "imitation",
            },
            {
                "name": "Real-time budget",
                "notation": "ms",
                "definition": "Per-frame latency cap.",
                "boundary": "<100ms",
                "related": "throughput",
            },
        ],
        "experiments": [
            {
                "id": "E01",
                "title": "nuScenes benchmark",
                "verifies": ["C01"],
                "setup": {
                    "model": "DiffusionDrive-B",
                    "hardware": "1x A100",
                    "dataset": "nuScenes",
                    "system": "PyTorch",
                },
                "procedure": ["Train on train split", "Evaluate on val split"],
                "metrics": "NDS, mAP",
                "expected": "Ours outperforms baseline on NDS",
                "baselines": "VAD",
                "dependencies": "none",
            },
            {
                "id": "E02",
                "title": "Latency study",
                "verifies": ["C01"],
                "setup": {
                    "model": "DiffusionDrive-B",
                    "hardware": "1x A100",
                    "dataset": "nuScenes",
                    "system": "PyTorch",
                },
                "procedure": ["Measure per-frame latency"],
                "metrics": "ms/frame",
                "expected": "Ours is faster than full-chain",
                "baselines": "full diffusion",
                "dependencies": "E01",
            },
            {
                "id": "E03",
                "title": "Truncation ablation",
                "verifies": ["C01"],
                "setup": {
                    "model": "DiffusionDrive-B",
                    "hardware": "1x A100",
                    "dataset": "nuScenes",
                    "system": "PyTorch",
                },
                "procedure": ["Sweep k"],
                "metrics": "NDS vs k",
                "expected": "Small k hurts accuracy",
                "baselines": "k=full",
                "dependencies": "E01",
            },
        ],
        "related_work": [
            {
                "id": "RW01",
                "cite": "VAD, 2023",
                "doi": "arXiv:2303.12077",
                "type": "baseline",
                "what_changed": "We add diffusion",
                "why": "multimodality",
                "claims": "C01",
                "adopted": "BEV encoder",
            },
        ],
        "architecture": "## Encoder\nBEV encoder.\n\n## TruncatedDiffusion\nDenoiser truncated to k steps.\n",  # noqa: E501
        "algorithm": "$$L = \\mathbb{E}\\|x-\\hat{x}\\|^2$$\nPseudocode: denoise k steps.\n",
        "constraints": "Assumes BEV inputs; limited to k>0.\n",
        "heuristics": [
            {
                "id": "H01",
                "desc": "Cosine noise schedule",
                "rationale": "stabilizes truncation",
                "sensitivity": "medium",
                "bounds": "k in [2,8]",
                "code_ref": "src/execution/diffusion.py",
                "source": "§3",
            },
        ],
        "configs_training": [
            {
                "name": "learning_rate",
                "value": "1e-4",
                "rationale": "AdamW default",
                "range": "1e-5..1e-3",
                "sensitivity": "medium",
                "source": "§4",
            },
        ],
        "configs_model": [
            {
                "name": "k_steps",
                "value": "4",
                "rationale": "latency/accuracy trade",
                "range": "2..8",
                "sensitivity": "high",
                "source": "§3",
            },
        ],
        "environment": {
            "python": "3.11",
            "framework": "PyTorch 2.3",
            "hardware": "A100",
            "deps": ["torch==2.3.0"],
            "seeds": "0",
        },
        "execution_stub": 'import torch\n\n\ndef truncated_denoise(x: torch.Tensor, k: int) -> torch.Tensor:\n    """Denoise x for k truncated steps."""\n    for _ in range(k):\n        x = x - 0.1 * x\n    return x\n',  # noqa: E501
        "innovations": [{"name": "Truncated diffusion", "grep": "truncated_denoise"}],
        "exploration_tree": [
            {
                "id": "N01",
                "type": "question",
                "support_level": "explicit",
                "source_refs": ["§1"],
                "title": "Can diffusion plan in real time?",
                "description": "Central question.",
                "children": [
                    {
                        "id": "N02",
                        "type": "experiment",
                        "support_level": "explicit",
                        "source_refs": ["Table 1"],
                        "title": "Truncate to k steps",
                        "result": "Maintains NDS",
                    },
                    {
                        "id": "N03",
                        "type": "dead_end",
                        "support_level": "inferred",
                        "title": "k=1 single step",
                        "hypothesis": "1 step suffices",
                        "failure_mode": "NDS collapses",
                        "lesson": "need k>=2",
                    },
                    {
                        "id": "N04",
                        "type": "decision",
                        "support_level": "inferred",
                        "title": "Pick k",
                        "choice": "k=4",
                        "alternatives": ["k=2", "k=8"],
                    },
                    {
                        "id": "N05",
                        "type": "experiment",
                        "support_level": "explicit",
                        "source_refs": ["§4"],
                        "title": "Latency",
                        "result": "Real time",
                    },
                    {
                        "id": "N06",
                        "type": "experiment",
                        "support_level": "explicit",
                        "source_refs": ["§4"],
                        "title": "Ablation",
                        "result": "k matters",
                    },
                    {
                        "id": "N07",
                        "type": "experiment",
                        "support_level": "explicit",
                        "source_refs": ["§5"],
                        "title": "Transfer",
                        "result": "Holds",
                    },
                    {
                        "id": "N08",
                        "type": "question",
                        "support_level": "inferred",
                        "title": "Other domains?",
                        "description": "Future work.",
                    },
                ],
            },
        ],
        "evidence_tables": [
            {
                "name": "table1_nuscenes",
                "source": "Table 1, §4",
                "caption": "nuScenes val results",
                "claims": "C01",
                "headers": ["Method", "NDS", "mAP"],
                "rows": [["VAD", "0.57", "0.48"], ["Ours", "0.61", "0.52"]],
            },
        ],
        "highlights": {"model_structure": True, "math": True, "loss": True},
    }


@pytest.fixture(autouse=True)
def _patch_analyzer(monkeypatch, analysis):
    """Inject the analyzer-spoke bundle so produce_outputs is hermetic.

    In production, Chunk 3's hub passes the real analysis bundle; in tests we
    patch the resolver the orchestrator calls. Autouse + guarded import so it
    is a no-op for the earlier tasks whose module does not yet exist.
    """
    try:
        import scripts.output.produce as prod
    except ModuleNotFoundError:
        return
    monkeypatch.setattr(prod, "resolve_analysis", lambda md_path, candidate: analysis)
