---
key: '2509.24527'
title: TrainingAgentsInsideOfScalableWorldModel
authors: []
year: 2025
venue: null
doi: arXiv:2509.24527
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Dreamer 4
- world model
- causal tokenizer
- interactive dynamics model
- shortcut forcing
- x-prediction
- ramp loss weight
- imagination training
claims_summary:
- Dreamer 4 通过在世界模型中进行想象训练，可以在不进行在线环境交互的离线设置中完成 Minecraft 钻石挑战，并且相对行为克隆类基线表现更强。
- Dreamer 4 的世界模型在 Minecraft 中比 Oasis、Lucid-v1 和 MineWorld 更能支持复杂物体交互与游戏机制的实时交互式模拟。
- Dreamer 4 可以从大量无动作标签视频中吸收主要世界知识，只用少量配对动作视频学习动作条件化，并能泛化到只在无标签视频中出现的 Minecraft 维度。
headline_metric: Success rates for Diamond
headline_value: 0.7
params_million: 2000.0
---

# TrainingAgentsInsideOfScalableWorldModel

## Overview
Dreamer 4 把可扩展 world model 变成离线控制智能体：先用视频和动作预训练 tokenizer 与 dynamics model，再把任务 token、policy、reward、value 接入同一个 transformer。它的核心动机是让智能体不依赖在线环境交互，而是在模型想象出的轨迹中做 reinforcement learning。方法上，shortcut forcing objective 与高效 block-causal transformer 共同服务于两件事：更准确地预测 Minecraft 物体交互与游戏机制，同时保持实时交互推理。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 10 concepts |
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
