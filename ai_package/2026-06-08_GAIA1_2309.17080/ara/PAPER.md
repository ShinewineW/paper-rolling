---
key: '2309.17080'
title: 'GAIA-1: A Generative World Model for Autonomous Driving'
authors: []
year: 2023
venue: null
doi: arXiv:2309.17080
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 生成式世界模型（Generative World Model）
- 向量量化图像标记化（VQ Image Tokenization）
- DINO语义蒸馏归纳偏置（DINO Semantic Distillation Inductive Bias）
- 自回归下一令牌预测（Autoregressive Next-Token Prediction）
- 无分类器引导（Classifier-Free Guidance）
- 视频扩散解码器（Video Diffusion Decoder）
- Top-k采样策略（Top-k Sampling Strategy）
- 世界模型缩放定律（World Model Scaling Laws）
claims_summary:
- GAIA-1将世界建模定义为无监督下一词元预测问题，通过将视频帧、文本和动作编码为离散词元序列，利用自回归Transformer预测未来图像词元，实现对自车行为和场景特征具备精细控制能力的真实驾驶视频生成。
- 与大型语言模型中观察到的缩放规律类似，GAIA-1世界模型的验证交叉熵与模型规模/计算量之间遵循幂律关系，可用不超过1/20计算量的小模型准确预测最终性能。
- GAIA-1在大规模真实驾驶数据上通过自监督训练后，涌现出包括高层结构与场景动态理解、泛化与创造性、上下文感知与3D几何理解在内的多项能力，并能外推至训练数据中未曾出现的驾驶行为（如超出道路边界行驶）。
headline_metric: world model 参数量(B)
headline_value: 6.5
params_million: 6500.0
---

# GAIA-1: A Generative World Model for Autonomous Driving

## Overview
GAIA-1 是一个面向自动驾驶的生成式世界模型，将视频、文本和动作三种输入模态映射为离散token序列，并以自回归下一token预测建模世界动态。模型分为两部分：自回归Transformer世界模型负责推理场景高层语义与时序动态，视频扩散解码器负责将隐token还原为高保真像素视频。GAIA-1 在保留世界模型结构化动态推理能力的同时继承了生成视频模型的视觉真实感，并通过动作和文本条件实现对自车行为与场景属性的精细控制。该方法在真实伦敦城市驾驶数据上以无监督方式训练，涌现出对3D几何、交通规则和因果交互的理解。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 9 concepts |
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
