"""Integration tests for the production spoke (WIRING-1 fix).

Drives the concrete spoke end-to-end through the binding pipeline
(ingest -> branch2 -> G2 -> branch1 -> G3 -> done) with fully deterministic
injected seams, and a capstone that drives the whole campaign tick through
``run_campaign_tick`` so the gates run in a real executable pipeline — not just
unit tests with hand-built fakes.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from conftest import write_mineru_output
from scripts.audit.rigor_rubric import DIMENSION_KEYS
from scripts.audit.types import Finding, GateVerdict, Severity, SkepticVote
from scripts.campaign import CampaignConfig, write_campaign
from scripts.hub import run_campaign_tick
from scripts.ledger.store import Ledger
from scripts.paths import FAILURE_AUDIT_BLOCK, FAILURE_CONVERT_ERROR
from scripts.spoke import make_spoke

# --- shared deterministic fixtures (bundle + seams) ------------------------

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

# Source MD the fake MinerU "produces". It carries EVERY evidence number in the
# analysis bundle below (0.57 / 0.48 / 0.61 / 0.52 / 3.2) plus one $$ display
# block, so the honest skeptic seam grounds them all and the G3 equation gate
# (1 $$ block vs 1 content_list equation) passes.
_SOURCE_MD = (
    "# DiffusionDrive\n\n"
    "## Abstract\n"
    "We propose a truncated diffusion policy that reaches 0.61 NDS on nuScenes, "
    "improving over the VAD baseline (0.57 NDS, 0.48 mAP) by 3.2 points.\n\n"
    "## Method\n"
    "The loss is a denoising objective $$L = \\mathbb{E}\\|x - \\hat{x}\\|^2$$ truncated to k steps.\n\n"  # noqa: E501
    "## Experiments\n"
    "Table 1 reports 0.61 NDS and 0.52 mAP on the nuScenes validation split.\n"
)

# Analyzer-spoke bundle (same shape as tests/output/conftest.py). Evidence
# numbers all appear in _SOURCE_MD above.
_ANALYSIS = {
    "overview": "A truncated-diffusion planning policy.",
    # Headline contract → branch2 frontmatter → landscapes comparator.
    "headline_metric": "NDS",
    "headline_value": 0.61,
    "params_million": 60.0,
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


def _resolve_analysis(md_path, candidate, *, prior_failure=None):
    """Inject a fresh deep copy so producer mutations never leak across runs.

    Accepts the optional ``prior_failure`` kwarg a branch2 re-emit injects (ADR-0009);
    this fake ignores the feedback and returns the same clean bundle.
    """
    return copy.deepcopy(_ANALYSIS)


def _resolve_analysis_fabricating(*fabricated_numbers: str):
    """Analyzer variant that injects a fabricated evidence row whose numbers are
    ABSENT from _SOURCE_MD. Since G2 Layer-1 now confirms every verbatim-present
    number by code (the skeptic is no longer consulted for them), a genuine G2
    block requires a candidate the source does NOT contain — this is the only way
    to drive one. The fabricated cells fill the 3-column (Method/NDS/mAP) row."""

    def _resolve(md_path, candidate, *, prior_failure=None):
        bundle = copy.deepcopy(_ANALYSIS)
        bundle["evidence_tables"][0]["rows"].append(["Bogus", *fabricated_numbers])
        return bundle

    return _resolve


def _all_found_skeptic(numbers, source_md, claim_context):
    """Happy-path seam: every evidence number grounds in the source (clean paper)."""
    return tuple(SkepticVote(number=n, found_in_source=True) for n in numbers)


def _honest_skeptic(numbers, source_md, claim_context):
    """Realistic seam: a number grounds iff it actually appears in the source MD.

    This is what exposed Codex Round-10: when G2 over-collected identifier-glued
    digits (e.g. "01" from claim id C01), this honest check could not find them
    in the source and hard-blocked a legitimate paper.
    """
    return tuple(SkepticVote(number=n, found_in_source=(n in source_md)) for n in numbers)


def _skeptic_missing(*fabricated: str):
    """Build a seam that reports `fabricated` numbers as NOT found, rest found.

    Mirrors a real skeptic that locates every honest number in the source MD but
    flags a value the evidence invented (the highest poisoning risk).
    """

    fab = set(fabricated)

    def _seam(numbers, source_md, claim_context):
        return tuple(SkepticVote(number=n, found_in_source=(n not in fab)) for n in numbers)

    return _seam


def _good_rigor(ara_bundle):
    return {
        "dimensions": {
            k: {"score": 4, "strengths": [], "weaknesses": [], "suggestions": []}
            for k in DIMENSION_KEYS
        },
        "findings": [],
    }


def _entailed(claim, experiment_text):
    return (True, "experiment matches claim")


def _mineru_emitting(md_text: str):
    """Build a fake_cli side_effect that drops a MinerU bundle with one equation."""

    def _side_effect(argv, cwd):
        out = argv[argv.index("-o") + 1]
        write_mineru_output(
            Path(cwd, out),
            md=md_text,
            images=["fig1.png"],
            content_list='[{"type":"equation"}]',  # 1 typed block == 1 $$ in MD
        )

    return _side_effect


def _tier2_http(fake_http, candidate):
    """Force the tier-1 HTML to 404 so ingest demotes to tier-2 (MinerU)."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")


