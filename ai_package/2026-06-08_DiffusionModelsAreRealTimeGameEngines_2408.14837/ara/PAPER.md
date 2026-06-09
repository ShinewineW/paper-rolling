---
key: '2408.14837'
title: Diffusion Models Are Real-Time Game Engines
authors: []
year: 2024
venue: null
doi: arXiv:2408.14837
ara_version: '1.0'
schema_version: '1.0'
domain: deep learning
keywords:
- 交互式世界仿真
- 教师强迫训练目标
- 自回归漂移
- 噪声增强
- 速度参数化扩散损失
- 潜在解码器微调
- 选择性无分类器引导
claims_summary:
- GameNGen 是首个完全由神经模型驱动的游戏引擎，能够在单张 TPU-v5 上以 20 FPS 对复杂游戏 DOOM 进行实时交互式仿真，并在长时轨迹上保持与原始游戏相当的视觉质量
- 在训练时对历史上下文帧添加可变量高斯噪声（噪声增强），能有效阻止自回归生成中因教师强制与推理分布偏移导致的质量退化，是长轨迹稳定仿真的必要条件
- GameNGen 仅需 4 个 DDIM 采样步骤即可达到与 20 步或更多步骤相当的仿真质量，从而在单张 TPU-v5 上实现 20 FPS 实时推理；单步蒸馏模型可进一步提升至
  50 FPS，但带来轻微质量损耗
headline_metric: PSNR
headline_value: 29.43
params_million: 860.0
---

# Diffusion Models Are Real-Time Game Engines

## Overview
GameNGen 是首个完全由神经网络驱动的游戏引擎，基于 Stable Diffusion v1.4 改造，能够在单块 TPU 上以每秒 20 帧实时仿真复杂游戏 DOOM。训练分两阶段：先用强化学习代理采集大规模游戏轨迹，再训练扩散模型根据过去帧与动作序列预测下一帧。通过向上下文帧注入可控高斯噪声缓解自回归漂移，通过微调潜变量解码器提升视觉细节保真度。系统在多分钟游玩会话中保持稳定，人类评分者几乎无法区分仿真片段与真实游戏片段。

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims |
| [concepts.md](logic/concepts.md) | 7 concepts |
| [experiments.md](logic/experiments.md) | 7 experiments |

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
