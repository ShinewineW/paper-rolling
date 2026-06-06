"""Three-layer citation anchor lint — paper-rolling HARD gate (吸收-D1).

NET-NEW paper-rolling module (Round 5/9): our own implementation of the
documented v3.7.3 three-layer-anchor grammar + an empirical-performance-without-
`<!--ref-->` clause. ARS ships only `lint_file(path)->list[str]`, so this is
not a vendored file; it is original code covered by this repo's CC-BY-NC license.

Contract (per branch1 report):
  * Every `<!--ref:slug-->` MUST be immediately followed by a well-formed
    `<!--anchor:<kind>:<value>-->`, kind in {quote, page, section,
    paragraph, none}.
  * `quote` value: URL-encoded, <=25 words by whitespace split, no raw `--`
    (premature HTML-comment terminator).
  * Non-`none` kinds require a non-empty decoded value.
  * Orphan anchors (anchor without a preceding ref) are violations.

paper-rolling ADDITION over the base anchor-grammar lint (吸收-D1, per the
documented v3.7.3 grammar; ARS
`uncited_assertion_detector.py`): an empirical PERFORMANCE assertion — a line
carrying a number adjacent to a metric/comparison cue (NDS/mAP/accuracy/提升/
outperform/...), or a `%`/`个百分点`, or an English empirical verb — with NO
`<!--ref-->` marker hard-blocks. Illustrative numbers without a performance cue
(toy examples, k-steps, list numbering, math constants) do NOT require an
anchor, so the report can pass its own gate.

Detection is line-based and strips HTML-comment markers before the number
scan, so decimals (`0.61`) and `-->` terminators never shred a sentence or
hide its `<!--ref-->` marker.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import unquote

VALID_KINDS = {"quote", "page", "section", "paragraph", "none"}
QUOTE_WORD_CAP = 25

# A ref marker optionally carrying 0-2 status suffix tokens, optionally
# followed by an anchor (the documented v3.7.3 ref/anchor grammar).
_REF_ANCHOR = re.compile(
    r"<!--ref:[A-Za-z][A-Za-z0-9_:-]*"
    r"(?:\s+[\w-]+(?:\+[\w-]+)*){0,2}"
    r"\s*-->"
    r"(\s*<!--anchor:([^:>]*):([^>]*?)-->)?"
)
_BROAD_REF = re.compile(r"<!--ref:([^>]*?)-->")
_ANCHOR = re.compile(r"<!--anchor:([^:>]*):([^>]*?)-->")
_REF_TAIL = re.compile(r"<!--ref:[A-Za-z][A-Za-z0-9_:-]*(?:\s+[\w-]+(?:\+[\w-]+)*){0,2}\s*-->\s*$")
_REF_MARKER = re.compile(r"<!--ref:")
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

# Empirical performance detection (grounded in ARS uncited_assertion_detector):
# a number alongside a metric/comparison cue, or a percent, or an empirical verb.
_PERCENT = re.compile(r"\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*个百分点")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
_METRIC_CUE = re.compile(
    r"\b(NDS|mAP|AP|IoU|mIoU|BLEU|F1|AUC|ROUGE|PSNR|SSIM|FID|accuracy|acc|recall|"
    r"precision|score|top-?\d|准确率|精度|召回|提升|超过|高于|达到|outperform\w*|"
    r"improv\w*|reduc\w*|gain|百分点)\b",
    re.IGNORECASE,
)
_EMPIRICAL_VERBS = {
    "showed",
    "demonstrated",
    "observed",
    "proved",
    "confirmed",
    "achieved",
    "outperformed",
    "improved",
    "reduced",
}
_DEFINITION_PHRASES = (
    "refers to",
    "is defined as",
    "we define",
    "for the purposes of",
    "定义为",
    "记为",
    "是指",
)


@dataclass(frozen=True)
class AnchorViolation:
    """One lint failure with 1-based line number and human message."""

    line: int
    message: str


def _strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks, preserving newline count for line nos."""

    def _blank(m: re.Match[str]) -> str:
        return "\n" * m.group(0).count("\n")

    return _FENCE.sub(_blank, text)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _is_empirical_assertion(prose: str) -> bool:
    """True if `prose` is an unanchored-worthy performance assertion.

    `prose` is a single line with HTML comments already stripped.
    """
    lowered = prose.lower()
    if any(p in lowered for p in _DEFINITION_PHRASES):
        return False
    if _PERCENT.search(prose):
        return True
    # A number AND a performance/metric cue on the same line.
    if _NUMBER.search(prose) and _METRIC_CUE.search(prose):
        return True
    return any(w in _EMPIRICAL_VERBS for w in re.findall(r"[A-Za-z][A-Za-z-]*", lowered))


