---
key: '2603.16666'
title: 'Fast-WAM: Do World Action Models Need Test-time Future Imagination?'
authors: []
year: 2026
venue: null
doi: arXiv:2603.16666
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 世界行动模型 (World Action Models, WAMs)
- 想象后执行范式 (imagine-then-execute paradigm)
- 视频协同训练 (video co-training)
- 混合专家 Transformer 架构 (Mixture-of-Transformer, MoT)
- 流匹配目标 (Flow Matching Objective)
- 结构化注意力掩码 (structured attention mask)
- 潜在世界表征 (latent world representation)
claims_summary:
- 视频预测在WAMs中的主要价值在于训练期间改善世界表示,而非在测试时生成未来观测;去除视频协训练目标导致的性能下降远大于去除测试时未来想象所带来的下降
- Fast-WAM在LIBERO和RoboTwin基准上实现了有竞争力的结果,无需依赖其他WAMs使用的具身预训练,表明视频协训练具有强大的数据效率
- 通过在测试时跳过未来视频生成,Fast-WAM的推理延迟远低于imagine-then-execute WAMs(如Fast-WAM-IDM),速度差距超过4倍,支持实时机器人控制部署
headline_metric: success_rate
headline_value: 91.8
params_million: 6000.0
---

# Fast-WAM: Do World Action Models Need Test-time Future Imagination?

## Overview
Fast-WAM 是一种世界行动模型(WAM),在训练阶段保留视频联合训练,但在推理阶段完全跳过未来视频生成,实现单次前向传播的直接动作预测。其架构基于混合Transformer(MoT):以预训练视频扩散Transformer(DiT)作为世界编码骨干,叠加一个动作专家DiT,二者通过结构化注意力掩码共享注意力,同时阻断动作令牌对未来视频令牌的访问。训练时,视频联合目标驱动视频DiT学习物理动态的潜在表示;推理时,仅对第一帧干净潜变量做单次前向传播,由此获得的世界表示直接用于动作去噪,无需迭代视频采样。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 4 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
| [experiments.md](logic/experiments.md) | 3 experiments |

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
