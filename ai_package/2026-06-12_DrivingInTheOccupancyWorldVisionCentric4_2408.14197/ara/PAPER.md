---
key: '2408.14197'
title: DrivingInTheOccupancyWorldVisionCentric4
authors: []
year: 2024
venue: null
doi: arXiv:2408.14197
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Drive-OccWorld
- 4D occupancy forecasting
- Memory Queue
- Semantic- and Motion-Conditional Normalization
- BEV embeddings
- World Decoder
- Action Conditions
- Unified Conditioning Interface
claims_summary:
- 论文声称Drive-OccWorld在nuScenes、Lyft-Level5和nuScenes-Occupancy上的膨胀GMO、细粒度GMO以及GMO和GSO预测中优于既有方法。
- 论文声称将轨迹、速度、转角或命令等动作条件注入世界模型，可以改善预测并带来可控生成能力。
- 论文声称将4D世界模型与占用代价规划器结合，可以提升开放环轨迹规划的L2误差和碰撞率表现。
headline_metric: mIoUf
headline_value: 37.4
params_million: 0.0
---

# DrivingInTheOccupancyWorldVisionCentric4

## Overview
Drive-OccWorld把视觉中心的占用预测世界模型接到端到端规划上，用历史多视角图像形成BEV记忆，再由世界解码器预测未来occupancy和flow。它引入semantic- and motion-conditional normalization，让历史BEV特征同时携带语义辨别性和运动补偿信息。模型还把velocity、steering angle、trajectory和commands作为动作条件注入解码器，使未来状态生成可控，并让规划器用occupancy-based cost function选择更安全的轨迹。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 12 concepts |
| [experiments.md](logic/experiments.md) | 4 experiments |

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
