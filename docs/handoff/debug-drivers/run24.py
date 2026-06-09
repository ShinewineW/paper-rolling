# attn_sink/cosmos_trial/run24.py
"""Batch run the 24 world-model / world-action-model papers, max_concurrent=2.

WHY a custom dispatcher instead of `run_tick`:
    hub.run_tick's `max_concurrent` is a NO-OP — its reference loop processes
    papers strictly SEQUENTIALLY (the docstring says "the real harness fans them
    out via the Agent/Task tool"). For a FIXED 24-paper list we don't need
    run_tick's discovery/backfill/N-target machinery, so this driver reuses the
    tested SPOKE directly across a `ThreadPoolExecutor(max_workers=2)` and is the
    single ledger writer (a threading.Lock serializes `ledger.record`, preserving
    the single-writer invariant). Per-paper isolation + wall-clock cap + EngineAbort
    re-raise all come from `hub._run_spoke_guarded`, unchanged.

Safety budget:
    * global `claude -p` concurrency is hard-capped at 5 in providers.py, so 2
      concurrent papers (each analyzer = up to 5 chunks) can never exceed 5 → no
      rate-limit stall (the failure mode from the first overnight run).
    * `build_http` (fresh requests.get per call) and `build_run_cli` (stateless
      subprocess.run) are both thread-safe; the spoke has no module-global state
      (spoke.py:150). Distinct papers write distinct corpus/ + vault dirs.

Skip / reprocess:
    ledger.skip_set() contains only `done` papers (store.py:142). The 2 already-
    promoted Cosmos papers (2503.14492 / 2503.15558) are NOT in this list and
    stay skipped; the 3 ingested-but-FAILED ones (2511.00062 / 2501.03575 /
    2606.02800) are NOT in skip_set, so they reprocess (ingest re-runs — accepted
    cost, no engine change).

Run (background):
    PYTHONPATH=.claude/skills/paper-landscape \
      uv run python attn_sink/cosmos_trial/run24.py
"""

from __future__ import annotations

import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.adapters import build_http, build_run_cli
from scripts.audit_config import load_audit_config
from scripts.hub import _candidate_key, _quarantine, _run_spoke_guarded
from scripts.ledger.store import Ledger
from scripts.llm.seams import build_seams
from scripts.paths import FAILURE_STALLED, EngineAbort
from scripts.spoke import make_spoke

W = Path(".").resolve()
OUT = Path(__file__).parent
TOPIC = "world model and world-action model for embodied AI and autonomous driving"

MAX_CONCURRENT = 2
PER_PAPER_STALL_SEC = 7200  # 2h wall-clock ceiling per paper (genuine-hang backstop)

# All 24 (titles fetched verbatim from the arXiv Atom API on 2026-06-09).
_RAW: list[tuple[str, str]] = [
    (
        "2604.01765",
        "DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning",
    ),
    ("2603.16666", "Fast-WAM: Do World Action Models Need Test-time Future Imagination?"),
    ("2601.18692", "A Pragmatic VLA Foundation Model"),
    (
        "2503.19755",
        "ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation",
    ),
    ("2411.15139", "DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving"),
    (
        "2408.14197",
        "Driving in the Occupancy World: Vision-Centric 4D Occupancy Forecasting and Planning via World Models for Autonomous Driving",
    ),
    (
        "2507.00603",
        "World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model",
    ),
    (
        "2311.17918",
        "Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving",
    ),
    ("2506.21539", "WorldVLA: Towards Autoregressive Action World Model"),
    ("2603.28955", "Enhancing Policy Learning with World-Action Model"),
    ("2603.00825", "COMBAT: Conditional World Models for Behavioral Agent Training"),
    ("2511.00062", "World Simulation with Video Foundation Models for Physical AI"),
    ("2501.03575", "Cosmos World Foundation Model Platform for Physical AI"),
    ("2309.17080", "GAIA-1: A Generative World Model for Autonomous Driving"),
    (
        "2405.17398",
        "Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability",
    ),
    ("2402.15391", "Genie: Generative Interactive Environments"),
    ("2408.14837", "Diffusion Models Are Real-Time Game Engines"),
    ("2407.01392", "Diffusion Forcing: Next-token Prediction Meets Full-Sequence Diffusion"),
    ("1803.10122", "World Models"),
    ("2301.04104", "Mastering Diverse Domains through World Models"),
    ("2509.24527", "Training Agents Inside of Scalable World Models"),
    ("2405.12399", "Diffusion for World Modeling: Visual Details Matter in Atari"),
    ("2510.20668", "From Masks to Worlds: A Hitchhiker's Guide to World Models"),
    ("2606.02800", "Cosmos 3: Omnimodal World Models for Physical AI"),
]


def _candidate(arxiv_id: str, title: str) -> dict:
    return {
        "arxiv_id": arxiv_id,
        "doi": None,  # produce.py reads candidate["doi"]; direct-feed must set it
        "oa_pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
        "title": title,
        "year": 2000 + int(arxiv_id[:2]),  # YYMM prefix → publication year
        "github_repo": None,
        "forced": True,
        "discovery_sources": ["forced"],
        "authority_score": 1.0,
    }


