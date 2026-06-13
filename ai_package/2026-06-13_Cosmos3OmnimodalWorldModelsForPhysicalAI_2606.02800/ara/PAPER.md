---
key: '2606.02800'
title: Cosmos3OmnimodalWorldModelsForPhysicalAI
authors: []
year: 2026
venue: null
doi: arXiv:2606.02800
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Cosmos 3
- omnimodal world model
- Physical AI
- understanding
- generation
- action token
- unified action representation
- action tokenization
claims_summary:
- Cosmos 3 在推理、图像生成、视频生成、音频生成、迁移生成和动作生成上都给出了同一模型族或后训练变体的结果，论文据此主张它可以作为 Physical AI
  的通用 backbone。
- 在 Text-to-Image、PAIBench-G、RBench、Cosmos HUE 与 Human World Bench 中，Cosmos 3 的生成器变体整体上优于或接近主要开放模型，并在若干开放模型比较中领先。
- 在 forward dynamics、inverse dynamics、RoboLab、LIBERO-10 和 PushT 动作模式实验中，mid-training
  或 joint action 训练通常带来更好的动作相关表现。
headline_metric: UniGenBench All (1170)
headline_value: 91.36
params_million: 64000.0
---

# Cosmos3OmnimodalWorldModelsForPhysicalAI

## Overview
Cosmos 3把语言、图像、视频、音频和动作放进统一的 omnimodal world model，用 Mixture-of-Transformers 同时承载理解与生成。它的核心动机是让 Physical AI 不再拼接 VLM、Video Generation Models、World Models、VLAs 和 WAMs，而是在同一表示空间里感知、推理、模拟和行动。模型通过 AR reasoner tower 处理理解和语言条件，通过 diffusion generator tower 生成视觉、音频和动作，并用 joint attention 让生成端受理解端条件约束。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 5 falsifiable claims |
| [concepts.md](logic/concepts.md) | 18 concepts |
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
