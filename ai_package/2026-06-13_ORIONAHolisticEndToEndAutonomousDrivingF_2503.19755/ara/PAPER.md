---
key: '2503.19755'
title: ORIONAHolisticEndToEndAutonomousDrivingF
authors: []
year: 2025
venue: null
doi: arXiv:2503.19755
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- ORION
- vision-reasoning-action space alignment
- QT-Former
- memory bank and history queries
- planning token
- generative planner
- VAE latent alignment
- Chat-B2D
claims_summary:
- ORION在Bench2Drive base set闭环评测中相对既有E2E-AD方法取得更优的Driving Score与Success Rate，并在相同NC条件与相机模态下超过DriveTransformer-Large。
- ORION在Bench2Drive多能力评测的平均能力上领先主要闭环基线，并在Overtaking、Emergency Brake与Traffic Sign能力上表现突出；但在Merging与Give
  Way上落后于DriveAdapter。
- 在ORION框架中，VAE式生成规划器相对Diffusion式生成规划器在闭环、开环和能力均值指标上整体更优。
headline_metric: Driving Score (DS)
headline_value: 77.74
params_million: 7000.0
---

# ORIONAHolisticEndToEndAutonomousDrivingF

## Overview
ORION 是一个面向 E2E autonomous driving 的整体框架，把多视角图像先交给 QT-Former 聚合当前场景与历史上下文，再由 LLM 完成场景理解、动作推理并产生 planning token。它的核心动机是让 VLM 的语义推理不要停在文本空间，而是通过 generative planner 进入可优化的轨迹动作空间。generative planner 以 VAE latent space 对齐 reasoning space 与 action space，从而让推理信息直接条件化多模态轨迹生成。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 8 falsifiable claims |
| [concepts.md](logic/concepts.md) | 9 concepts |
| [experiments.md](logic/experiments.md) | 8 experiments |

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
