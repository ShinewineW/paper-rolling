---
key: '2301.04104'
title: Mastering Diverse Domains through World Models
authors: []
year: 2023
venue: null
doi: arXiv:2301.04104
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 循环状态空间模型(RSSM)
- symlog/symexp 变换
- symexp twohot 损失
- 回报百分位归一化
- 自由比特(Free Bits)
- 想象训练(Imagination Training)
- 1% Unimix 均匀混合
claims_summary:
- DreamerV3是一种通用强化学习算法，在固定超参数的条件下，可在超过150个多样化任务中超越针对各领域专门设计并调优的专家算法，并大幅优于通用的PPO算法。
- DreamerV3是首个在不使用人类数据、不使用自适应课程学习的条件下，从稀疏奖励出发、从零开始在Minecraft中采集到钻石的算法；所有DreamerV3运行均在100M环境步内发现钻石，而所有对比基线均未能发现钻石。
- DreamerV3中的一系列鲁棒性技术——包括KL平衡与自由位、1%均匀混合分布、百分位数回报归一化（带分母下限）、symexp twohot损失——共同使得算法在多样领域下无需超参数调优即可稳定学习。每种技术对部分任务至关重要，但不一定对所有任务均有显著影响。
headline_metric: Minecraft Diamond Return
headline_value: 9.1
params_million: 200.0
---

# Mastering Diverse Domains through World Models

## Overview
DreamerV3 是一个通用强化学习算法，通过学习环境的世界模型并在想象的未来轨迹中优化 Actor-Critic 策略，以单一固定超参数配置在 150 余个多样化任务上超越各领域专用算法。其核心创新是一套稳健性技术——包括 symlog 变换、KL free bits、百分位回报归一化和 symexp twohot 损失——用于消除跨域学习中信号幅度差异导致的训练不稳定问题。算法在世界模型的无监督重建目标驱动下形成丰富表示，无需依赖任务特定的奖励梯度即可实现有效感知。DreamerV3 还是首个在无人类数据或课程设置前提下于 Minecraft 中从零收集钻石的算法，达成了 AI 领域的重要里程碑。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
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
