---
key: '2604.04198'
title: DriveVAVideoActionModelsAreZeroShotDrivers
authors: []
year: null
venue: null
doi: arXiv:2604.04198
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- DriveVA
- 共享潜在生成过程
- 视频-轨迹一致性
- action chunk
- future video clip
- video continuation
- DiT decoder
- IDM-style action grounding
claims_summary:
- DriveVA 在 NAVSIM Navtest 闭环指标上优于论文比较的传统端到端方法和 WorldModel Methods。
- 在从 NAVSIM 训练后直接评估到 nuScenes 与 Bench2Drive 的零样本设置中，DriveVA 相比论文中的 WorldModel Methods
  表现更强。
- DriveVA 生成的视频所隐含的运动与模型预测轨迹保持较强一致性。
headline_metric: PDMS
headline_value: 90.9
params_million: 5000.0
---

# DriveVAVideoActionModelsAreZeroShotDrivers

## Overview
DriveVA把未来视频想象和未来动作序列放进同一个 latent generative process 中，由 DiT decoder 共同解码，而不是先生成世界再单独规划。它利用 Wan2.2-TI2V-5B 的视频先验，把大规模视频模型学到的时空运动和物理合理性迁移到自动驾驶规划。方法还加入 video continuation，让短窗口预测可以递归滚动，缓解长时域 rollout 中视频和轨迹逐步脱节的问题。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 10 concepts |
| [experiments.md](logic/experiments.md) | 10 experiments |

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
