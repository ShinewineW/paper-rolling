---
key: '2503.14492'
title: 'Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control'
authors: []
year: 2025
venue: null
doi: arXiv:2503.14492
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 时空控制图（Spatiotemporal Control Map）
- DiT-based ControlNet（扩散变换器控制网络）
- 多模态自适应控制（Adaptive Multimodal Control）
- Sim2Real 仿真到真实域迁移（Sim-to-Real Transfer）
- TransferBench 评测集
- 推理并行化扩展策略（Inference Parallelism Scaling）
- 提示上采样器（Prompt Upsampler）
claims_summary:
- 在均匀权重设置下融合全部四种模态（Vis、Edge、Depth、Seg）的多模态控制模型，在整体生成质量（Quality Score）上优于所有单模态控制模型，并在深度对齐上取得最佳结果。
- 通过对前景/背景区域赋予不同模态权重，时空控制图可独立调节各区域的对齐度与多样性，且模态权重与对应区域对齐指标呈强相关（Pearson相关系数绝对值达0.92-0.93）。
- 将各模态控制分支独立训练、推理时融合，相比同时训练所有分支，具有更低的显存需求、支持模态异构数据训练，并允许在推理时任意增减模态。
headline_metric: Quality Score
headline_value: 8.54
params_million: 7000.0
---

# Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control

## Overview
Cosmos-Transfer1 是一个基于扩散模型的多模态可控世界生成框架，通过在 Cosmos-Predict1 的 DiT 架构上添加多个 ControlNet 控制分支（每种模态对应一个分支），实现从分割、深度、边缘等多模态条件视频输入到世界模拟视频的高质量生成。核心创新是时空自适应控制图（spatiotemporal control map），允许在不同空间位置和时间帧为不同模态赋予不同权重，从而实现精细可控的世界生成。各控制分支独立训练、仅在推理时融合，兼顾内存效率与模态可扩展性。框架已在机器人 Sim2Real 数据生成和自动驾驶数据增强等 Physical AI 应用中展现出显著价值。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
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
