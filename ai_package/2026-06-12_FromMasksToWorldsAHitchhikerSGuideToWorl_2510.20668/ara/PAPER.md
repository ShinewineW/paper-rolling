---
key: '2510.20668'
title: FromMasksToWorldsAHitchhikerSGuideToWorl
authors: []
year: 2025
venue: null
doi: arXiv:2510.20668
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- True World Model
- Generative Heart
- Interactive Loop
- Memory System
- Mask-based Models
- Unified Models
- Interactive Generative Models
- Memory and Consistency
claims_summary:
- 论文主张真世界模型不是单一实体，而是由生成核心、交互闭环和持久记忆系统合成；这些子系统分别支撑世界状态生成、实时行动感知循环和长时域一致性。
- 论文将世界模型的发展描述为从掩码建模到统一模型、再到交互生成模型和记忆一致性系统，最终综合为真世界模型的窄路。
- 论文主张，仅有实时交互不足以形成持久世界；隐式逐帧生成容易遗忘和漂移，显式空间表示虽有稳定导航优势但仍需处理动态状态，因而需要专门的记忆和一致性策略。
headline_metric: fps
headline_value: 24.0
params_million: 0.0
---

# FromMasksToWorldsAHitchhikerSGuideToWorl

## Overview
本文不是常规综述，而是为构建 world models 给出一条收窄后的路线图：从 Mask-based Models 出发，经 Unified Models、Interactive Generative Models、Memory and Consistency，走向 True World Models。核心判断是，真正的 world model 需要把 generative heart、interactive loop 与 memory system 合成一个能持续运行的整体。它强调从静态预测或一次性生成，转向可交互、可记忆、能保持长期一致性的世界。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 3 falsifiable claims |
| [concepts.md](logic/concepts.md) | 14 concepts |
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
