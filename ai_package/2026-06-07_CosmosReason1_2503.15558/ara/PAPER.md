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
- 物理常识 (Physical Common Sense)
- 具身推理 (Embodied Reasoning)
- 物理AI本体论 (Physical AI Ontology)
- 混合 Mamba-MLP-Transformer 架构 (Hybrid Mamba-MLP-Transformer)
- GRPO (Group Relative Policy Optimization)
- 直觉物理 (Intuitive Physics)
- 规则化可验证奖励 (Rule-based Verifiable Rewards)
- Physical AI SFT (物理AI监督微调)
claims_summary:
- 基于精心整理的约400万条物理常识VQA与具身推理SFT数据对骨干VLM进行有监督微调后,Cosmos-Reason1在具身推理基准上相较各自骨干模型均提升超过10个百分点,在物理常识基准上亦有显著提升。
- 使用基于规则的可验证奖励(准确率奖励+格式奖励)进行强化学习后训练,可在SFT模型基础上进一步提升物理常识、具身推理与直觉物理任务的综合准确率。
- 在时间箭头(二分类)和物体恒常性任务上,包括Gemini 2.0 Flash、GPT-4o在内的当前最优VLM准确率接近随机猜测基线,揭示了现有评测体系未能有效衡量模型对物理世界的理解能力。
headline_metric: Intuitive Physics Avg Accuracy
headline_value: 74.5
params_million: 56000.0
---

# Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning

## Overview
Cosmos-Reason1 是专为 Physical AI 推理设计的多模态大语言模型系列(Cosmos-Reason1-7B 和 Cosmos-Reason1-56B),通过两阶段训练(Physical AI SFT 和 Physical AI RL)使模型具备物理常识推理与具身推理能力。论文构建了物理常识层级本体论(Space/Time/Fundamental Physics 三大类、16 子类)和具身推理二维本体论,并据此策划约 400 万条视频-文本标注数据及评测基准。模型以视频为主要感知输入,通过长链式思维(CoT)生成解释性洞察和具身决策(如「下一步动作」)。Physical AI SFT 在物理常识与具身推理基准上相较骨干模型提升超 10%,Physical AI RL 进一步提升超 5%。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
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