def _ledger(tmp_path: Path) -> Ledger:
    return Ledger(tmp_path)


def _low_rigor(ara_bundle):
    # All dims score 1 -> any-dim==1 -> Reject -> G3 SEAL2 hard-block (seal fails).
    return {
        "dimensions": {
            k: {"score": 1, "strengths": [], "weaknesses": ["insufficient"], "suggestions": []}
            for k in DIMENSION_KEYS
        },
        "findings": [],
    }


def _make_spoke(
    tmp_path,
    fake_http,
    fake_cli,
    *,
    analysis_md,
    skeptic_votes=_all_found_skeptic,
    rigor_scores=_good_rigor,
    max_gate_rounds=2,
    resolve_analysis=_resolve_analysis,
    write_report=None,
    faithfulness_judge=None,
):
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(analysis_md))
    return make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=resolve_analysis,
        skeptic_votes=skeptic_votes,
        rigor_scores=rigor_scores,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=max_gate_rounds,
        write_report=write_report,
        faithfulness_judge=faithfulness_judge,
    )


# --- HAPPY PATH ------------------------------------------------------------


def test_spoke_happy_path_produces_both_vaults(tmp_path, fake_http, fake_cli):
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)

    result = spoke(dict(_CANDIDATE))

    assert result.status == "done"
    assert result.attempted_tier == "2"
    person = Path(result.person_vault_path)
    ai = Path(result.ai_package_path)
    # Returned paths are produce_outputs' EXACT on-disk dirs (no re-derivation).
    assert person.is_dir()
    assert ai.is_dir()
    assert (person / "report.md").exists()
    assert (ai / "ara").is_dir()
    assert (ai / "ara" / "PAPER.md").exists()
    # G3 always writes the rigor seal report.
    assert (ai / "ara" / "level2_report.json").exists()


def test_spoke_stall_cancel_preserves_built_ara_as_scene(tmp_path, fake_http, fake_cli):
    """ADR-0011: a stall cancel must PRESERVE the paid-for ARA as a self-contained
    _failed scene, not reflex-delete it (the former known residual). The spoke catches
    SpokeCancelled, scenes the handed-off ARA, and reports FAILURE_STALLED."""
    import threading

    from scripts.paths import FAILURE_STALLED

    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)
    cancel = threading.Event()
    cancel.set()  # the hub's stall guard already fired before promotion

    result = spoke(dict(_CANDIDATE), cancel=cancel)

    assert result.status == "failed"
    assert result.failure_class == FAILURE_STALLED
    # The built ARA survives in a self-contained scene (NOT deleted).
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    assert scenes, "stall must leave a _failed/<key>/scene.json"
    ara_dirs = list((tmp_path / "_failed").glob("*/ai/ara"))
    assert ara_dirs and any(ara_dirs[0].iterdir()), "the built ARA must be preserved in the scene"
    # OT-5: neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_spoke_honest_skeptic_passes_and_links_paired_ai_package(tmp_path, fake_http, fake_cli):
    # Codex Round-10 regression (both findings): (1) an HONEST skeptic (a number
    # grounds iff it appears in the source MD) must NOT hard-block legitimate
    # output — G2 no longer over-collects identifier-glued digits like "01" from
    # claim ids. (2) the branch1 report links to the paired ai_package by the
    # REAL shared key, never the old "REPLACE_KEY" placeholder.
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        skeptic_votes=_honest_skeptic,
    )

    result = spoke(dict(_CANDIDATE))

    assert result.status == "done"  # NOT blocked by a spurious id-glued "01"
    ai = Path(result.ai_package_path)
    key = ai.name
    report = (Path(result.person_vault_path) / "report.md").read_text(encoding="utf-8")
    assert "REPLACE_KEY" not in report
    assert f"../../ai_package/{key}/ara/evidence/" in report


