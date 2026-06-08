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
- 物理常识本体（Physical Common Sense Ontology）
- 具身推理本体（Embodied Reasoning Ontology）
- GRPO（Group Relative Policy Optimization）
- 直觉物理推理（Intuitive Physics Reasoning）
- 异步 RL 训练框架（Asynchronous RL Training Framework）
- 混合 Mamba-MLP-Transformer 骨干（Hybrid Mamba-MLP-Transformer Backbone）
- 规则化可验证奖励（Rule-based Verifiable Rewards）
claims_summary:
- 针对物理AI能力的专项监督微调（SFT）使7B模型在物理常识基准平均准确率相对骨干模型提升6.9分、在具身推理基准提升11.0个百分点，使56B模型在物理常识基准提升2.0分、在具身推理基准提升10.2个百分点。
- 在Physical AI SFT基础上，利用规则化可验证奖励进行强化学习后训练，Cosmos-Reason1-7B整体综合平均准确率进一步提升5.0分（从60.7提升至65.7），直觉物理平均准确率进一步提升7.0分。
- 所提出的全异步RL训练框架通过分离策略训练节点与Actor展开节点并使用统一调度器，与主流同位框架相比实现约160%的训练效率提升，同时支持节点故障热恢复与动态弹性扩缩容。
headline_metric: 直觉物理基准平均准确率 (Cosmos-Reason1-7B SFT)
headline_value: 74.5
params_million: 7000.0
---

# Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning

## Overview
Cosmos-Reason1 是 NVIDIA 推出的物理 AI 推理多模态大语言模型系列，包含 7B 和 56B 两个规模。论文首先构建层次化物理常识本体论（Space / Time / Fundamental Physics 三大类、16 个细粒度子类）和二维具身推理本体论（4 种推理能力 × 5 类具身主体），为物理 AI 能力提供结构化定义与衡量框架。在此基础上，模型经历 Physical AI SFT（约 400 万视频-文本对，含长链式推理追踪）和 Physical AI RL（规则可验证多选题奖励）两阶段训练，使模型能够通过长链式思维过程感知物理世界并生成自然语言形式的具身决策。代码与模型权重以 NVIDIA Open Model License 开源。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
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
