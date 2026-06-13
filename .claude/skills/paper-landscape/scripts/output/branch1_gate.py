"""branch1 「评价」 (ADR-0012 rev) — the 理解阅读's opening faithfulness note, NOT a
gate. The report has NO hard门 and NEVER fails. Assembled here:
(b) mechanical number-grounding of the report against the verified ARA (this module),
(c) a config-routed LLM judge's prose note (report ↔ ARA), assembled in build_assessment.
The report MAY carry numbers in natural prose; an UNGROUNDED prose number is surfaced
in the 评价 as a fact for the reader — it does not block publication.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set
from scripts.audit.g3_seal import load_ara_bundle

_FENCE = re.compile(r"^\s*```")
# Strip HTML comments BEFORE number extraction. ADR-0012 rev retired the <!--ref-->
# anchoring, but any stray HTML comment (e.g. a legacy `<!--ref:quote:Table%201...-->`
# in an old report, or an editorial note) would otherwise let extract_numbers parse its
# URL-encoded payload into bogus tokens ('201', '20', '2028.4') — so we always drop them.
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# Markdown ordered-list index ("1. ", "2. ") — the LLM assembler emits numbered
# 核心结论 lines; the index is structure, not a data number.
_OL_PREFIX = re.compile(r"^\s*\d+\.\s")
# Provenance LOCATORS (English Table 1 / §4 / Eq 3 AND Chinese 图1 / 表1 / 第4节 /
# 公式1) — references, not metric values; strip so a faithful report is never blocked
# on a locator digit absent from the source MD (mirrors g2_data_fidelity._LOCATOR).
_LOCATOR = re.compile(
    r"(?i)(?:\b(?:tables?|tab|sections?|sec|figures?|fig|equations?|eq|appendix|app)\.?\s*|§\s*)\d+"
    r"|(?:图|表|公式|附录|第)\s*\d+"
)
# Markdown link targets `](...)` — strip the URL/path payload so vault-key paths
# like `../../ai_package/2026-06-05.../ara/evidence/` and arXiv IDs in hrefs are
# not parsed as ungrounded data numbers (they are infrastructure references, not
# scientific claims).
_MD_LINK_TARGET = re.compile(r"\]\([^)]*\)")
# Inline code spans `...` — the assembler/writer wraps vault-key paths, file
# names, and code refs in backticks (e.g. `ai_package/2026-06-12_..._2503.19755/`);
# those are infrastructure references, not prose data. Strip them like fenced code
# and link targets (ADR-0012 demo, ORION: a backticked vault path leaked 2026/2503).
_INLINE_CODE = re.compile(r"`[^`]*`")
# Bibliographic IDENTIFIERS — an arXiv id (`2503.19755`, YYMM.NNNNN) or a DOI
# (`10.1234/...`). These are paper-identity metadata, never scientific data, so a
# report that names the paper's own arXiv id in prose must not be number-grounded
# on it (ADR-0012 demo, ORION: the writer echoed `arXiv:2503.19755` → a bogus
# ungrounded "number"). A real metric with 4 integer + 4–5 decimal digits does not
# occur, so this shape is unambiguous.
_IDENTIFIER = re.compile(r"(?<!\d)\d{4}\.\d{4,5}(?!\d)|10\.\d{4,9}/\S+")


def prose_numbers(report_text: str) -> list[str]:
    """Distinct DATA numbers in report PROSE. Stripped/skipped before extraction:
    HTML-comment anchor payloads, fenced code blocks, markdown table rows (the
    paper's own figures, gated by 数字门 on the ARA), ordered-list indices,
    inline `code` spans, markdown link targets (vault-key paths / hrefs),
    bibliographic identifiers (arXiv id / DOI), and provenance locators
    (Table 1 / 图1 / §4). The SINGLE
    scope used by both the grounding check and its ratio denominator, so they can
    never diverge."""
    nums: list[str] = []
    in_fence = False
    for raw in report_text.splitlines():
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or raw.lstrip().startswith("|"):
            continue
        line = _OL_PREFIX.sub("", _COMMENT.sub("", raw))  # drop anchors + list index
        line = _INLINE_CODE.sub(" ", line)  # drop inline `code` (vault paths, file/code refs)
        line = _MD_LINK_TARGET.sub(" ", line)  # drop link targets (vault-key paths, hrefs)
        line = _IDENTIFIER.sub(" ", line)  # drop arXiv id / DOI (paper-identity metadata)
        line = _LOCATOR.sub(" ", line)  # drop Table 1 / 图1 / §4
        for n in extract_numbers(line):
            if n not in nums:
                nums.append(n)
    return nums


def ara_value_set(ara_dir: Path) -> set[float]:
    """The distinct numeric VALUES present in the verified ARA bundle (claims +
    evidence tables + logic). The branch1 「評価」 grounds report prose numbers
    against THIS — the ARA is the writer's only source and the verified SoT, so a
    report number absent here is what we surface (ADR-0012 rev)."""
    bundle = load_ara_bundle(ara_dir)
    return source_value_set("\n".join(bundle.values()))


def ungrounded_report_numbers(report_text: str, ara_dir: Path) -> list[str]:
    """Report prose numbers whose VALUE is NOT present in the verified ARA.
    Order-preserving, deterministic — produces FACTS for the 「評価」, never blocks."""
    vals = ara_value_set(ara_dir)
    return [n for n in prose_numbers(report_text) if not number_present(n, vals)]


def _read_audit_flags(ara_dir: Path) -> str:
    """The ARA's own AUDIT_FLAGS.md (numbers 数字门 flagged-but-kept in tolerant mode),
    surfaced in the 评价 so the reader sees the verified pack's own caveats too."""
    f = ara_dir / "AUDIT_FLAGS.md"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


_ATX_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")


def _demote_headings(text: str) -> str:
    """Turn any markdown ATX heading line into plain **bold** text, so a free-form
    judge note can never inject a rogue H1/H2 that breaks the report's one-H1 hierarchy."""
    out = []
    for ln in text.splitlines():
        m = _ATX_HEADING.match(ln)
        out.append(f"**{m.group(1)}**" if m and m.group(1) else (ln if not m else ""))
    return "\n".join(out)


def build_assessment(report_text: str, ara_dir: Path, *, judge=None) -> str:
    """branch1 opening 「评价」 (ADR-0012 rev) — NEVER raises, NEVER blocks.
    Deterministic facts ((b) report numbers not in the ARA + 数字门 AUDIT_FLAGS) plus
    the judge's semantic note, assembled into a `## 评价` block prepended to the report.
    `judge` is the (c) prose seam (None => facts-only). Every ARA-touching step is
    guarded: a corrupt/unreadable ARA degrades the note, it can never fail the report."""
    try:
        bundle = load_ara_bundle(ara_dir)
        # A MISSING/empty ARA bundle is NOT a clean "all grounded" — load_ara_bundle
        # returns {} (no exception) for an absent/empty ARA, so we must treat that as
        # "未核对" too, never a false all-clear (Codex Final-gate HIGH).
        checked = bool(bundle)
        if checked:
            vals = source_value_set("\n".join(bundle.values()))
            ungrounded = [n for n in prose_numbers(report_text) if not number_present(n, vals)]
        else:
            ungrounded = []
    except Exception:  # noqa: BLE001 — 评价 never blocks; an unreadable ARA degrades to 未核对
        ungrounded, checked = [], False
    note = ""
    if judge is not None:
        try:
            out = judge(report_text, ara_dir, ungrounded=ungrounded)
            # The judge note is PROSE under `## 评价`; a free-form LLM may emit its own
            # ATX heading (e.g. `# 忠实性评价`), which would inject a second H1 and break
            # the report's one-H1 hierarchy. Demote any heading line to plain bold text.
            note = _demote_headings(str(out)).strip() if out else ""
        except Exception:  # noqa: BLE001 — 评价 never blocks; a judge failure just drops the note
            note = ""
    lines = ["## 评价", ""]
    if note:
        lines += [note, ""]
    if not checked:
        # ARA unreadable — must NOT claim all-grounded (false reassurance). Say so.
        lines.append("> 机器核对:未能读取已验证知识包(ARA),本次未核对正文数字。")
    elif ungrounded:
        lines.append(
            "> 机器核对:以下正文数字未在已验证知识包(ARA)中找到,读者请留意——"
            + "、".join(ungrounded)
            + "。"
        )
    else:
        lines.append("> 机器核对:正文数字均可在已验证知识包(ARA)中对应。")
    try:
        flags = _read_audit_flags(ara_dir)
    except Exception:  # noqa: BLE001 — 评价 never blocks
        flags = ""
    if flags:
        # Carry the 数字门's own flag body inline (quoted) so the reader sees the
        # flagged items here, not just a pointer to a sibling file.
        quoted = "\n".join("> " + ln for ln in flags.splitlines())
        lines += ["", "> 知识包自身的数字门存疑项(摘自 AUDIT_FLAGS.md):", ">", quoted]
    return "\n".join(lines) + "\n"


def _prepend_assessment(report: str, assessment: str) -> str:
    """Insert the `## 评价` block right after the `# 标题` (+ 导读 blockquote, if any),
    before the first content section. Shared by both branch1 paths."""
    lines = report.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):  # skip to H1
        i += 1
    i += 1
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith(">")):
        i += 1  # skip blank lines + 导读 blockquote
    head, tail = lines[:i], lines[i:]
    return "\n".join(head) + "\n\n" + assessment.rstrip() + "\n\n" + "\n".join(tail) + "\n"
