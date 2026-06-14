# .claude/skills/paper-landscape/scripts/preflight.py
"""Environment preflight — verify the local machine has EVERY external
prerequisite the engine needs BEFORE a campaign runs, so a broken tool is a loud
STOP, never a silent per-paper skip that burns tokens to a late failure.

Three layers (cheap → expensive):
  1. check_environment()  — presence: python deps + pandoc/mineru on PATH (stdlib-only).
  2. check_llm()          — config: llm.yaml routing valid, api keys set, and a
                            LIVENESS probe of each routed API provider (a trivial
                            prompt → does it reply). Local agents (claude-code /
                            codex) are presence-only — NOT probed (a gratuitous
                            subprocess call = IP-detection / account-ban risk).
  3. deep_smoke()         — FUNCTIONAL: pandoc converts; mineru actually parses a
                            tiny bundled PDF and its products match a committed
                            golden. mineru is CACHED (keyed on version+fixture) —
                            the ~75s model-load cost is paid only on first use /
                            version change; cache hits are instant.

Plus one ADVISORY (non-blocking) check:
  * check_runtime()       — which AI drives the engine (the engine never runs
                            autonomously). On a non-Claude-Code runtime the
                            terminal-review gate (ADR-0013) has no autonomous
                            reviewer, so it WARNs (does not fail) — the operator
                            decides whether to route a reviewer onto their provider.

The TOP-LEVEL imports stay stdlib-only so layer 1 reports even when the runtime
deps (requests/pyyaml) or the LLM stack are themselves missing; layers 2/3
lazy-import the heavier modules inside their functions.

CLI: `python -m scripts.preflight [--no-probe] [--no-deep] [--force-smoke]`
  exit 0 if all present/healthy, exit 1 otherwise (with each fix command).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_ASSET_DIR = Path(__file__).parent / "preflight_assets"
_SMOKE_PDF = _ASSET_DIR / "smoke.pdf"
_SMOKE_GOLDEN = _ASSET_DIR / "smoke_golden.json"


@dataclass(frozen=True)
class Check:
    """One prerequisite's status + the command to fix it if missing.

    `warn=True` is an advisory: it renders as [WARN] and carries `fix` as a note,
    but keeps `ok=True` so it never lowers the exit code — for situations the
    operator must DECIDE on, not a hard prerequisite they must fix."""

    name: str
    ok: bool
    detail: str
    fix: str
    warn: bool = False


def _has_module(mod: str) -> bool:
    """True if `mod` is importable, without importing it."""
    return importlib.util.find_spec(mod) is not None


def check_environment() -> list[Check]:
    """Layer 1 — presence only (stdlib-only; runs even when deps are missing)."""
    checks: list[Check] = []

    for mod, pkg in (("requests", "requests"), ("yaml", "pyyaml")):
        present = _has_module(mod)
        checks.append(
            Check(
                name=f"python:{pkg}",
                ok=present,
                detail="importable" if present else f"missing module {mod!r}",
                fix="uv sync",
            )
        )

    pandoc = shutil.which("pandoc")
    checks.append(
        Check(
            name="pandoc",
            ok=pandoc is not None,
            detail=pandoc or "not on PATH",
            fix="brew install pandoc  (or a GitHub release binary)",
        )
    )

    mineru = shutil.which("mineru")
    checks.append(
        Check(
            name="mineru",
            ok=mineru is not None,
            detail=mineru or "not on PATH",
            fix='uv tool install --with socksio "mineru[core]"',
        )
    )

    return checks


def check_runtime() -> list[Check]:
    """Which AI runtime drives the engine — an ADVISORY check, never blocking.

    The engine NEVER runs autonomously: it is always driven by an AI, and the
    terminal-review gate (ADR-0013) has no engine-side reviewer. On a non-Claude-Code
    runtime (e.g. a pure-API driver) terminal review therefore has no autonomous
    reviewer — report it (WARN) so the operator can route a reviewer onto their own
    provider or skip terminal review deliberately, rather than have it silently absent.
    """
    if os.environ.get("CLAUDECODE", "").strip():
        return [
            Check(
                "final-review:runtime",
                True,
                "Claude Code runtime — terminal review runs via the main-session agent",
                "",
            )
        ]
    return [
        Check(
            "final-review:runtime",
            True,
            "non-Claude-Code runtime (e.g. pure API): terminal-review gate has no "
            "autonomous reviewer — the engine never runs alone",
            "route terminal review onto your own API provider, or skip it deliberately",
            warn=True,
        )
    ]


# --------------------------------------------------------------------------- #
# Layer 2 — LLM config + provider liveness (lazy imports; never prints secrets) #
# --------------------------------------------------------------------------- #


def _provider_live(provider) -> tuple[bool, str]:
    """Trivial-prompt liveness probe. Reports reachable/unreachable + latency ONLY
    — never the api key, never the response body."""
    import time

    try:
        t0 = time.monotonic()
        out = provider.complete("reply with the single word OK", tier="fast", timeout=20)
        dt = time.monotonic() - t0
    except Exception as exc:  # noqa: BLE001 — any failure = not live (it's a probe)
        return (False, f"unreachable: {type(exc).__name__}: {str(exc)[:80]}")
    body = str(out).strip()
    return (bool(body), f"reachable ({dt:.1f}s)" if body else "empty response")


def check_llm(workspace: str | Path = ".", *, probe: bool = True) -> list[Check]:
    """Layer 2 — llm.yaml routing validity + api-key presence + provider liveness.

    `probe=True` calls each ROUTED openai-compatible provider with a trivial prompt
    to confirm the key/endpoint actually work. Local agents (claude-code / codex,
    incl. round_robin pool members) are presence-only (NOT probed): a gratuitous
    subprocess call carries IP-detection / account-ban risk, and the real analyzer
    workload exercises it anyway.
    """
    try:
        from scripts.llm.config import SEAMS, load_llm_config
    except Exception as exc:  # noqa: BLE001 — deps missing → report, don't crash layer 2
        return [Check("llm:config", False, f"cannot import llm config layer: {exc}", "uv sync")]

    try:
        cfg = load_llm_config(Path(workspace))
    except Exception as exc:  # noqa: BLE001 — raises if a seam routes to an undefined provider
        return [
            Check(
                "llm:llm.yaml", False, f"invalid/unroutable routing: {exc}", "fix config/llm.yaml"
            )
        ]

    checks = [
        Check("llm:llm.yaml", True, f"all {len(SEAMS)} seams routed to defined providers", "")
    ]

    distinct: dict = {}
    for seam in SEAMS:
        p = cfg.for_seam(seam)
        distinct.setdefault(p.name, p)

    def _check_leaf(label: str, leaf) -> list[Check]:
        """Checks for ONE non-composite provider: a local agent (presence-only) or
        an HTTP API (key set + optional liveness probe)."""
        base_url = getattr(leaf, "base_url", None)
        if base_url is None:
            # local agent (claude-code / codex): presence-only, NOT probed — a
            # gratuitous subprocess call carries IP/account risk and the real
            # workload exercises it anyway. It names its CLI via `cli`.
            binary = getattr(leaf, "cli", "claude")
            cl = shutil.which(binary)
            return [
                Check(
                    name=f"provider:{label}",
                    ok=cl is not None,
                    detail=(
                        f"{cl} (presence-only; not probed — local-agent IP risk)"
                        if cl
                        else f"{binary} CLI not on PATH"
                    ),
                    fix=f"install the {binary} CLI",
                )
            ]
        # HTTP API: the key must be set, then (when probing) a liveness check.
        key_env = getattr(leaf, "api_key_env", None)
        key_set = bool(os.environ.get(key_env, "").strip()) if key_env else False
        if not key_set:
            return [
                Check(
                    f"provider:{label}",
                    False,
                    f"api key env {key_env} is UNSET",
                    f"set {key_env} in .env",
                )
            ]
        if not probe:
            return [Check(f"provider:{label}", True, f"{key_env} set (liveness skipped)", "")]
        ok, detail = _provider_live(leaf)
        return [
            Check(
                f"provider:{label}",
                ok,
                detail,
                f"verify {base_url} reachability / {key_env} validity",
            )
        ]

    for name, p in distinct.items():
        members = getattr(p, "members", None)
        if members:
            # round_robin pool: recurse into EVERY member so an HTTP member still
            # gets its key/liveness check and an agent member its presence check —
            # the composite itself has no base_url and would otherwise be skipped.
            for m in members:
                checks.extend(_check_leaf(f"{name}:{m.name}", m))
        else:
            checks.extend(_check_leaf(name, p))

    return checks


# --------------------------------------------------------------------------- #
# Layer 3 — functional deep smoke (pandoc instant; mineru cached golden compare) #
# --------------------------------------------------------------------------- #


def _pandoc_smoke() -> Check:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        return Check("pandoc:smoke", False, "not on PATH", "brew install pandoc")
    try:
        r = subprocess.run(  # noqa: S603 — fixed argv
            [pandoc, "-f", "markdown", "-t", "html"],
            input="# hi",
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        ok = r.returncode == 0 and "<h1" in r.stdout
    except (OSError, subprocess.SubprocessError) as exc:
        return Check("pandoc:smoke", False, f"conversion error: {exc}", "reinstall pandoc")
    return Check(
        "pandoc:smoke",
        ok,
        "converts markdown→html" if ok else "ran but output unexpected",
        "reinstall pandoc",
    )


def _mineru_version() -> str | None:
    m = shutil.which("mineru")
    if not m:
        return None
    try:
        r = subprocess.run(
            [m, "--version"], capture_output=True, text=True, timeout=15, check=False
        )  # noqa: S603
    except (OSError, subprocess.SubprocessError):
        return None
    return (r.stdout or r.stderr).strip() or "unknown"


def _smoke_cache_path() -> Path:
    return Path.home() / ".cache" / "paper-rolling" / "mineru_smoke.json"


def _golden_problems(types: dict, n_image_files: int, md_chars: int, expect: dict) -> list[str]:
    """Pure structural comparison of mineru output against the committed golden."""
    problems: list[str] = []
    if types.get("equation", 0) != expect["equation_blocks"]:
        problems.append(f"equation blocks {types.get('equation', 0)}≠{expect['equation_blocks']}")
    if types.get("image", 0) != expect["image_blocks"]:
        problems.append(f"image blocks {types.get('image', 0)}≠{expect['image_blocks']}")
    if types.get("text", 0) < expect["text_blocks_min"]:
        problems.append(f"text blocks {types.get('text', 0)}<{expect['text_blocks_min']}")
    if n_image_files < expect["image_files_min"]:
        problems.append(f"image files {n_image_files}<{expect['image_files_min']}")
    if md_chars < expect["md_chars_min"]:
        problems.append(f"md chars {md_chars}<{expect['md_chars_min']}")
    return problems


def _run_mineru_smoke() -> tuple[bool, str]:
    import tempfile
    from collections import Counter

    expect = json.loads(_SMOKE_GOLDEN.read_text())["expect"]
    env = dict(os.environ)
    # localhost must bypass any SOCKS proxy — orchestrated mineru talks to its own
    # local api over http; routing 127.0.0.1 through the proxy breaks it.
    no_proxy = env.get("NO_PROXY", "")
    for host in ("localhost", "127.0.0.1", "::1"):
        if host not in no_proxy:
            no_proxy = (no_proxy + "," + host).lstrip(",")
    env["NO_PROXY"] = env["no_proxy"] = no_proxy
    with tempfile.TemporaryDirectory() as td:
        try:
            r = subprocess.run(  # noqa: S603 — fixed argv
                ["mineru", "-p", str(_SMOKE_PDF), "-o", td, "-b", "pipeline"],
                capture_output=True,
                text=True,
                timeout=600,
                env=env,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return (False, "mineru timed out (>600s)")
        except OSError as exc:
            return (False, f"mineru spawn failed: {exc}")
        if r.returncode != 0:
            return (False, f"mineru rc={r.returncode}: {r.stderr[-200:].strip()}")
        out = Path(td)
        cls = [p for p in out.rglob("*content_list.json") if "_v2" not in p.name]
        mds = list(out.rglob("*.md"))
        if not cls or not mds:
            return (False, "mineru produced no content_list/.md")
        types = dict(Counter(b.get("type") for b in json.loads(cls[0].read_text())))
        imgdirs = [d for d in out.rglob("images") if d.is_dir()]
        n_imgs = sum(1 for f in imgdirs[0].iterdir() if f.is_file()) if imgdirs else 0
        md_chars = len(mds[0].read_text(encoding="utf-8"))
        problems = _golden_problems(types, n_imgs, md_chars, expect)
        if problems:
            return (False, "golden mismatch: " + "; ".join(problems))
        return (
            True,
            f"converted OK (eq={types.get('equation', 0)}, img={types.get('image', 0)}, "
            f"text={types.get('text', 0)}, files={n_imgs})",
        )


def mineru_smoke(*, force: bool = False) -> Check:
    """Layer 3 (mineru) — run the bundled fixture through mineru and compare products
    to the committed golden. CACHED on (mineru version, fixture sha) so the ~75s
    model-load cost is paid only on first use / version change."""
    name = "mineru:smoke"
    ver = _mineru_version()
    if ver is None:
        return Check(
            name, False, "mineru not on PATH", 'uv tool install --with socksio "mineru[core]"'
        )
    if not _SMOKE_PDF.is_file() or not _SMOKE_GOLDEN.is_file():
        return Check(
            name,
            False,
            "fixture/golden missing under preflight_assets/",
            "restore preflight_assets/",
        )
    fsha = hashlib.sha256(_SMOKE_PDF.read_bytes()).hexdigest()
    cache = _smoke_cache_path()
    if not force and cache.is_file():
        try:
            c = json.loads(cache.read_text())
            if c.get("mineru_version") == ver and c.get("fixture_sha256") == fsha and c.get("ok"):
                return Check(name, True, f"cached OK (mineru {ver})", "")
        except (OSError, ValueError):
            pass
    ok, detail = _run_mineru_smoke()
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(
            json.dumps({"mineru_version": ver, "fixture_sha256": fsha, "ok": ok, "detail": detail})
        )
    except OSError:
        pass
    return Check(name, ok, detail, "socksio installed? MINERU_MODEL_SOURCE set? models downloaded?")


def deep_smoke(*, force: bool = False) -> list[Check]:
    """Layer 3 — functional converter checks (pandoc instant; mineru cached)."""
    return [_pandoc_smoke(), mineru_smoke(force=force)]


# --------------------------------------------------------------------------- #
# Report + CLI                                                                  #
# --------------------------------------------------------------------------- #


def all_ok(checks: list[Check]) -> bool:
    """True iff every check passed."""
    return all(c.ok for c in checks)


def format_report(checks: list[Check]) -> str:
    """Human-readable PASS/FAIL report; names the fix for each failing item."""
    lines = ["paper-landscape preflight (REQUIRED unless marked WARN):"]
    for c in checks:
        mark = "WARN" if c.warn else ("OK  " if c.ok else "FAIL")
        lines.append(f"  [{mark}] {c.name}: {c.detail}")
        if c.fix and (c.warn or not c.ok):
            lines.append(f"         {'note' if c.warn else 'fix'}: {c.fix}")
    if not all_ok(checks):
        lines.append("PROBLEMS ABOVE — fix them, then re-run. DO NOT proceed.")
    elif any(c.warn for c in checks):
        lines.append("ALL HEALTHY (advisories above) — safe to proceed; decide on the WARNs.")
    else:
        lines.append("ALL HEALTHY — safe to proceed.")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    import sys

    argv = sys.argv[1:] if argv is None else argv
    probe = "--no-probe" not in argv
    deep = "--no-deep" not in argv
    force = "--force-smoke" in argv

    checks = check_environment() + check_runtime() + check_llm(probe=probe)
    if deep:
        checks += deep_smoke(force=force)
    print(format_report(checks))
    return 0 if all_ok(checks) else 1


if __name__ == "__main__":
    import sys

    sys.exit(_main())
