# attn_sink/cosmos_trial/task3_run.py
"""Task 3 overnight run: 4 remaining Cosmos papers + 5 world-action-model papers.

Through the hardened pipeline (fabrication-proof analyzer, fixed JSON repair,
O#/G# IDs, .git-safe code-ref, LLM human chain with figures/theme/math).

Tick A — re-process the 4 previously-FAILED Cosmos papers. Corpus is already
  ingested and they're known, so we feed them DIRECTLY (no discovery network) —
  discovery was observed to retry-loop/stall on transient 429/503, and that stall
  is OUTSIDE the per-paper watchdog. Direct feed = guaranteed.
Tick B — NEW landscape on "world action model": real discovery + ingest, but the
  discover() call is HARD-TIME-BOUNDED (a thread join) so a stalled source can
  never block the whole night; on timeout it proceeds with nothing rather than hang.

Per-paper failures are isolated by the hub (中枢-D2). Summaries -> task3_*.json.

Run: PYTHONPATH=.claude/skills/paper-landscape uv run python attn_sink/cosmos_trial/task3_run.py
"""

from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

from scripts.adapters import build_discover, build_http, build_run_cli
from scripts.audit_config import load_audit_config
from scripts.hub import Watchdog, run_tick
from scripts.ledger.store import Ledger
from scripts.llm.seams import build_seams
from scripts.spoke import make_spoke

WORKSPACE = Path(".").resolve()
OUT = Path(__file__).parent

COSMOS_TOPIC = "NVIDIA Cosmos world foundation models for physical AI"
WAM_TOPIC = "world action model for embodied agents and robot manipulation"

COSMOS_4 = [
    {
        "arxiv_id": "2501.03575",
        "doi": None,
        "oa_pdf_url": "https://arxiv.org/pdf/2501.03575",
        "title": "Cosmos World Foundation Model Platform for Physical AI",
        "year": 2025,
        "github_repo": None,
        "forced": True,
        "discovery_sources": ["forced"],
        "authority_score": 1.0,
    },
    {
        "arxiv_id": "2503.15558",
        "doi": None,
        "oa_pdf_url": "https://arxiv.org/pdf/2503.15558",
        "title": "Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning",
        "year": 2025,
        "github_repo": None,
        "forced": True,
        "discovery_sources": ["forced"],
        "authority_score": 1.0,
    },
    {
        "arxiv_id": "2511.00062",
        "doi": None,
        "oa_pdf_url": "https://arxiv.org/pdf/2511.00062",
        "title": "World Simulation with Video Foundation Models",
        "year": 2025,
        "github_repo": None,
        "forced": True,
        "discovery_sources": ["forced"],
        "authority_score": 1.0,
    },
    {
        "arxiv_id": "2606.02800",
        "doi": None,
        "oa_pdf_url": "https://arxiv.org/pdf/2606.02800",
        "title": "Cosmos-3: Omnimodal World Models for Physical AI",
        "year": 2026,
        "github_repo": None,
        "forced": True,
        "discovery_sources": ["forced"],
        "authority_score": 1.0,
    },
]


def _log(m: str) -> None:
    print(f"[task3] {time.strftime('%H:%M:%S')} {m}", file=sys.stderr, flush=True)


def _bounded(inner, seconds: float):
    """Wrap a discover() so it can never block the run beyond `seconds`."""

    def discover(topic: str, n: int):
        box: dict = {}
        t = threading.Thread(target=lambda: box.__setitem__("r", inner(topic, n)), daemon=True)
        t.start()
        t.join(seconds)
        if "r" not in box:
            _log(f"discovery exceeded {seconds:.0f}s budget — proceeding with none")
            return []
        return box["r"]

    return discover


def _tick(ledger, spoke, *, topic, n, discover, label):
    t0 = time.time()
    try:
        hub = run_tick(
            workspace=WORKSPACE,
            topic=topic,
            n_target=n,
            ledger=ledger,
            discover=discover,
            spoke=spoke,
            watchdog=Watchdog(stall_seconds=5400, max_refires=2),
            # SEQUENTIAL papers: 4 papers x 5 analyzer chunks = ~20 concurrent
            # `claude -p` saturated the API and stalled. One paper at a time keeps
            # it to 5 concurrent chunks (the config that worked for paper #1).
            max_concurrent=1,
        )
        s = {
            "label": label,
            "topic": topic,
            "elapsed_sec": round(time.time() - t0, 1),
            "done": hub.done_count,
            "failed": hub.failed_count,
            "exhausted": hub.exhausted,
        }
    except Exception as exc:  # noqa: BLE001 — one tick's crash must not kill the other
        s = {"label": label, "topic": topic, "error": f"{type(exc).__name__}: {exc}"}
    _log(f"{label} DONE: {s}")
    (OUT / f"task3_{label}.json").write_text(json.dumps(s, indent=2, default=str), encoding="utf-8")
    return s


def main() -> int:
    cfg = load_audit_config(WORKSPACE)
    seams = build_seams()
    ledger = Ledger(WORKSPACE)
    spoke = make_spoke(
        workspace=WORKSPACE,
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
    _log("START task3")
    results = []
    with ledger.acquire():
        # Tick A: feed the 4 forced Cosmos directly — no discovery network.
        results.append(
            _tick(
                ledger,
                spoke,
                topic=COSMOS_TOPIC,
                n=4,
                label="A_cosmos4",
                discover=lambda _t, _n: [dict(c) for c in COSMOS_4],
            )
        )
        # Tick B: real discovery, hard-bounded to 8 min so a stalled source can't hang.
        wam_discover = _bounded(build_discover(llm=seams["expand_llm"], is_ad_domain=True), 480.0)
        results.append(
            _tick(
                ledger,
                spoke,
                topic=WAM_TOPIC,
                n=5,
                label="B_world_action_model",
                discover=wam_discover,
            )
        )
    (OUT / "task3_summary.json").write_text(
        json.dumps(results, indent=2, default=str), encoding="utf-8"
    )
    _log(f"ALL DONE: {results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
