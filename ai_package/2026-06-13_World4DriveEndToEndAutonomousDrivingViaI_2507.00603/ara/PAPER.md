---
key: '2507.00603'
title: World4DriveEndToEndAutonomousDrivingViaI
authors: []
year: 2025
venue: null
doi: arXiv:2507.00603
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- World4Drive
- Driving World Encoding
- Intention Encoder
- Physical World Latent Encoding
- Semantic Understanding
- 3D Spatial Encoding
- Temporal Aggregation
- Intention-aware World Model
claims_summary:
- World4Drive 在 nuScenes 开放环基准上，在无需人工感知标注的设定中优于感知标注-free 强基线，并在碰撞率指标上表现突出。
- World4Drive 在 NavSim 闭环基准上相较 LAW (Perception-free) 提升 PDMS，并在若干空间安全相关指标上更好，但仍低于
  DiffusionDrive。
- 组件消融表明，引入车辆意图、深度空间先验、语义先验以及保留世界模型评估机制，会影响规划误差和碰撞表现；仅保留意图而缺少世界模型会导致规划表现退化。
headline_metric: L2 (m)↓ Avg.
headline_value: 0.5
params_million: 0.0
---

# World4DriveEndToEndAutonomousDrivingViaI

## Overview
World4Drive 是一个面向端到端自动驾驶的 intention-aware physical latent world model，用 RGB 图像和 trajectory vocabulary 同时构建驾驶意图与物理世界 latent 表示。它用 Metric3D v2 和 Grounded-SAM 提供空间与语义先验，再在 latent 空间中预测不同意图下的未来状态。World Model Selector 通过比较预测 latent 与真实未来 latent 的距离来选择训练目标，并在推理时按 ScoreNet 分数选择轨迹。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 10 concepts |
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