def test_spoke_tier1_synthesizes_content_list_and_passes(tmp_path, fake_http, fake_cli):
    """Tier-1 (pandoc) emits no content_list.json; the spoke synthesizes one so
    G3's mechanical equation gate is a faithful pass-through (1 $$ block)."""
    cand = dict(_CANDIDATE)
    aid, ver = cand["arxiv_id"], cand["arxiv_version"]
    # Tier-1 HTML available with math so ingest stays on tier-1 (no demote).
    fake_http.add(
        f"https://arxiv.org/html/{aid}{ver}", 200, b"<html><math><mi>x</mi></math></html>"
    )

    def _pandoc(argv, cwd):
        out = argv[argv.index("-o") + 1]
        Path(cwd, out).write_text(_SOURCE_MD, encoding="utf-8")

    fake_cli.program(returncode=0, side_effect=_pandoc)
    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
    )

    result = spoke(cand)

    assert result.status == "done"
    assert result.attempted_tier == "1"
    assert Path(result.ai_package_path).is_dir()
    # The synthetic content_list.json was written next to the {ID}.md in corpus/.
    assert any((tmp_path / "corpus").rglob("content_list.json"))


# --- G2 HARD BLOCK ---------------------------------------------------------


def test_spoke_g2_block_aborts_before_any_vault(tmp_path, fake_http, fake_cli):
    # The evidence carries a fabricated number (888.88) absent from the source MD;
    # it escalates past Layer-1 and the honest skeptic flags it -> G2 hard-blocks
    # BEFORE branch1/promotion.
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        skeptic_votes=_honest_skeptic,
        resolve_analysis=_resolve_analysis_fabricating("888.88", "777.77"),
    )

    result = spoke(dict(_CANDIDATE))

    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
    assert "G2" in result.failure_reason
    assert result.person_vault_path is None
    assert result.ai_package_path is None
    # OT-5: nothing reached the real vaults.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())
    # audit F: a self-contained scene (not a throwaway note) preserves the staged ai/.
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    assert scenes, "expected a _failed/<key>/scene.json"
    m = json.loads(scenes[0].read_text(encoding="utf-8"))
    assert m["failed_gate"] == "数字门"
    assert (scenes[0].parent / "ai" / "ara").is_dir()


def test_spoke_forced_candidate_still_g2_blocked(tmp_path, fake_http, fake_cli):
    # 中枢-D1 invariant: a force-included paper is mandatory to ATTEMPT, NOT exempt
    # from the quality gates. A forced candidate carrying a fabricated number must
    # be G2 hard-blocked exactly like a discovered one — the spoke never branches
    # on `forced`, so it quarantines instead of polluting the vaults.
    forced = {**_CANDIDATE, "forced": True, "discovery_sources": ["forced"]}
    _tier2_http(fake_http, dict(forced))
    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        skeptic_votes=_honest_skeptic,
        resolve_analysis=_resolve_analysis_fabricating("888.88", "777.77"),
    )

    result = spoke(dict(forced))

    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
    assert "G2" in result.failure_reason
    assert result.person_vault_path is None
    assert result.ai_package_path is None


