---
key: '2603.28955'
title: Enhancing Policy Learning with World-Action Model
authors: []
year: 2026
venue: null
doi: arXiv:2603.28955
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 世界-动作模型（WAM）
- 逆动力学目标（Inverse Dynamics Objective）
- 动作感知级联效应（Action-Aware Cascading Effect）
- RSSM（循环状态空间模型）
- WAM 训练目标（$$\mathcal{L}_{\mathrm{WAM}}$$）
- 潜在空间 MDP（$$\mathcal{M}_{\mathrm{wm}}$$）
- 扩散策略（DiffusionMLP）
claims_summary:
- 在 CALVIN 基准验证集上进行 50 步开环想象对比，WAM 在 PSNR、SSIM、LPIPS、FVD 四项生成质量指标上全面优于 DreamerV2 基线，且
  WAM 使用的训练步数远少于基线。
- 在相同策略架构（DiffusionMLP）和训练超参数下，使用 WAM 特征训练的扩散策略在 CALVIN 8 个操控任务的行为克隆阶段，平均成功率高于使用 DreamerV2
  特征的 DiWA 基线，8 个任务中 7 个取得更高成功率，关节型操控任务（如抽屉开关、滑轨移动）提升幅度最为显著。
- 在冻结世界模型潜空间中进行 800 轮 PPO 精调后，WAM 在 8 个 CALVIN 任务上的平均成功率高于 DiWA 基线，其中两个任务达到 100% 成功，精调所需的总物理交互次数均为零。
headline_metric: average_success_rate_PPO
headline_value: 92.8
params_million: 0.0
---

# Enhancing Policy Learning with World-Action Model

## Overview
WAM（World-Action Model）在 DreamerV2 的 RSSM 架构基础上增加逆动力学头，联合预测未来视觉观测与驱动状态转换的动作，使编码器表征同时兼顾视觉外观和动作因果结构。传统世界模型仅以观测重建为监督目标，用于下游策略的潜在特征 f_t 从未被显式引导编码动作相关信息，限制了行为克隆与模型内强化学习的效果。WAM 通过端到端训练目标 L_WAM 将逆动力学回归项注入编码器，并借助「后验 z_t → KL → 先验 ẑ_t」级联路径将动作感知结构传播至想象轨迹，无需修改策略架构即可同时提升世界模型生成质量与下游扩散策略性能。该方法在 CALVIN 基准 8 个操作任务上验证，仅需约 8.7 倍更少的训练步数即超越 DiWA 基线。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
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
