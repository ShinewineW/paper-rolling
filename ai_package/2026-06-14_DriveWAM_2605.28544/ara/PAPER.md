---
key: '2605.28544'
title: 'DriveWAM: Video Generative Priors Enable Scalable World-Action Modeling for
  Autonomous Driving'
authors: []
year: null
venue: null
doi: arXiv:2605.28544
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- DriveWAM
- autoregressive video-action generation
- unified temporal token sequence
- world-action flow
- joint flow-matching objective
- scene-evolving driving guidance
- temporally localized guidance injection
- selective KV memory
claims_summary:
- DriveWAM 在 NAVSIM v1 上以单前视相机输入取得强规划表现，并在论文比较的同类端到端规划方法中整体占优。
- DriveWAM 在 PhysicalAI-Autonomous-Vehicles 的精选测试子集上优于论文比较的 VaVAM 与 Alpamayo-1.5。
- 将固定全局 prompt 替换为 chunk-specific 的 scene-evolving guidance，可以在不同训练数据规模下改善轨迹预测。
headline_metric: PDMS
headline_value: 90.1
params_million: 13000.0
---

# DriveWAM: Video Generative Priors Enable Scalable World-Action Modeling for Autonomous Driving

## Overview
DriveWAM 将 pretrained video diffusion transformer 改造成自动驾驶的 autoregressive video-action policy，把未来视频潜变量生成和 ego action 生成放在同一个 temporal token 序列里建模。它用 joint flow-matching objective 保留视频生成先验，同时让 action decoder 从生成的未来世界中读出可执行运动。为补上高层语义，模型用 frozen Qwen3-VL-8B 产生随场景演化的 chunk-specific guidance；为支持长时域 rollout，又用 selective KV memory 保留相关且不冗余的历史上下文。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
| [concepts.md](logic/concepts.md) | 10 concepts |
| [experiments.md](logic/experiments.md) | 7 experiments |

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