def test_g2_blind_retry_recalls_analyzer(tmp_path, fake_http, fake_cli):
    """审计 E / ADR-0006:数字门盲重试 = 重调 analyzer(fresh 采样),不注入 verdict。
    第一轮 analyzer 吐一个源文里没有的证据数字 → 诚实 skeptic 在 strict 模式 hard-block;
    第二轮吐干净 bundle → 放行。断言 resolve_analysis 被重调(计数=2)且重试未注入 prior_failure。"""
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    seen_prior: list = []

    def flaky_analyzer(md_path, candidate, *, prior_failure=None):
        seen_prior.append(prior_failure)
        bundle = copy.deepcopy(_ANALYSIS)
        if len(seen_prior) == 1:
            # Round 1: a fabricated evidence number absent from _SOURCE_MD → the
            # honest skeptic flags it → G2 strict hard-block.
            bundle["evidence_tables"][0]["rows"].append(["Bogus", "888.88", "777.77"])
        return bundle

    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=flaky_analyzer,
        skeptic_votes=_honest_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        g2_blind_retry_rounds=1,
    )

    result = spoke(dict(_CANDIDATE))

    assert result.status == "done"  # the fresh round-2 sampling passed G2
    assert len(seen_prior) == 2  # analyzer was RE-CALLED (fresh sampling), not re-rendered
    assert seen_prior == [None, None]  # blind retry: NO verdict/feedback injected


# --- STRUCTURAL GATE (Seal-1) ----------------------------------------------


def test_spoke_structural_seal_failure_writes_scene(tmp_path, fake_http, fake_cli, monkeypatch):
    """审计 R1 Finding 1:Seal-1 结构校验失败 → StructuralSealFailed 被 spoke 接住,写
    failed_gate='结构门' 自包含现场(根在 branch2),不逃逸成泛化 stalled、不污染 vault。"""
    import scripts.output.produce as prod

    # Force Seal-1 to hard-fail AFTER write_branch2 staged a real ara/ (so the scene
    # captures staged ai/), BEFORE G2 — exercises the structural-gate handler only.
    monkeypatch.setattr(
        prod,
        "validate_ara_tree",
        lambda _ara: ["N1: also_depends_on references unknown node 'D'"],
    )
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)

    result = spoke(dict(_CANDIDATE))  # must NOT raise StructuralSealFailed

    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
    assert result.person_vault_path is None and result.ai_package_path is None
    # OT-5: nothing reached the vaults.
    assert not (tmp_path / "ai_package").exists() or not any(
        p for p in (tmp_path / "ai_package").iterdir() if p.name != ".gitkeep"
    )
    # Self-contained structural-gate scene with the staged ai/ara preserved.
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    assert scenes, "expected a _failed/<key>/scene.json"
    m = json.loads(scenes[0].read_text(encoding="utf-8"))
    assert m["failed_gate"] == "结构门"
    assert (scenes[0].parent / "ai" / "ara").is_dir()


# --- G3 SEAL FAIL (post-promotion cleanup) ---------------------------------


def test_spoke_g3_failure_removes_promoted_vault(tmp_path, fake_http, fake_cli):
    # Codex Round-6 regression: G3 runs AFTER produce_outputs already promoted
    # both vaults. If the seal fails for the whole budget, the promoted
    # ai_package/ + person_vault/ products MUST be removed — otherwise a
    # failed-seal paper pollutes the library AND the cross-paper landscape (which
    # scans ai_package/*/ara/PAPER.md, not ledger status).
    from scripts.landscapes import generate_landscapes

    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        rigor_scores=_low_rigor,  # every dim scores 1 -> seal hard-fails every round
        max_gate_rounds=2,
    )

    result = spoke(dict(_CANDIDATE))

    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
    assert result.person_vault_path is None
    assert result.ai_package_path is None
    # No vault products remain — the seal-failed paper left NOTHING behind.
    ai_root = tmp_path / "ai_package"
    pv_root = tmp_path / "person_vault"
    assert not ai_root.exists() or not any(p for p in ai_root.iterdir() if p.name != ".gitkeep")
    assert not pv_root.exists() or not any(p for p in pv_root.iterdir() if p.name != ".gitkeep")
    # audit F: the promoted products are preserved as a self-contained final-gate
    # scene (moved out of the vault into _failed/<key>/), not just deleted.
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    assert scenes, "expected a _failed/<key>/scene.json"
    m = json.loads(scenes[0].read_text(encoding="utf-8"))
    assert m["failed_gate"] == "最终门"
    assert (scenes[0].parent / "ai").is_dir() and (scenes[0].parent / "person").is_dir()
    # And the cross-paper landscape does NOT include the failed paper.
    land = generate_landscapes(tmp_path, topic="real-time planning")
    assert land.paper_count == 0


