---
key: '2604.09059'
title: LearningVisionLanguageActionWorldModelsForAutonomousDriving
authors: []
year: null
venue: null
doi: arXiv:2604.09059
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- VLA-World
- VLA Models
- World Models
- Predictive Imagination
- Reflective Reasoning
- Short-term Prediction
- Condition-guided Generation
- Visual Tokens
claims_summary:
- VLA-World在nuScenes端到端轨迹规划评测中，相比多类非自回归与自回归基线取得更低的L2误差与碰撞率，并且论文将收益归因于动作条件未来帧生成与反思式轨迹修正。
- VLA-World在nuScenes未来帧生成评测中取得最低FID，论文认为即便未来帧只是中间推理步骤，也能有效释放多模态大模型的视觉生成能力。
- VLA-World在nuScenes动作预测任务中，相比基础Qwen2-VL-2B及其nuScenes微调版本，在横向与纵向动作类别上表现更好。
headline_metric: FID↓
headline_value: 9.8
params_million: 2000.0
---

# LearningVisionLanguageActionWorldModelsForAutonomousDriving

## Overview
VLA-World把VLA的行动推理和world model的未来想象放进同一条自回归链路：先从多视角观测和任务目标预测短时轨迹，再按该轨迹生成未来帧，随后对自生成未来进行反思并修正长时规划。这样做的动机是让规划不只模仿当前观测到动作的映射，而是显式看到自己动作可能造成的场景后果。论文用nuScenes-GR-20K和预训练、SFT、GRPO三个阶段，让生成、感知、推理和规划在同一策略中逐步对齐。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 10 concepts |
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
