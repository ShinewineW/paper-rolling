# Related Work

## R1: Micheli et al. (2023)
- **DOI**: 
- **Type**: world_model_baseline
- **Delta**:
  - What changed: IRIS 使用 discrete autoencoder 将图像转为 tokens，并用 autoregressive transformer 组合时间序列；DIAMOND 改为直接在 image space 中使用 diffusion world model。
  - Why: 论文认为离散压缩可能丢失对 RL 关键的小视觉细节，因此用 DIAMOND 检验更忠实视觉生成是否能带来更好代理表现。
- **Claims affected**: ['C1', 'C4', 'C6']
- **Adopted elements**: ['作为 Atari world model baseline', '作为视觉细节比较对象', '作为 3D environments baseline']

## R2: Hafner et al. (2023)
- **DOI**: 
- **Type**: world_model_baseline
- **Delta**:
  - What changed: DreamerV3 是固定超参数、跨域有效的 latent world model；DIAMOND 用 diffusion model 生成 observation，并与 DreamerV3 比较代理表现、参数和 3D 视觉质量。
  - Why: 该对比用于说明 DIAMOND 的收益不是仅来自强化学习组件，而是与 world model 的视觉生成机制相关。
- **Claims affected**: ['C1', 'C5', 'C6']
- **Adopted elements**: ['作为 Atari baseline', '作为参数与训练时间比较对象', '作为 3D environments baseline']

## R3: Zhang et al. (2023)
- **DOI**: 
- **Type**: world_model_baseline
- **Delta**:
  - What changed: STORM 是近期 stochastic transformer based world model；DIAMOND 在同一 Atari benchmark 中作为 diffusion-based alternative 进行比较。
  - Why: STORM 代表强 world model baseline，能检验 DIAMOND 是否在完全 world model 训练代理范式中取得竞争力。
- **Claims affected**: ['C1']
- **Adopted elements**: ['作为 Atari world model baseline']

## R4: Karras et al. (2022)
- **DOI**: 
- **Type**: diffusion_design
- **Delta**:
  - What changed: EDM 提供 diffusion design space 与 network preconditioning；DIAMOND 采用 EDM 形式而非默认 DDPM，并将其条件化为 world model。
  - Why: 论文认为 EDM 的训练目标在高噪声区域提供更好的 score estimate，使少量 denoising steps 下的自回归生成更稳定。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['EDM formulation', 'network preconditioning', 'log-normal noise sampling']

## R5: Ho et al. (2020)
- **DOI**: 
- **Type**: diffusion_baseline
- **Delta**:
  - What changed: DDPM 是自然候选 diffusion variant；论文将其作为与 EDM 对比的设计选择 baseline。
  - Why: DDPM 在少量 denoising steps 下出现更强 compounding error，因此支持 DIAMOND 采用 EDM 的设计。
- **Claims affected**: ['C2']
- **Adopted elements**: ['作为 diffusion variant baseline']

## R6: Pearce and Zhu (2022)
- **DOI**: 
- **Type**: dataset_source
- **Delta**:
  - What changed: 论文使用 Pearce and Zhu 的 CS:GO gameplay 数据来训练静态数据上的 diffusion world model，并展示 interactive neural game engine 能力。
  - Why: 该数据提供更复杂的 3D 第一人称环境，用于检验 DIAMOND 是否能超出 Atari 像素控制任务。
- **Claims affected**: ['C6']
- **Adopted elements**: ['CS:GO gameplay dataset']
