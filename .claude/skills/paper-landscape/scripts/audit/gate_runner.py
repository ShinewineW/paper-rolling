"""Bounded gate runner (中枢-D2): max-N rounds, then quarantine + flag.

Wraps a gate callable in a bounded retry loop so a permanently-failing paper
never spins forever (the engine runs unattended via /loop daily). Each round
runs the gate; on a hard block it calls `on_reemit(round_index)` (the HUB
re-emits the offending branch) and retries. After `max_rounds` blocked rounds
it gives up: writes a `_failed/{key}.md` quarantine record (tracked, small, git-
visible per 中枢-D2) and returns an escalated outcome. The HUB then skips this
paper and back-fills the next candidate.

This is the "整篇不可处理 → 跳过 + 写 _failed/ + 候补" path (中枢-D2). Partial
degradation (garbled equations, no OSS code) is NOT routed here — that is
handled in-branch by suppression+flag and the paper still enters the library.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path

from scripts.audit.types import GateOutcome, GateVerdict


def _write_failed_record(
    failed_dir: Path, key: str, paper_meta: Mapping[str, object], verdict: GateVerdict
) -> Path:
    """Write a small human-readable quarantine record for manual hand-off."""
    failed_dir.mkdir(parents=True, exist_ok=True)
    record = failed_dir / f"{key}.md"
    lines = [
        f"# Quarantined: {key}",
        "",
        f"- **arxiv_id**: {paper_meta.get('arxiv_id', 'n/a')}",
        f"- **title**: {paper_meta.get('title', 'n/a')}",
        f"- **source_url**: {paper_meta.get('source_url', 'n/a')}",
        f"- **tier**: {paper_meta.get('tier', 'n/a')}",
        f"- **gate**: {verdict.gate}",
        "- **reason**: hard-block survived the gate round budget",
        "",
        "## Hard findings",
        "",
    ]
    for f in verdict.hard_findings:
        lines.append(f"- [{f.severity.value}] {f.target}: {f.observation}")
    lines.append("")
    record.write_text("\n".join(lines), encoding="utf-8")
    return record


def run_with_budget(
    gate: Callable[[], GateVerdict],
    *,
    max_rounds: int,
    on_reemit: Callable[[int], None],
    failed_dir: Path,
    key: str,
    paper_meta: Mapping[str, object],
) -> GateOutcome:
    """Run `gate` up to `max_rounds` times; quarantine on persistent block."""
    if max_rounds < 1:
        raise ValueError("max_rounds must be >= 1")

    last_verdict: GateVerdict | None = None
    for round_index in range(1, max_rounds + 1):
        verdict = gate()
        last_verdict = verdict
        if not verdict.blocked:
            return GateOutcome(
                passed=True,
                escalated=False,
                rounds_used=round_index,
                final_verdict=verdict,
            )
        # Blocked. Re-emit and retry unless this was the final budgeted round.
        if round_index < max_rounds:
            on_reemit(round_index)

    # Budget exhausted while still blocked → quarantine + flag.
    assert last_verdict is not None  # loop ran at least once (max_rounds >= 1)
    record = _write_failed_record(failed_dir, key, paper_meta, last_verdict)
    return GateOutcome(
        passed=False,
        escalated=True,
        rounds_used=max_rounds,
        failed_path=str(record),
        final_verdict=last_verdict,
    )
