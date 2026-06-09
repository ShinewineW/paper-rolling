---
key: '2411.15139'
title: 'DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving'
authors: []
year: 2024
venue: null
doi: arXiv:2411.15139
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 截断扩散策略
- 锚定高斯分布
- 模式多样性分数
- 级联扩散解码器
- 模式坍塌
- 条件扩散模型（前向与反向过程）
- 推理灵活性
- PDM分数（PDMS）
claims_summary:
- 通过引入基于K-Means聚类锚点构建的锚定高斯分布并截断扩散时间表,截断扩散策略将去噪起点从纯高斯噪声替换为多模式锚定分布,从而解决原始扩散策略的模态崩溃问题,并将推理所需去噪步数从20步压缩至2步
- DiffusionDrive在NAVSIM navtest split上以相同ResNet-34主干网络仅用20个锚点实现88.1 PDMS,超越所有先前方法(包括使用8192个锚点和额外监督及后处理的强力竞争者),同时在NVIDIA
  4090上以45 FPS实时速度运行
- 所提出的级联扩散解码器通过稀疏可变形空间交叉注意力与BEV/PV特征交互、与智能体/地图查询的交叉注意力以及级联迭代精化机制,在参数量少于基于UNet方案的条件下显著提升规划质量
headline_metric: PDMS
headline_value: 88.1
params_million: 60.0
---

# DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving

## Overview
DiffusionDrive 是一种面向端到端自动驾驶的截断扩散策略模型，通过将先验多模态锚点嵌入扩散过程，使模型从「锚定高斯分布」而非随机高斯分布开始去噪，从而在仅 2 步内生成高质量多模态行驶轨迹。与此同时，作者设计了高效的级联扩散解码器，通过稀疏可变形注意力与 BEV/透视视图特征及感知查询进行多层次交互。该方法将去噪步骤较普通扩散策略减少 10 倍，在 NVIDIA 4090 上达到 45 FPS 实时推理速度，并在 NAVSIM 数据集上取得 88.1 PDMS 的当时最优结果。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
| [concepts.md](logic/concepts.md) | 8 concepts |
| [experiments.md](logic/experiments.md) | 9 experiments |

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
