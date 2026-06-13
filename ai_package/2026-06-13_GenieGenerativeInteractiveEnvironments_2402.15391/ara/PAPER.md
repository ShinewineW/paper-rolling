---
key: '2402.15391'
title: GenieGenerativeInteractiveEnvironments
authors: []
year: 2024
venue: null
doi: arXiv:2402.15391
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- Generative Interactive Environment
- Latent Action Model
- Latent Action Space
- Video Tokenizer
- ST-Transformer
- Dynamics Model
- Action-Controllable Video Generation
- Controllability
claims_summary:
- Genie 将 latent action model、video tokenizer 与 dynamics model 组合起来，在没有 ground-truth
  action labels 或 text annotations 的训练条件下，仍能通过 learned latent action space 进行逐帧控制。
- 相比 token-input 版本，使用原始图像作为 latent action model 输入的 Pixel-input Genie 在两个评估环境中表现出更高的
  controllability。
- 在 tokenizer architecture ablation 中，ST-ViViT 相比 spatial-only ViT 与 C-ViViT 同时带来更好的
  video generation fidelity 与 controllability。
headline_metric: FVD
headline_value: 82.7
params_million: 10700.0
---

# GenieGenerativeInteractiveEnvironments

## Overview
Genie 把 video-only 数据学习成可逐帧交互的 generative interactive environment：先用 ST-ViViT tokenizer 把视频压成离散 tokens，再用 LAM 从相邻帧中无监督抽取 latent actions，最后由 MaskGIT dynamics model 根据历史 tokens 与动作预测下一帧。这样做的动机是绕开 Internet videos 缺少 ground-truth action labels 的限制，同时保留 world model 所需的 frame-level controllability。论文把这一框架扩展到 Platformers 与 Robotics，并展示 latent actions 还能用于从 unseen videos 中做行为模仿。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims |
| [concepts.md](logic/concepts.md) | 9 concepts |
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
