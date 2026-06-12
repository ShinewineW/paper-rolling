# Code Reference

- **Repository**: https://github.com/NVIDIA/flashdreams
- **Pinned commit**: `caf870e1f03a68d0a15167332c8b62cf2154a4c5`
- **Source**: paper-text (verified)
- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.

## Innovation → code location

| Innovation | Location (`file:line`) |
|---|---|
| 面向闭环 AV 的 action-conditioned autoregressive diffusion world model | README.md:20 |
| 用 streaming KV cache 维持长 rollout 上下文 | docs/source/api/core.rst:26 |
| 轻量 control branch 把 world-scenario map 编成 control tokens | _not found_ |
| 多视角生成中的 view embedding 与 Cross-View Attention | _not found_ |
| 用 Diffusion Forcing 将 bidirectional model 转成 causal autoregressive model | _not found_ |
| Self Forcing 与 DMD 结合的少步长 rollout distillation | _not found_ |
| FlashDreams training-free streaming inference stack | AGENTS.md:1 |
| AlpaSim 中面向 video-diffusion renderer 的 session-based state 与 pre-fetch chunk integration | _not found_ |
| 用 OmniDreams post-training 作为 Diffusion Fixer 修复 reconstruction artifacts | _not found_ |
| 将 OmniDreams-SV backbone fine-tune 成 World-Action Model | _not found_ |
