---
key: '2501.03575'
title: Cosmos World Foundation Model Platform for Physical AI
authors: []
year: 2025
venue: null
doi: arXiv:2501.03575
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 世界基础模型 (World Foundation Model, WFM)
- 视频分词器 (Video Tokenizer)
- 预训练后训练范式 (Pre-training and Post-training Paradigm)
- 时序因果分词 (Temporal Causal Tokenization)
- EDM 扩散训练目标 (EDM Denoising Score Matching Loss)
- 自回归世界基础模型 (Autoregressive WFM)
- 扩散解码器 (Diffusion Decoder)
- Medusa 推测解码 (Medusa Speculative Decoding)
claims_summary:
- Cosmos WFM平台采用「预训练→后训练」两阶段范式，通过大规模多样视频数据预训练获得通才WFM，再通过少量领域数据微调即可适配相机控制、机器人操控和自动驾驶等多个物理AI下游任务，后训练模型在各任务上均显著优于从头训练的专用基线
- Cosmos Tokenizer在DAVIS和TokenBench多个基准上的PSNR、SSIM、rFVD等重建指标均超越现有连续和离散视频tokenizer，在A100
  GPU上推理速度显著快于同类方法，且参数量更小；在更高压缩率下仍保持优于对比方法低压缩率时的重建质量
- 在3D一致性评估中，扩散型WFM的Sampson几何误差更低、相机位姿估计成功率更高；在物理对齐评估中，扩散型WFM在多帧条件设置下的像素级预测指标优于自回归型；扩散型WFM的总体感知视觉质量更高
headline_metric: FVD
headline_value: 120.49
params_million: 7000.0
---

# Cosmos World Foundation Model Platform for Physical AI

## Overview
Cosmos World Foundation Model (WFM) Platform 是 NVIDIA 为 Physical AI 构建的开放世界模型平台，采用「预训练→微调」范式：先在约 2000 万小时多样化视频上训练通用世界基础模型，再针对具体 Physical AI 场景进行轻量级领域微调。平台涵盖视频数据处理流水线、连续/离散视频 Tokenizer（Cosmos-Tokenize1）、基于扩散与自回归 Transformer 的预训练 WFM（Cosmos-Predict1 系列）、后训练样例（摄像机控制、机器人操控、自动驾驶多视角），以及安全护栏系统，并以 NVIDIA Open Model License 开放权重，支持开发者在其之上构建定制化世界模型。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 8 falsifiable claims |
| [concepts.md](logic/concepts.md) | 8 concepts |
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
