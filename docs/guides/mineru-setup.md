# MinerU setup (Tier-2 ingest) — environment fix

> **创建日期**: 2026-06-10
> **更新日期**: 2026-06-10
> **适用环境**: `~/Coding/paper-rolling/` 仓库;Tier-2 ingest(PDF→MD)依赖本机 mineru;以下命令可直接复制粘贴。
> 所有命令可直接复制粘贴。

---

`mineru` (Tier-2 ingest: PDF → Markdown + images + content_list) is **installed but
not functional by default** in a China-network / Clash-proxy environment. Two
environment problems make `mineru -p` crash with `rc=1` even though `mineru
--version` works — so `scripts.preflight` (presence check) used to pass while real
ingest died. The preflight **deep smoke** now catches this, but here is the actual
fix.

## Symptom

```
mineru_failed: rc=1            # what the engine reports at Tier-2
```
Running `mineru -p <pdf> -o out -b pipeline` directly shows the real cause (one of):

1. `ImportError: Using SOCKS proxy, but the 'socksio' package is not installed.`
2. Model download stalls/fails ("Fetching N files" then a worker dies) — HuggingFace
   is unreachable/slow behind the proxy.

## Fix

### 1. Add `socksio` to mineru's environment

mineru (installed via `uv tool`) starts an `httpx` client at launch; under a SOCKS
proxy (`all_proxy=socks5://…`) httpx needs `socksio`, which mineru's isolated env
lacks → it crashes before doing anything.

```bash
uv tool install --with socksio "mineru[core]"
```

### 2. Download models from ModelScope (domestic), direct (not via the proxy)

The pipeline models default to HuggingFace, which is blocked/slow here. Use the
ModelScope mirror, and **bypass the proxy** for the download — ModelScope is a
domestic (`.cn`) source, so routing it through a foreign proxy node is slow/broken.
(If Clash Verge TUN mode is on with a correct DIRECT rule for `.cn`, it also works;
the explicit-proxy env vars are what force the wrong route.)

```bash
# resume-safe: re-running skips already-downloaded files
env -u http_proxy -u https_proxy -u all_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
  mineru-models-download -s modelscope -m pipeline
```

### 3. Run with the right env

```bash
# models cached from step 2; localhost must bypass any SOCKS proxy because mineru's
# orchestrated mode talks to its own local api over http.
MINERU_MODEL_SOURCE=modelscope NO_PROXY=localhost,127.0.0.1,::1 \
  mineru -p paper.pdf -o out -b pipeline
```

`MINERU_MODEL_SOURCE=modelscope` is **deployment config, not engine code** — a
US/HF-reachable host should leave it unset (defaults to HuggingFace). Set it (e.g.
in your shell profile) on China-network hosts. The engine inherits the ambient env
when it invokes mineru.

## Verify

```bash
# full functional smoke against the committed golden (first run ~75s; then cached)
PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.preflight --force-smoke
```
Expect `mineru:smoke: converted OK (eq=1, img=1, text=3, files=2)`.

## Why this is a footgun

`mineru --version` returning 0 says nothing about whether `mineru -p` can convert.
The preflight **deep smoke** (`scripts.preflight`, layer 3) runs mineru on a tiny
bundled fixture and compares products to `preflight_assets/smoke_golden.json`, so a
broken mineru is a loud STOP **before** the engine burns analyzer/G2/writer tokens
to a late failure.
