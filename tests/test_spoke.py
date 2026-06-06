"""Integration tests for the production spoke (WIRING-1 fix).

Drives the concrete spoke end-to-end through the binding pipeline
(ingest -> branch2 -> G2 -> branch1 -> G3 -> done) with fully deterministic
injected seams, and a capstone that drives the whole campaign tick through
``run_campaign_tick`` so the gates run in a real executable pipeline — not just
unit tests with hand-built fakes.
"""

from __future__ import annotations

import copy
from pathlib import Path

from conftest import write_mineru_output
from scripts.audit.rigor_rubric import DIMENSION_KEYS
from scripts.audit.types import SkepticVote
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


def _resolve_analysis(md_path, candidate):
    """Inject a fresh deep copy so producer mutations never leak across runs."""
    return copy.deepcopy(_ANALYSIS)


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
):
    fake_cli.program(returncode=0, side_effect=_mineru_emitting(analysis_md))
    return make_spoke(
        workspace=tmp_path,
        http=fake_http,
        run_cli=fake_cli,
        resolve_analysis=_resolve_analysis,
        skeptic_votes=skeptic_votes,
        rigor_scores=rigor_scores,
        entailment_judge=_entailed,
        ledger=_ledger(tmp_path),
        n_skeptics=3,
        max_gate_rounds=max_gate_rounds,
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
    # The majority of skeptics report the evidence number 0.61 as NOT found in
    # the source MD (fabricated/mis-transcribed) -> G2 hard-blocks BEFORE
    # branch1/promotion.
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(
        tmp_path,
        fake_http,
        fake_cli,
        analysis_md=_SOURCE_MD,
        skeptic_votes=_skeptic_missing("0.61"),
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
    # A _failed/ hand-off record exists.
    assert any((tmp_path / "_failed").glob("*.md"))


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
    # Quarantine record written.
    assert any((tmp_path / "_failed").glob("*.md"))
    # And the cross-paper landscape does NOT include the failed paper.
    land = generate_landscapes(tmp_path, topic="real-time planning")
    assert land.paper_count == 0


# --- branch1 ANCHOR GATE (failure isolation) ------------------------------


def test_spoke_unanchorable_claim_quarantines_not_crash(tmp_path, fake_http, fake_cli):
    # Codex Round-8 regression: a branch1 empirical claim that cannot be grounded
    # in the MD raises AnchorGateError in staging (pre-promotion). The spoke MUST
    # quarantine + return failed — NOT let the exception escape and crash the
    # unattended /loop tick.
    _tier2_http(fake_http, dict(_CANDIDATE))
    bad = copy.deepcopy(_ANALYSIS)
    # The ONLY claim cites "99 NDS", which never appears in _SOURCE_MD, so branch1
    # cannot anchor it. (The anchor lint is line-based, so the claim must stand
    # alone — an anchored sibling claim on the same paragraph line would mask it.)
    # The single unanchored number + metric cue makes the three-layer lint
    # hard-fail -> AnchorGateError inside write_branch1 (staging, pre-promotion).
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
    )

    result = spoke(dict(_CANDIDATE))  # must NOT raise AnchorGateError

    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
    assert "anchor" in result.failure_reason.lower()
    # Pre-promotion: nothing reached the vaults (OT-5 holds for the anchor gate too).
    assert not (tmp_path / "ai_package").exists() or not any(
        p for p in (tmp_path / "ai_package").iterdir() if p.name != ".gitkeep"
    )
    assert any((tmp_path / "_failed").glob("*.md"))


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
