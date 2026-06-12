---
key: '2511.00062'
title: WorldSimulationWithVideoFoundationModels
authors: []
year: 2025
venue: null
doi: arXiv:2511.00062
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Physical AI
- world simulator
- Cosmos-Predict2.5
- flow matching
- shifted logit-normal distribution
- 统一的 Text2World Image2World Video2World
- frame-replacement strategy
- Cosmos-Reason1 text encoder
claims_summary:
- Cosmos-Predict2.5 采用 flow matching 架构，并将 Text2World、Image2World 与 Video2World 统一到单一模型中，用
  Cosmos-Reason1 提供更丰富的文本表征与更细粒度控制。
- 在 VideoAlign 奖励模型下进行强化学习后，Cosmos-Predict2.5-2B 在 Text2World 与 Image2World 设置中的文本对齐、运动质量、视觉质量综合奖励整体提高，论文还报告
  RL 生成结果在人工投票中平均更受偏好。
- rCM 时间步蒸馏后的 Cosmos-Predict2.5-2B 在 PAI-Bench Text2World 与 Image2World 上取得与 teacher
  相近的定量结果，论文称其可用更少步骤生成高保真样本。
headline_metric: PAI-Bench-Predict-Image2World Overall Score
headline_value: 0.81
params_million: 2000.0
---

# WorldSimulationWithVideoFoundationModels

## Overview
Cosmos-Predict2.5 是面向 Physical AI 的视频世界基础模型，用 flow matching 统一 Text2World、Image2World 和 Video2World 生成。它用更严格的数据过滤、面向 Physical AI 的领域数据、Cosmos-Reason1 文本表征、SFT、模型合并和 RL 后训练，提升视频质量、指令对齐和可控仿真。论文还把它扩展为 Cosmos-Transfer2.5，用 control-net style 条件分支支持 Sim2Real、Real2Real、机器人和自动驾驶场景。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 8 falsifiable claims |
| [concepts.md](logic/concepts.md) | 15 concepts |
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
