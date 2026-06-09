---
key: '2506.21539'
title: 'WorldVLA: Towards Autoregressive Action World Model'
authors: []
year: 2025
venue: null
doi: arXiv:2506.21539
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 动作世界模型（Action World Model）
- 动作注意力掩码策略（Action Attention Masking）
- 动作分块生成（Action Chunking）
- 统一多模态词表（Unified Vocabulary）
- 世界模型与动作模型的互增强（Mutual Enhancement）
- 误差传播（Error Propagation in Autoregressive Action Generation）
claims_summary:
- WorldVLA 将 VLA 动作模型与世界模型统一在单一离散自回归框架中，两者相互增益：世界模型提升动作生成性能，动作模型提升视频生成质量，联合框架整体优于各自独立模型。
- 在 LIBERO 基准上，加入世界模型数据联合训练后，WorldVLA 平均抓取成功率相较单独动作模型提升约 4%；在 LIBERO-Long 任务上提升尤为显著。
- 与单独世界模型相比，WorldVLA 动作世界模型在长序列（50 帧）视频生成上具有更低的 FVD，表明动作模型对视觉理解的增强有助于生成更物理合理的视频序列。
headline_metric: Average SR
headline_value: 81.8
params_million: 7000.0
---

# WorldVLA: Towards Autoregressive Action World Model

## Overview
WorldVLA 是一个以 Chameleon 为骨干的自回归动作世界模型，在单一 LLM 框架中将动作预测（VLA）与世界状态预测统一到共享词表下。世界模型通过学习物理规律来预测未来帧，从而增强动作生成质量；动作模型通过深化视觉理解来提升世界模型的视觉生成准确性，两者双向互促。针对动作块自回归生成时误差传播的问题，论文额外提出了动作注意力掩码策略，让每个动作仅依赖视觉输入而非先前动作，显著改善了多步动作生成性能。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
| [concepts.md](logic/concepts.md) | 6 concepts |
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
