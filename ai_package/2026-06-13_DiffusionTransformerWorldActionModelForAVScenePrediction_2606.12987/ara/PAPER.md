---
key: '2606.12987'
title: DiffusionTransformerWorldActionModelForAVScenePrediction
authors: []
year: null
venue: null
doi: arXiv:2606.12987
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 动作条件世界模型
- Stable-Diffusion-VAE encode-predict-decode
- 空间 tokens
- AnchoredVAEDiT
- x0 预测目标
- 残差锚定
- Fourier action embedding
- 感知-失真前沿
claims_summary:
- 在冻结视觉编码器基准中，V-JEPA2 rep64利用时间上下文，相比单帧编码器在steering RMSE上表现更好；论文将改进归因于时间视频表征捕获了单帧不可见的帧间ego-motion模式与车道曲率动态。
- 在SD-VAE encode-predict-decode管线中，direct regression在CosSim等失真指标上更强，但diffusion经过train-derived
  calibration后在KID和FID等分布指标上更接近真实帧分布。
- 论文将single-pass模型的有限coherent motion诊断为shared-present anchoring问题，并用chain-anchor jump
  model通过逐步re-anchoring恢复更好的前向运动方向与低频运动幅度。
headline_metric: KID
headline_value: 0.078
params_million: 5.4
---

# DiffusionTransformerWorldActionModelForAVScenePrediction

## Overview
本文构建一个紧凑的 action-conditioned DiT 世界模型：输入当前前视相机的 Stable-Diffusion VAE latent 和 ego-actions，预测未来场景 latent，再由冻结 VAE decoder 渲染为帧。作者先比较多个冻结视觉编码器以回答该在哪个 latent 空间预测，再通过诊断实验确定 DiT 在紧凑 latent 中需要空间 token、x_0 预测目标、残差锚定和与目标不确定性匹配的采样。核心价值在于指出常规失真指标会偏爱模糊的回归均值，而分布指标能揭示 diffusion 预测更接近真实帧分布。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 11 concepts |
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