# --- G3 BRANCH-LEVEL RE-EMIT DISPATCH (Task 4.4) ---------------------------


def _hard_verdict(gate: str, target: str, obs: str = "forced") -> GateVerdict:
    return GateVerdict(
        gate=gate,
        findings=(
            Finding(
                finding_id="F01",
                severity=Severity.CRITICAL,
                target=target,
                observation=obs,
                is_hard_block=True,
            ),
        ),
    )


def test_g3_reemit_seals_fresh_not_stale(tmp_path, fake_http, fake_cli):
    """R2 Finding 1: _on_g3_reemit rebinds `produced` (nonlocal), so round 2 seals
    the FRESH re-emitted product. rigor low→good across rounds → re-emit then pass."""
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    rigor_calls = {"n": 0}

    def flaky_rigor(bundle):
        rigor_calls["n"] += 1
        return _low_rigor(bundle) if rigor_calls["n"] == 1 else _good_rigor(bundle)

    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=flaky_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=2,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "done"  # round-2 fresh product sealed
    assert rigor_calls["n"] == 2  # G3 ran twice (round 1 low re-emitted, round 2 good)


def test_g3_ingest_root_raises_to_scene(tmp_path, fake_http, fake_cli, monkeypatch):
    """R1 Finding 5: an ingest-rooted G3 finding (equation fidelity) is unfixable →
    _Unfixable → 最终门 scene; never re-emits a branch, never escapes as stalled."""
    import scripts.audit.g3_seal as g3

    monkeypatch.setattr(
        g3,
        "check_equation_fidelity",
        lambda _md, _cl: _hard_verdict("equation-fidelity", "2411.15139v1.md", "eq mismatch"),
    )
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed" and result.failure_class == FAILURE_AUDIT_BLOCK
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    assert scenes and json.loads(scenes[0].read_text())["failed_gate"] == "最终门"
    ai_root = tmp_path / "ai_package"
    assert not ai_root.exists() or not any(p for p in ai_root.iterdir() if p.name != ".gitkeep")


def test_g3_branch2_reemit_hits_g2_lands_scene(tmp_path, fake_http, fake_cli):
    """branch2 re-emit (rigor root) re-samples the analyzer; if the fresh sample
    hits G2 before re-promotion → 数字门 scene, staged ai/ kept, old vault removed."""
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    acalls = {"n": 0}

    def flaky_analyzer(_md, _cand, *, prior_failure=None):
        acalls["n"] += 1
        bundle = copy.deepcopy(_ANALYSIS)
        if acalls["n"] >= 2:  # the branch2 re-emit fabricates a number → G2 blocks
            bundle["evidence_tables"][0]["rows"].append(["Bogus", "888.88", "777.77"])
        return bundle

    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=flaky_analyzer,
        skeptic_votes=_honest_skeptic,
        rigor_scores=_low_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=2,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed"
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    m = json.loads(scenes[0].read_text())
    assert m["failed_gate"] == "数字门"
    assert (scenes[0].parent / "ai" / "ara").is_dir()
    ai_root = tmp_path / "ai_package"
    assert not ai_root.exists() or not any(p for p in ai_root.iterdir() if p.name != ".gitkeep")


def test_g3_branch2_reemit_hits_seal1_lands_scene(tmp_path, fake_http, fake_cli, monkeypatch):
    """branch2 re-emit hits Seal-1 → 结构门 scene; _findings_of(StructuralSealFailed)
    lands non-empty findings; staged ai/ kept; old vault removed."""
    import scripts.output.produce as prod

    real_validate = prod.validate_ara_tree
    vcalls = {"n": 0}

    def flaky_validate(ara):
        vcalls["n"] += 1
        if vcalls["n"] == 1:
            return real_validate(ara)
        return ["N1: also_depends_on references unknown node 'D'"]

    monkeypatch.setattr(prod, "validate_ara_tree", flaky_validate)
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_low_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=2,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed"
    scenes = list((tmp_path / "_failed").glob("*/scene.json"))
    m = json.loads(scenes[0].read_text())
    assert m["failed_gate"] == "结构门"
    assert m["attempts"][-1]["findings"]  # _findings_of(StructuralSealFailed) non-empty
    assert (scenes[0].parent / "ai" / "ara").is_dir()


