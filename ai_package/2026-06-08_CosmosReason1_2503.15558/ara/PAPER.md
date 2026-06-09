---
key: '2503.15558'
title: 'Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning'
authors: []
year: 2025
venue: null
doi: arXiv:2503.15558
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Physical AI
- 物理常识层级本体
- 具身推理二维本体
- GRPO（组内相对策略优化）
- 基于规则的可验证奖励
- 混合 Mamba-MLP-Transformer 架构
- 直觉物理（Intuitive Physics）
- 异步 RL 训练框架
claims_summary:
- 经过专门的 Physical AI SFT 训练（约 400 万条视频-文本标注），Cosmos-Reason1-7B 和 Cosmos-Reason1-56B
  在物理常识和具身推理基准上，相比各自骨干 VLM 均实现超过 10% 的平均准确率提升。
- 基于规则可验证奖励（准确率奖励 + 格式奖励）的 GRPO RL 后训练，能在 Physical AI SFT 模型基础上进一步提升物理常识和具身推理的整体平均准确率。
- 经过专门的直觉物理 SFT（空间拼图 11K、时间箭头 30K、物体永恒 10K 样本），Cosmos-Reason1-7B 在三项直觉物理任务上均显著优于同规模骨干
  VLM，整体平均提升幅度远超随机猜测水平。
headline_metric: 物理AI综合平均准确率（Avg.）——物理常识与具身推理联合基准，Cosmos-Reason1-7B 经 Physical AI
  RL 后训练
headline_value: 65.7
params_million: 7000.0
---

# Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning

## Overview
Cosmos-Reason1 是 NVIDIA 推出的专为物理AI推理设计的多模态大语言模型家族，包含 Cosmos-Reason1-7B 和 Cosmos-Reason1-56B 两个规模。论文首先提出两套本体框架——涵盖空间/时间/基础物理三大类16个细粒度子类的物理常识本体，以及4类能力×5类具身智能体的二维具身推理本体——以系统定义 Physical AI 所需能力。模型经两阶段训练：Physical AI SFT（基于约4M视频-文本对及从 DeepSeek-R1 提炼的长链式推理轨迹）和 Physical AI RL（基于规则可验证奖励的 GRPO 后训练），在物理常识、具身推理和直觉物理三类任务上均取得显著提升。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
| [concepts.md](logic/concepts.md) | 8 concepts |
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
