---
key: '1803.10122'
title: World Models
authors: []
year: 2018
venue: null
doi: arXiv:1803.10122
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 世界模型 (World Model)
- VAE V模型 (Variational Autoencoder V Model)
- MDN-RNN M模型 (Mixture Density Network RNN M Model)
- 控制器 C模型 (Controller C Model)
- 梦境训练 (Dream Training / Latent Space Training)
- 温度参数τ (Temperature Parameter τ)
- 对抗性策略问题 (Adversarial Policy / Cheating the World Model)
- CMA-ES进化策略 (CMA-ES Evolution Strategy)
claims_summary:
- 将智能体分解为视觉模块V（VAE）、记忆模块M（MDN-RNN）和控制器C（线性层），以无监督方式快速训练大容量世界模型，再用参数极少的控制器利用其表示完成强化学习任务，从而绕开信用分配问题对大型网络训练的瓶颈。
- 仅使用VAE空间特征zₜ的控制器（含或不含隐藏层）均无法达到CarRacing-v0的解任务阈值（100次平均分900），而同时使用zₜ和MDN-RNN隐状态hₜ的完整世界模型控制器达到新最优性能，并据论文所述首次解决该任务。
- 以MDN-RNN为核心构建的虚拟OpenAI Gym环境（DoomRNN）可完全替代真实VizDoom环境进行策略训练；梦境中习得的策略部署到真实环境后，存活时步数远超解任务阈值（750步），且超越了已知排行榜最优成绩。
headline_metric: avg_score (CarRacing-v0)
headline_value: 906.0
params_million: 4.35
---

# World Models

## Overview
本文提出一个受人类认知系统启发的「世界模型」智能体框架，将智能体分解为三个组件：负责空间压缩的视觉模型V（变分自编码器）、负责时序预测的记忆模型M（MDN-RNN）以及极小的控制器C（线性模型，用CMA-ES优化）。世界模型V+M以无监督方式学习环境的压缩时空表示，控制器C仅在这些表示上进行决策。核心贡献在于：智能体可以完全在M生成的「幻梦」虚拟环境中训练，再将策略迁移回真实环境，首次解决了CarRacing-v0任务。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 8 concepts |
| [experiments.md](logic/experiments.md) | 3 experiments |

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
