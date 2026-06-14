#!/usr/bin/env python3
"""Stop-hook reminder (paper-rolling, project-local).

Fires when the main Claude Code agent tries to hand control back. If any paper has
passed the machine gates but has NOT been terminally reviewed (ADR-0013), inject a
one-shot reminder so the missed final-review step surfaces before the turn ends —
instead of being silently skipped on the way out.

It is an ADVISORY nudge, not a hard gate: the `stop_hook_active` guard means it
blocks at most once per stop-chain, so it can never trap the session. Wired from
.claude/settings.json (Stop hook). Project-local by design — it only runs under
Claude Code, so a non-Claude-Code (pure-API) runtime never sees it (consistent
with the preflight `final-review:runtime` WARN). On any internal error it stays
silent and allows the stop — a reminder must never break the user's ability to end.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# this file lives at <root>/.claude/hooks/final_review_reminder.py
ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / ".claude" / "skills" / "paper-landscape"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    # loop guard: if we are already continuing because of a prior Stop-hook block,
    # do not block again — remind at most once per stop-chain.
    if payload.get("stop_hook_active"):
        return 0

    sys.path.insert(0, str(ENGINE))
    try:
        from scripts.output.final_review import unreviewed_compliant_keys

        pending = list(unreviewed_compliant_keys(ROOT))
    except Exception:  # noqa: BLE001 — a reminder must never break stopping
        return 0

    if not pending:
        return 0

    shown = ", ".join(pending[:8]) + (f" …(+{len(pending) - 8})" if len(pending) > 8 else "")
    reason = (
        f"⚠️ 终审收尾未完成:{len(pending)} 篇已过机器门但未终审(ADR-0013)。\n"
        f"待终审:{shown}\n"
        f"如本回合在跑 paper-landscape campaign,请按 "
        f".claude/skills/paper-landscape/sub-skills/final-review/SKILL.md 对这些篇跑终审;"
        f"若与本次工作无关或有意跳过,直接再次结束即可(本提醒每个 stop-chain 只出现一次)。"
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
