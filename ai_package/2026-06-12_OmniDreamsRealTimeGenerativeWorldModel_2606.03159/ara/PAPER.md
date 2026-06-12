---
key: '2606.03159'
title: OmniDreamsRealTimeGenerativeWorldModel
authors: []
year: 2026
venue: null
doi: arXiv:2606.03159
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- OmniDreams
- 闭环仿真
- World-scenario map
- Autoregressive diffusion video generation
- Streaming KV cache
- Lightweight control branch
- Cross-view attention
- Diffusion Forcing
claims_summary:
- OmniDreams 通过自回归视频扩散、流式 KV cache、轻量编解码与多 GPU 并行，在闭环仿真中达到实时交互渲染。
- 从双向模型到因果 Diffusion Forcing 再到 Self Forcing 蒸馏后，OmniDreams-SV 在生成质量、结构条件保真与车道线指标上整体优于未蒸馏因果阶段，同时保留可实时因果生成能力。
- 继续使用长上下文双向教师进行 Self Forcing 能降低长 rollout 的时间漂移与累积伪影，使后段窗口相对短上下文教师更稳定。
headline_metric: Effective FPS
headline_value: 105.0
params_million: 2000.0
---

# OmniDreamsRealTimeGenerativeWorldModel

## Overview
OmniDreams 是从 Cosmos-Predict 2.5 继续训练而来的自动驾驶生成式世界模型，用于在闭环仿真中根据历史画面、当前 simulator state 和 driving actions 生成下一步传感器视频。它把视频扩散模型改造成因果、自回归、可缓存的渲染器，使策略动作可以即时影响后续观测。论文的核心动机是用生成式先验突破 reconstruction-based neural simulators 只能围绕已采集场景外推的限制。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 12 concepts |
| [experiments.md](logic/experiments.md) | 5 experiments |

### Physical Layer (`/src`)
| File | Description |
|------|-------------|
| [execution/core.py](src/execution/core.py) | Novel-contribution stub |
| [code_ref.md](src/code_ref.md) | Repo + pinned SHA + file:line map |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of tables + figures |
