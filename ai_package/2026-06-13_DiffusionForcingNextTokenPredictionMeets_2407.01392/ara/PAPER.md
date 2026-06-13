---
key: '2407.01392'
title: DiffusionForcingNextTokenPredictionMeets
authors: []
year: 2024
venue: null
doi: arXiv:2407.01392
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Diffusion Forcing
- Causal Diffusion Forcing
- 噪声作为部分遮蔽
- 独立逐 token 噪声水平
- 训练目标
- all sequences of noise levels
- 采样调度矩阵
- Monte Carlo Guidance
claims_summary:
- 在D4RL迷宫规划中，Diffusion Forcing通过不同时间步的噪声日程和MCG，将未来不确定性纳入引导采样；论文报告其平均奖励优于主要离线强化学习与Diffuser基线，去掉MCG后性能下降。
- 在Minecraft和DMLab视频预测中，Causal Diffusion Forcing被用于自回归滚动，论文称其能在训练视野之外保持稳定，而teacher
  forcing和causal full-sequence diffusion基线较快发散。
- 在水果换位机器人任务中，Diffusion Forcing利用潜状态记忆处理非马尔可夫观察，并在视觉干扰或遮挡时通过噪声观测机制依赖先验，从而优于无记忆的diffusion
  policy和next-frame diffusion基线。
headline_metric: Single-task Average reward
headline_value: 141.7
params_million: 4.33
---

# DiffusionForcingNextTokenPredictionMeets

## Overview
Diffusion Forcing 把序列生成看成沿时间轴和噪声轴同时做部分遮蔽：每个 token 都带有独立噪声水平，模型学习从任意噪声组合中去噪。论文把它实例化为 Causal Diffusion Forcing，用因果 RNN 在保留 next-token prediction 可变长度能力的同时，引入 full-sequence diffusion 的引导采样能力。这样做的目的，是让连续序列、规划轨迹和机器人控制既能按需延展，又能在采样时被目标或奖励引导。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 4 falsifiable claims |
| [concepts.md](logic/concepts.md) | 9 concepts |
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