def test_g3_branch2_root_recalls_analyzer_with_feedback(tmp_path, fake_http, fake_cli):
    """rigor (branch2) root → _attempt(prior_failure_analyzer=...) re-samples the
    analyzer WITH the feedback injected (audit R8, moved from 4.3)."""
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    seen: list = []

    def rec_analyzer(_md, _cand, *, prior_failure=None):
        seen.append(prior_failure)
        return copy.deepcopy(_ANALYSIS)

    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=rec_analyzer,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_low_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=2,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed"  # rigor always low → escalates to a scene
    assert len(seen) >= 2  # analyzer was re-sampled on the branch2 re-emit
    assert any(p is not None for p in seen[1:])  # the re-emit injected prior_failure feedback


def test_g3_branch1_root_reuses_branch2(tmp_path, fake_http, fake_cli, monkeypatch):
    """ADR-0012 rev: the only branch1 G3 root left is G3R0 (missing report.md). It →
    _attempt(prior_failure_branch1=...) REUSES the branch2 SSOT: the analyzer is NOT
    re-sampled (audit R8, retargeted from the retired anchor root to G3R0)."""
    import scripts.output.produce as prod

    def noop_wb1(person_dir, *a, **k):
        # person/ exists but report.md is NEVER written → G3R0 (missing report.md).
        person_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(prod, "write_branch1", noop_wb1)
    _tier2_http(fake_http, dict(_CANDIDATE))
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    acalls = {"n": 0}

    def counting_analyzer(_md, _cand, *, prior_failure=None):
        acalls["n"] += 1
        return copy.deepcopy(_ANALYSIS)

    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=counting_analyzer,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=2,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed"  # report.md never written → G3R0 always → scene
    assert acalls["n"] == 1  # branch1 re-emit reused branch2 — analyzer NOT re-sampled


# --- branch1 ANCHOR GATE (failure isolation) ------------------------------


def test_spoke_unanchored_prose_claim_now_passes(tmp_path, fake_http, fake_cli):
    # ADR-0012: prose-anchor requirement dropped — a branch1 empirical claim
    # that cannot be grounded in the MD no longer raises AnchorGateError.
    # The spoke MUST succeed (status=done), not quarantine. Faithfulness is
    # branch1_gate's job, not the anchor lint's.
    _tier2_http(fake_http, dict(_CANDIDATE))
    bad = copy.deepcopy(_ANALYSIS)
    # The ONLY claim cites "99 NDS", which never appears in _SOURCE_MD. Under the
    # old contract this caused AnchorGateError; after ADR-0012 it is allowed.
    bad["claims"] = [
        {
            "id": "C99",
            "title": "Unanchorable perf",
            "statement": "Reaches 99 NDS on the held-out split.",
            "status": "supported",
            "falsification": "NDS < baseline",
            "proof": ["E01"],
            "evidence_basis": "Table 1 NDS column",
            "interpretation": "",
            "tags": "planning",
        },
    ]

    def _bad_analysis(md_path, candidate):
        return copy.deepcopy(bad)

    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_bad_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        # Production default from AuditConfig.data_fidelity_tolerant=True; the report
        # gate reuses g2_tolerant so we must match the production value here (ADR-0012).
        g2_tolerant=True,
        g2_max_unconfirmed=5,
        g2_max_unconfirmed_ratio=0.2,
    )

    result = spoke(dict(_CANDIDATE))
    # ADR-0012: prose number no longer blocked by anchor lint → spoke succeeds.
    assert result.status == "done"


# --- INGEST FAIL -----------------------------------------------------------


def test_spoke_ingest_failure_quarantines(tmp_path, fake_http, fake_cli):
    cand = dict(_CANDIDATE)
    aid, ver = cand["arxiv_id"], cand["arxiv_version"]
    # Both tiers fail: HTML 404 + PDF url unregistered (404) -> IngestFailed.
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)

    result = spoke(cand)

    assert result.status == "failed"
    assert result.failure_class == FAILURE_CONVERT_ERROR
    assert result.attempted_tier == "1,2"
    assert result.person_vault_path is None
    # ingest.quarantine wrote the per-paper _failed/{ID}.json record (the ingest
    # short_name caps the title slug at 40 chars).
    assert (
        tmp_path / "_failed" / "2411.15139v1_DiffusionDriveTruncatedDiffusionForRealT.json"
    ).exists()


