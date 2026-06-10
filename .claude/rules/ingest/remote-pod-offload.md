---
paths:
  - ".claude/skills/paper-landscape/scripts/ingest/**"
  - ".claude/skills/paper-landscape/scripts/preflight.py"
---

# Offloading heavy ingest (MinerU) to a borrowed remote pod

When local MinerU OOMs on large PDFs (a 16 GB box dies on 30+ MB / image-heavy papers
that a high-RAM pod handles), offload Tier-2 ingest to a borrowed CPU pod.

## Constraints — non-negotiable
- **User-gated, secret-free.** The user must explicitly designate the pod and supply the
  SSH command for that session. Never hardcode or record the host / port / key, and never
  write secrets into any file (keys live in the user's `~/.ssh/config`).
- **Borrowed CPU only.** Keep ALL work under `/tmp/<workdir>` — the venv and the model
  cache included (`MODELSCOPE_CACHE=/tmp/<workdir>/...`). Leave zero residue.

## Flow
1. **Recon** the pod: cores, RAM, python, `uv`, `pandoc`, network reachability (arXiv +
   ModelScope), `/tmp` free space.
2. **Install MinerU into a `/tmp` venv** (`uv venv` + `uv pip install "mineru[core]"`). Add
   `socksio` only if the pod is behind a SOCKS proxy (usually it is not).
3. **Models under `/tmp`**: `mineru-models-download -s modelscope -m pipeline` with
   `MODELSCOPE_CACHE` inside `/tmp` (ModelScope mirror for China networks; HuggingFace where
   reachable). MinerU also writes `~/mineru.json` outside `/tmp` — delete it at cleanup.
4. **Supply PDFs by uploading from local; never let the pod fetch arXiv.** Pod arXiv egress
   can be throttled (observed ~14 KB/s → truncated PDF → MinerU "Data format error"). Download
   locally (fast), `scp` up.
5. **Run raw `mineru -p <pdf> -o <out> -b pipeline` on the pod — never the engine's ingest
   there.** The engine's threadpool + subprocess orchestration deadlocks (futex) inside the
   container; raw MinerU is robust. Use `nohup` + a progress file, since SSH drops lose stdout.
6. **Concurrency is the main footgun (haste makes waste).** Each MinerU process uses torch CPU
   threads ≈ the core count (e.g. 64 on a 128-core box). Running N in parallel (`xargs -P N`)
   over-subscribes when `N × threads ≫ cores` → ~100× slowdown (observed 119–192 s/page at
   `-P 6`, zero completions in 28 min). Choose N so **N × torch_threads ≈ cores** (128C / 64
   threads → `-P 2`: 40 pages in 46 s). A single process is already fast; parallelism only helps
   within the core budget. A CUDA-build torch on a GPU-less pod is a red herring — single-threaded
   CPU is fine; the slowness was purely over-subscription.
7. **Pull results**: `tar` the outputs on the pod (one stream beats per-file `scp` over thousands
   of small image files), `scp` the tar back, extract into a gitignored scratch dir (e.g.
   `attn_sink/`).
8. **Assemble downstream products locally with the engine** — do not run the engine on the pod.

## Cleanup — the borrow rule
`rm -rf /tmp/<workdir>` plus any tool config written outside `/tmp` (e.g. `~/mineru.json`). Verify
zero residue and no leftover processes: MinerU's orchestrated uvicorn server + workers are NOT
matched by `pkill -f mineru` — kill by the venv path instead.
