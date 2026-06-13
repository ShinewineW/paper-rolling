---
key: '2604.01765'
title: DriveDreamerPolicyAGeometryGroundedWorld
authors: []
year: 2026
venue: null
doi: arXiv:2604.01765
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- DriveDreamer-Policy
- geometry-aware world representation
- fixed-size query bottleneck
- causal 3D→2D→1D conditioning pathway
- Depth Generator
- Video Generator
- Action Generator
- Flow Matching
claims_summary:
- DriveDreamer-Policy 在 Navsim v1 和 Navsim v2 的闭环规划评测中，相比论文列出的现有方法取得更强的总体规划表现。
- DriveDreamer-Policy 在 Navsim 世界生成评测中，同时呈现更好的视频生成质量和深度预测质量。
- 加入世界学习相较 action-only 训练能够改善规划表现，且 depth 与 video 联合训练带来的规划收益最大。
headline_metric: EPDMS
headline_value: 88.7
params_million: 2000.0
---

# DriveDreamerPolicyAGeometryGroundedWorld

## Overview
DriveDreamer-Policy 把多视角图像、语言指令和当前动作交给 Qwen3-VL-2B，再通过固定查询接口驱动深度、视频和动作三个生成专家。它的核心动机是让世界-动作模型不只想象外观，还显式生成几何结构，从而让未来视频和规划都能利用空间线索。模型用 depth→video→action 的因果注意力顺序，把几何先验传给视频想象，再传给动作生成。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 9 concepts |
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