# --- CAPSTONE: full campaign tick through run_campaign_tick -----------------


def test_campaign_tick_runs_spoke_and_builds_landscape(tmp_path, fake_http, fake_cli):
    # Lock a campaign so gate_needed() is False (no HITL re-gate this tick).
    write_campaign(
        tmp_path,
        CampaignConfig(
            topic="real-time diffusion planning",
            n_per_tick=1,
            is_ad_domain=True,
        ),
    )
    _tier2_http(fake_http, dict(_CANDIDATE))
    ledger = _ledger(tmp_path)
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(_SOURCE_MD))
    spoke = make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=_all_found_skeptic,
        rigor_scores=_good_rigor,
        entailment_judge=_entailed,
        ledger=ledger,
    )

    def _discover(topic, n):
        return [dict(_CANDIDATE)]

    tick = run_campaign_tick(
        workspace=tmp_path,
        ledger=ledger,
        discover=_discover,
        spoke=spoke,
    )

    assert tick.hub.done_count >= 1
    # Landscape was generated for the locked topic slug.
    assert tick.landscape.index_path.exists()
    assert tick.landscape.report_path.exists()
    # End-to-end proof: branch2's headline frontmatter now FEEDS landscapes, so
    # the cross-paper table is non-empty for a real processed paper (not silently
    # skipped for lacking the headline keys).
    assert tick.landscape.paper_count >= 1
    # The ledger recorded a true-done row with both vault paths.
    done_rows = [r for r in ledger.entries() if r["status"] == "done"]
    assert done_rows
    row = done_rows[-1]
    assert row["person_vault_path"] and Path(row["person_vault_path"]).is_dir()
    assert row["ai_package_path"] and Path(row["ai_package_path"]).is_dir()


def test_sampled_is_deterministic_and_rate_bounded():
    """ROADMAP C2: cross-model sampling is deterministic per key and ~rate-bounded."""
    from scripts.spoke import _sampled

    assert _sampled("k", 0.0) is False  # off
    assert _sampled("k", 1.0) is True  # always
    assert _sampled("k", 0.5) == _sampled("k", 0.5)  # stable across calls
    hits = sum(_sampled(f"paper-{i}", 0.3) for i in range(1000))
    assert 200 <= hits <= 400  # ~30% within a loose band


# --- ADR-0012: branch1 忠实门 end-to-end ----------------------------------------


def test_spoke_branch1_passes_faithful_prose_numbers(tmp_path, fake_http, fake_cli):
    """ADR-0012: a report carrying grounded prose numbers must NOT be quarantined.

    The deterministic write_branch1 path derives the report from the ARA (which is
    itself grounded from the source MD), so the finished report naturally passes the
    忠实门. This test confirms the full gated pipeline (ingest → branch2 → G2 →
    branch1 → G3 → done) succeeds end-to-end when no faithfulness violation exists.
    """
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)
    result = spoke(dict(_CANDIDATE))
    assert result.status == "done"


def test_spoke_branch1_judge_note_never_blocks(tmp_path, fake_http, fake_cli):
    """ADR-0012 rev: the (c) faithfulness judge writes an opening 「评价」 note and
    NEVER blocks. Even a judge that voices a misgiving cannot fail the human report —
    the spoke still publishes, and its prose note is prepended to the report.
    """
    _tier2_http(fake_http, dict(_CANDIDATE))

    def _wary_judge(report_text, ara_dir, *, ungrounded=None):
        return "总体忠实,但个别表述可更贴近知识包。"

    def fake_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {
            "sections": {
                "01_导读": "本文提出一种方法,在整体质量上领先所有对比基线。",
            },
            "figures": [],
        }

    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        write_report=fake_write_report,
        faithfulness_judge=_wary_judge,
    )
    result = spoke(dict(_CANDIDATE))
    assert result.status == "done"
    report = (Path(result.person_vault_path) / "report.md").read_text(encoding="utf-8")
    assert "## 评价" in report and "总体忠实" in report
