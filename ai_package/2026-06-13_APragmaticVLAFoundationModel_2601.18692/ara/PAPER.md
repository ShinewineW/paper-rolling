---
key: '2601.18692'
title: APragmaticVLAFoundationModel
authors: []
year: 2026
venue: null
doi: arXiv:2601.18692
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Vision-Language-Action foundation model
- LingBot-VLA
- pre-trained VLM
- action expert
- Mixture-of-Transformers
- observation condition
- action chunk
- Flow Matching
claims_summary:
- LingBot-VLA 在 GM-100 真实世界评估中相对 WALL-OSS、GR00T N1.6 与 π0.5 表现更强，优势同时体现在任务完成与分步进展两个指标上。
- 加入基于 LingBot-Depth 的深度蒸馏后，LingBot-VLA w/ depth 在聚合真实世界结果中优于 π0.5，并在若干平台和任务上改善 SR
  或 PS。
- 在 RoboTwin 2.0 仿真评估中，LingBot-VLA 两个变体相对 π0.5 在 clean 和 randomized 场景的平均成功率上表现更好。
headline_metric: Success Rate (SR)
headline_value: 17.3
params_million: 3000.0
---

# APragmaticVLAFoundationModel

## Overview
LingBot-VLA 是面向真实机器人操作的 VLA foundation model，将预训练 VLM、action expert 与 Mixture-of-Transformers 组合起来，让语言和多视角视觉条件持续引导动作生成。方法用 Flow Matching 建模连续动作，并通过深度表示蒸馏补充空间感知，目标是在跨任务、跨平台迁移时兼顾泛化能力和训练效率。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 11 concepts |
| [experiments.md](logic/experiments.md) | 5 experiments |

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