PAPERS = [_candidate(aid, title) for aid, title in _RAW]


def _log(m: str) -> None:
    print(f"[run24] {time.strftime('%H:%M:%S')} {m}", file=sys.stderr, flush=True)


def main() -> int:
    cfg = load_audit_config(W)
    seams = build_seams()
    ledger = Ledger(W)
    spoke = make_spoke(
        workspace=W,
        http=build_http(),
        run_cli=build_run_cli(),
        resolve_analysis=seams["resolve_analysis"],
        skeptic_votes=seams["skeptic_votes"],
        rigor_scores=seams["rigor_scores"],
        entailment_judge=seams["entailment_judge"],
        ledger=ledger,
        n_skeptics=cfg.skeptic_votes,
        max_gate_rounds=cfg.max_gate_rounds,
        g2_tolerant=cfg.data_fidelity_tolerant,
        g2_max_unconfirmed=cfg.data_fidelity_max_unconfirmed,
        g2_max_unconfirmed_ratio=cfg.data_fidelity_max_unconfirmed_ratio,
        write_report=seams["write_report"],
    )

    skip = ledger.skip_set()
    queue: list[dict] = []
    for raw in PAPERS:
        cand = dict(raw)
        cand["key"] = _candidate_key(cand)
        if cand["key"] in skip:
            _log(f"SKIP already-done: {cand['key']}")
            continue
        queue.append(cand)

    _log(f"START run24 — {len(queue)}/{len(PAPERS)} to process, max_concurrent={MAX_CONCURRENT}")
    ledger_lock = threading.Lock()
    results: dict[str, dict] = {}
    aborted: list[BaseException] = []

    def process(cand: dict) -> tuple[str, str]:
        key = cand["key"]
        t0 = time.time()
        _log(f"  ▶ START {key}  {cand['title'][:60]}")
        result = _run_spoke_guarded(spoke, cand, stall_seconds=PER_PAPER_STALL_SEC)
        done_ok = bool(
            result.status == "done" and result.person_vault_path and result.ai_package_path
        )
        with ledger_lock:
            if done_ok:
                ledger.record(
                    key,
                    status="done",
                    person_vault_path=result.person_vault_path,
                    ai_package_path=result.ai_package_path,
                )
            else:
                ledger.record(key, status="failed", failure_class=result.failure_class)
                # Only write a quarantine record when the spoke/gate did NOT already
                # write a DETAILED one. A stalled (wall-clock) failure never ran to a
                # gate, so it has no record — write the brief one. Every other failure
                # path (ingest / G2 / anchor / G3) already wrote _failed/{key}.* with
                # specifics; clobbering it with the brief summary would discard the
                # G3 hard-findings needed for diagnosis.
                if result.failure_class == FAILURE_STALLED:
                    _quarantine(W, cand, result)
        results[key] = {
            "title": cand["title"],
            "status": "done" if done_ok else "failed",
            "failure_class": result.failure_class,
            "failure_reason": result.failure_reason,
            "person_vault_path": result.person_vault_path,
            "ai_package_path": result.ai_package_path,
            "elapsed_sec": round(time.time() - t0, 1),
        }
        _log(
            f"  ■ {'DONE ✓' if done_ok else 'FAILED ✗'} {key} "
            f"in {time.time() - t0:.0f}s"
            + ("" if done_ok else f"  [{result.failure_class}] {result.failure_reason}")
        )
        return key, results[key]["status"]

    t_start = time.time()
    with ledger.acquire():
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as ex:
            futs = {ex.submit(process, c): c for c in queue}
            for fut in as_completed(futs):
                try:
                    fut.result()
                except EngineAbort as exc:
                    # Total LLM-transport outage (primary AND claude-code fallback
                    # failed). Stop dispatching new papers; let in-flight finish.
                    aborted.append(exc)
                    _log(f"!! EngineAbort — aborting run: {exc}")
                    for f in futs:
                        f.cancel()
                    break

    done_n = sum(1 for r in results.values() if r["status"] == "done")
    failed_n = sum(1 for r in results.values() if r["status"] == "failed")
    summary = {
        "topic": TOPIC,
        "max_concurrent": MAX_CONCURRENT,
        "total_in_list": len(PAPERS),
        "queued": len(queue),
        "skipped_already_done": len(PAPERS) - len(queue),
        "done": done_n,
        "failed": failed_n,
        "aborted": bool(aborted),
        "elapsed_sec": round(time.time() - t_start, 1),
        "results": results,
    }
    (OUT / "run24_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    _log(
        f"ALL DONE in {summary['elapsed_sec']}s — done={done_n} failed={failed_n} "
        f"aborted={bool(aborted)}"
    )
    return 1 if aborted else 0


if __name__ == "__main__":
    raise SystemExit(main())
