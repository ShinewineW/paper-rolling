---
key: '2405.17398'
title: 'Vista: A Generalizable Driving World Model with High Fidelity and Versatile
  Controllability'
authors: []
year: 2024
venue: null
doi: arXiv:2405.17398
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 潜变量替换
- 动态增强损失
- 结构保留损失
- 动态先验注入
- 可泛化奖励函数
- 动作独立性约束
- 三角分类器无关引导方案
claims_summary:
- Vista 在 nuScenes 验证集的 FID 和 FVD 指标上超越所有已报告的驾驶世界模型，FID 相较最优基线提升 55%，FVD 相较最优基线提升
  27%
- Vista 在跨越 nuScenes、Waymo、OpenDV-YouTube-val 及 CODA 四个数据集的人类评估中，对视觉质量和运动合理性两个维度均超过最先进通用视频生成器超过
  70% 的比较次数
- 与仅使用标准扩散损失相比，引入动态增强损失后，模型对运动实例（如移动车辆）的预测更加真实，能够生成符合物理规律的运动（如车辆正常前行、场景几何随转向正确偏移）
headline_metric: FID
headline_value: 6.9
params_million: 2500.0
---

# Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability

## Overview
Vista 是基于 Stable Video Diffusion (SVD) 定制化构建的可泛化自动驾驶世界模型，通过动力学增强损失和结构保持损失显著提升高分辨率未来帧的预测保真度。利用「潜变量替换」方法将多帧历史帧作为位置/速度/加速度先验注入模型，使其可连续自回归地生成长时序驾驶视频。通过统一的 Fourier 嵌入条件接口，Vista 支持从高层意图(指令、目标点)到低层操控(轨迹、方向角、速度)的多模态动作条件，并可零样本泛化至未见数据集。此外，Vista 还被设计为可泛化的奖励函数，利用预测不确定性在无真值动作的情况下评估驾驶策略可靠性。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
| [experiments.md](logic/experiments.md) | 6 experiments |

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
