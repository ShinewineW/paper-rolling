# attn_sink/cosmos_trial/reprocess_p1.py
"""In-place re-process of paper #1 (Cosmos-Transfer1) after the analyzer formula fix.

The ARA audit (workflow wjjp676p9) found the analyzer FABRICATED a training-loss
formula not in the paper (conflating inference-time fusion into training). The
analyzer prompt is now hardened (formula fidelity + train/inference separation +
inference labeling). This re-runs resolve_analysis with the fixed prompt and
rebuilds the ARA + human report IN PLACE (same 06-07 key), so paper #1's final
entry is corrected. G2/G3 artifacts (AUDIT_FLAGS.md, level2_report.json) are kept;
stale evidence tables are cleared first. Seal-1 is re-validated.

Run: PYTHONPATH=.claude/skills/paper-landscape uv run python attn_sink/cosmos_trial/reprocess_p1.py
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

from scripts.llm.seams import build_seams
from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch1_llm import write_branch1_llm
from scripts.output.branch2_ara import write_branch2

W = Path(".").resolve()
KEY = "2026-06-07_CosmosTransfer1_2503.14492"
ARA = W / "ai_package" / KEY / "ara"
PERSON = W / "person_vault" / KEY
MD = (
    W
    / "corpus"
    / "2503.14492_CosmosTransfer1ConditionalWorldGeneratio"
    / "2503.14492_CosmosTransfer1ConditionalWorldGeneratio.md"
)
CAND = {
    "arxiv_id": "2503.14492",
    "title": "Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control",
    "github_repo": "https://github.com/nvidia-cosmos/cosmos-transfer1",
    "year": 2025,
}


def _log(m: str) -> None:
    print(f"[reprocess-p1] {time.strftime('%H:%M:%S')} {m}", file=sys.stderr, flush=True)


def main() -> int:
    t0 = time.time()
    seams = build_seams()
    _log("running fixed analyzer (claude -p grounded, chunked)…")
    analysis = seams["resolve_analysis"](MD, CAND)
    _log(f"analysis keys={len(analysis)}; rebuilding ARA in place")
    shutil.rmtree(ARA / "evidence" / "tables", ignore_errors=True)  # clear stale tables
    write_branch2(ARA, CAND, analysis)
    errs = validate_ara_tree(ARA)
    if errs:
        _log(f"SEAL-1 FAILED: {errs[:5]}")
        return 1
    _log("Seal-1 OK; regenerating human report from corrected ARA…")
    write_branch1_llm(PERSON, CAND, ARA, MD, seams["write_report"], key=KEY)
    algo = (ARA / "logic" / "solution" / "algorithm.md").read_text(encoding="utf-8")
    _log(f"done in {time.time() - t0:.0f}s. algorithm.md head: {algo[:200]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