def lint_text(text: str) -> list[AnchorViolation]:
    """Return all anchor-contract violations; empty list = PASS."""
    scan = _strip_code_fences(text)
    violations: list[AnchorViolation] = []

    # 1. Every ref must carry a well-formed anchor; validate anchor payloads.
    strict_ranges: list[tuple[int, int]] = []
    for m in _REF_ANCHOR.finditer(scan):
        ref_open = m.start()
        ref_close = scan.find("-->", ref_open) + 3
        strict_ranges.append((ref_open, ref_close))
        line = _line_of(scan, m.start())
        if m.group(1) is None:
            violations.append(
                AnchorViolation(line, f"ref marker without trailing anchor: {m.group(0)!r}")
            )
            continue
        kind, value = m.group(2), m.group(3)
        if kind not in VALID_KINDS:
            violations.append(AnchorViolation(line, f"invalid anchor kind {kind!r}"))
            continue
        if kind != "none" and unquote(value).strip() == "":
            violations.append(AnchorViolation(line, f"empty anchor value for kind {kind!r}"))
            continue
        if kind == "quote":
            if "--" in value:
                violations.append(
                    AnchorViolation(line, "quote anchor contains raw `--` in URL-encoded value")
                )
            if len(unquote(value).split()) > QUOTE_WORD_CAP:
                violations.append(AnchorViolation(line, "quote anchor exceeds 25 words"))

    # 2. Malformed ref markers not covered by the strict pattern.
    for m in _BROAD_REF.finditer(scan):
        if not any(s <= m.start() < e for (s, e) in strict_ranges):
            violations.append(
                AnchorViolation(_line_of(scan, m.start()), f"malformed ref marker: {m.group(0)!r}")
            )

    # 3. Orphan anchors (no preceding well-formed ref).
    for m in _ANCHOR.finditer(scan):
        if not _REF_TAIL.search(scan[: m.start()]):
            violations.append(
                AnchorViolation(_line_of(scan, m.start()), f"orphan anchor marker: {m.group(0)!r}")
            )

    # 4. paper-rolling addition — unanchored empirical PERFORMANCE assertions
    #    hard-block. Line-based: a line carrying a <!--ref--> is anchored;
    #    otherwise strip comment markers and test the prose for a performance
    #    assertion (so encoded decimals / `-->` cannot shred or hide a ref).
    for lineno, raw_line in enumerate(scan.splitlines(), 1):
        if _REF_MARKER.search(raw_line):
            continue
        prose = _COMMENT.sub("", raw_line)
        if _is_empirical_assertion(prose):
            violations.append(
                AnchorViolation(
                    lineno,
                    f"unanchored empirical assertion (no <!--ref--> marker): {prose.strip()[:60]!r}",  # noqa: E501
                )
            )

    return violations


def _main() -> int:
    """CLI: lint markdown files for the three-layer citation contract.

    Exit 0 = all conform; 1 = violations; 2 = invocation error.
    """
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="paper-rolling three-layer citation lint (HARD gate)"
    )
    parser.add_argument("paths", nargs="+", type=Path, help="markdown files to lint")
    args = parser.parse_args()

    total: list[str] = []
    for p in args.paths:
        if not p.exists():
            print(f"{p}: file does not exist", file=sys.stderr)
            return 2
        for v in lint_text(p.read_text(encoding="utf-8")):
            total.append(f"{p}:{v.line}: {v.message}")

    if total:
        print("\n".join(total), file=sys.stderr)
        print(
            f"\n[paper-rolling three-layer-citation lint] FAILED ({len(total)} violation(s))",
            file=sys.stderr,
        )
        return 1
    print(f"[paper-rolling three-layer-citation lint] PASSED ({len(args.paths)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
