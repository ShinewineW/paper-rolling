---
key: '2603.27287'
title: UniWorldVLAInterleavedWorldModelingAndPlanningForAD
authors: []
year: null
venue: null
doi: arXiv:2603.27287
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Uni-World VLA
- interleaved frame-action generation
- contextual tokens
- dynamic tokens
- action tokens
- depth fusion
- Dynamic Focal Loss
- bi-directional intra-frame attention
claims_summary:
- Uni-World VLA 在 NAVSIM 测试划分上相对传统端到端方法与世界模型方法取得更强的闭环规划综合表现，同时保持有竞争力的未来视频生成质量。
- 将未来帧与动作按评测频率对齐并严格交错生成，比高频动作帧交替、滑动动作窗口等替代生成方案带来更好的规划表现。
- 在预训练与未来帧建模均启用时，加入 Depth Anything 3 提供的 monocular depth 信息并通过 cross-attention 融合，可改善未来帧生成质量，并在部分规划子指标上带来补充收益。
headline_metric: PDMS
headline_value: 89.4
params_million: -1.0
---

# UniWorldVLAInterleavedWorldModelingAndPlanningForAD

## Overview
Uni-World VLA 将自动驾驶中的未来场景预测和轨迹规划放进同一个 VLA 自回归框架，按时间步交替生成未来视觉 token 与 action token。这样做的目的，是避免先完整幻想未来再规划时形成开环滚动，让每一步规划都能继续条件化在刚生成的未来观测上。模型还把 Depth Anything 3 估计的单目深度特征通过 cross-attention 融入历史视觉 token，用几何线索增强长时域未来帧预测。

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
