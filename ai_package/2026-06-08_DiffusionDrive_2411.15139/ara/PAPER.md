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
- 锚点高斯分布
- 模式多样性得分
- 级联扩散解码器
- 训练目标函数
- K-Means先验锚点
- 推理灵活性
claims_summary:
- 提出截断扩散策略，将去噪起点从纯高斯噪声改为锚定高斯分布，使去噪步数从20步缩减至2步（相比原始扩散策略减少10倍），同时将模式多样性得分D从11%提升至74%，FPS从7提升至45
- 使用对齐的ResNet-34骨干网络，DiffusionDrive在NAVSIM navtest分割上达到88.1 PDMS，超越所有先前方法，且不依赖后处理，同时在NVIDIA
  4090上以45 FPS运行
- 将原始DDIM扩散策略（Transfuser_DP）应用于自动驾驶时，从不同高斯噪声采样的20条轨迹在去噪后高度重叠，模式多样性得分D仅为11%；同时20步去噪使FPS从60降至7，无法满足实时需求
headline_metric: PDMS
headline_value: 88.1
params_million: 60.0
---

# DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving

## Overview
DiffusionDrive 是首个将扩散模型引入端到端自动驾驶的实时系统。其核心创新是「截断扩散策略」：用 K-Means 聚类得到少量（20个）先验锚轨迹，在锚轨迹附近加入少量高斯噪声构建「锚定高斯分布」，训练模型仅需从该分布去噪2步即可还原多模态驾驶轨迹，相比普通扩散策略减少10倍去噪步数。配合高效的级联扩散解码器（通过稀疏可变形注意力与 BEV/PV 特征及感知查询交互），DiffusionDrive 在 NAVSIM navtest 上以 45 FPS 实时运行并取得88.1 PDMS 的最优成绩。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
| [experiments.md](logic/experiments.md) | 8 experiments |

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
