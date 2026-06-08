# attn_sink/cosmos_trial/run_human_v2.py
"""Regenerate the Cosmos-Transfer1 human report via the ENGINE path (with figures).

Calls write_branch1_llm with the real write_report seam (routed per config/llm.yaml
-> deepseek), which now returns sections + the original-figure inventory + 中文
narration. The report embeds every original figure (guided tour) + the gated tables
+ anchored conclusions, hard-gated by the anchor lint + figure-completeness.

Run: PYTHONPATH=.claude/skills/paper-landscape uv run python attn_sink/cosmos_trial/run_human_v2.py
"""

from __future__ import annotations

import time
from pathlib import Path

from scripts.llm.seams import build_seams
from scripts.output.branch1_llm import write_branch1_llm

W = Path(".").resolve()
KEY = "2026-06-07_CosmosTransfer1_2503.14492"
ARA = W / "ai_package" / KEY / "ara"
MD = (
    W
    / "corpus"
    / "2503.14492_CosmosTransfer1ConditionalWorldGeneratio"
    / ("2503.14492_CosmosTransfer1ConditionalWorldGeneratio.md")
)
PERSON = W / "person_vault" / KEY
TITLE = "Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control"


def main() -> int:
    t0 = time.time()
    write_branch1_llm(PERSON, {"title": TITLE}, ARA, MD, build_seams()["write_report"], key=KEY)
    rep = (PERSON / "report.md").read_text(encoding="utf-8")
    import re

    cn = len([c for c in re.sub(r"<!--.*?-->", "", rep) if "一" <= c <= "鿿"])
    imgs = len(re.findall(r"!\[\]\(images/", rep))
    print(f"wrote {PERSON}/report.md in {time.time() - t0:.0f}s")
    print(f"  中文字符={cn}  inlined original figures={imgs}  bytes={len(rep)}")
    print(
        f"  images copied: {len(list((PERSON / 'images').glob('*'))) if (PERSON / 'images').exists() else 0}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
