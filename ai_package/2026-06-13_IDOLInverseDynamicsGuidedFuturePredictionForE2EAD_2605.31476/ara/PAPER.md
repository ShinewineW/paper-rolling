---
key: '2605.31476'
title: IDOLInverseDynamicsGuidedFuturePredictionForE2EAD
authors: []
year: null
venue: null
doi: arXiv:2605.31476
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- IDOL
- inverse dynamics model
- latent BEV world model
- trajectory anchors
- anchor-conditioned ego query
- candidate-conditioned BEV features
- IDM spatial dynamics map
- IDM global dynamics feature
claims_summary:
- IDOL 的核心主张是：仅预测未来潜在 BEV 状态不足以稳定改善规划，显式解码相邻未来状态之间的转移可以生成面向轨迹优化的运动线索。
- IDOL 使用轻量闭环细化，将更新后的规划查询重新送入未来推理；论文认为这能改善长时域一致性，但过多迭代可能带来过度修正。
- 论文主张，相邻两帧 BEV 转移比更长未来窗口更适合即时规划细化，因为长窗口可能稀释局部转移线索。
headline_metric: EPDMS
headline_value: 38.0
params_million: 69.36
---

# IDOLInverseDynamicsGuidedFuturePredictionForE2EAD

## Overview
IDOL 是面向 end-to-end autonomous driving 的 latent BEV world-model planner，核心做法是在预测多个未来 latent BEV 状态后，用 inverse dynamics 解码相邻未来状态之间的 transition-aware motion cues。它把 future prediction 从被动场景预想变成可用于 trajectory refinement 的规划信号，再用轻量 closed-loop refinement 将更新后的 query 重新送回未来推理。这样做的动机是补上 world modeling 与 executable motion generation 之间原本较弱的连接。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 12 concepts |
| [experiments.md](logic/experiments.md) | 6 experiments |

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
