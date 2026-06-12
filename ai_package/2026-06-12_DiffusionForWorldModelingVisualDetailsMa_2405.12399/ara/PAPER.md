---
key: '2405.12399'
title: DiffusionForWorldModelingVisualDetailsMa
authors: []
year: 2024
venue: null
doi: arXiv:2405.12399
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- DIAMOND
- 扩散世界模型
- Score-based diffusion
- EDM
- DDPM 对照
- 自回归想象
- NFE 与去噪步数
- 单步采样与多步采样
claims_summary:
- 在 Atari 100k benchmark 上，DIAMOND 相比同类完全在 world model 内训练的代理取得更高的平均表现，并在若干需要小视觉细节的游戏上表现突出。
- 相对 DDPM，基于 EDM 的 diffusion world model 在少量 denoising steps 下更能维持长时序 imagined trajectories
  的稳定性。
- 单步 denoising 在多模态后验或部分可观测情形下容易生成模糊或折中结果，而多步采样更能趋向具体模式，并在定量消融中总体更优。
headline_metric: mean human normalized score
headline_value: 1.46
params_million: 13.0
---

# DiffusionForWorldModelingVisualDetailsMa

## Overview
DIAMOND 将世界模型从离散 latent 序列转向图像空间的 diffusion 生成，直接按过去观测和动作条件化来预测下一帧。这样做的动机是保留对强化学习决策有影响的视觉细节，同时利用 diffusion 易条件化和建模多模态分布的性质。论文强调仅把 diffusion 放进世界模型还不够，需要 EDM 预条件、低 NFE 采样、奖励与终止模型以及想象中训练的 actor-critic 配合，才能在长时间 rollout 中稳定可用。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
| [concepts.md](logic/concepts.md) | 13 concepts |
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
