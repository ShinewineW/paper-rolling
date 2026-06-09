---
key: '2311.17918'
title: 'Driving into the Future: Multiview Visual Forecasting and Planning with World
  Model for Autonomous Driving'
authors: []
year: 2023
venue: null
doi: arXiv:2311.17918
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 驾驶世界模型(Driving World Model)
- 多视角联合时序建模(Joint Multiview Temporal Modeling)
- 视图分解生成(Factorized Multiview Generation)
- 统一条件接口(Unified Condition Interface)
- 基于图像的奖励函数(Image-based Reward Function)
- 树形规划展开(Tree-based Rollout)
- 关键点匹配一致性评分(KPM, Key Points Matching Score)
claims_summary:
- Drive-WM 是首个兼容现有端到端规划模型的驾驶世界模型，通过联合时空建模与视图分解，在自动驾驶场景下生成高质量、多视角一致且可控的多视角视频
- 将联合多视角建模分解为参考视角生成与条件化拼接视角生成两阶段，可使 KPM 多视角一致性指标大幅提升，同时维持视频质量
- 将初始帧图像、文本描述、自车动作、3D 框与 BEV 地图统一投影至 d 维特征空间后拼接，单一接口即可灵活驱动多种异构条件下的可控生成，无需为每类条件设计专用模块
headline_metric: FVD
headline_value: 122.7
params_million: 0.0
---

# Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving

## Overview
Drive-WM 是首个兼容现有端到端规划模型的自动驾驶多视角世界模型。通过联合时空建模与视角分解（view factorization），模型可生成高保真、空间一致的多视角驾驶视频。统一条件接口支持文本、图像、3D 布局、自车动作等异构条件的灵活组合输入。论文首次探索将世界模型用于端到端安全规划，通过基于图像奖励的树状规划选出最优轨迹。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
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
