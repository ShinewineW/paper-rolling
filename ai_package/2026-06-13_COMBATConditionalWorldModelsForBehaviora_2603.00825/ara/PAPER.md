---
key: '2603.00825'
title: COMBATConditionalWorldModelsForBehaviora
authors: []
year: 2026
venue: null
doi: arXiv:2603.00825
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- COMBAT
- 部分观测多智能体轨迹
- Player 1 动作条件
- Player 2 涌现策略
- Deep Compression AutoEncoder latent
- joint RGB-pose representation
- autoregressive Diffusion Transformer
- AdaLNZero conditioning
claims_summary:
- COMBAT 的 visual–pose 版本在标准感知指标上优于 RGB-only 版本，说明显式姿态信息有助于生成质量。
- 在只以 Player 1 输入作为条件的训练设置下，COMBAT 生成的 Player 2 攻击活动量和拳脚比例随训练 checkpoint 呈现不同阶段，显示出从过度活跃到更接近人类行为模式的变化。
- 论文提出基于 health data 的 damage distribution analysis 和 health trajectory analysis，用于检验生成
  gameplay 是否学习到游戏内在规则、动作后果和比赛节奏。
headline_metric: FVD↓
headline_value: 593.4
params_million: 1200.0
---

# COMBATConditionalWorldModelsForBehaviora

## Overview
COMBAT把Tekken 3 gameplay建模为由Player 1输入条件驱动的条件视频生成问题，用Diffusion Transformer在压缩潜空间中自回归预测后续画面。它的目的不是只复现视觉帧，而是在没有Player 2动作标签的情况下，让对手行为从时间一致、交互合理的生成目标中自然出现。模型结合RGB与pose潜表示，并用CausVid DMD和decoder distillation把生成推向实时交互。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 4 falsifiable claims |
| [concepts.md](logic/concepts.md) | 13 concepts |
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
