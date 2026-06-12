# Related Work

## R1: NVIDIA Cosmos world-foundation-model platform
- **DOI**: 
- **Type**: backbone
- **Delta**:
  - What changed: OmniDreams 从 Cosmos 系列视频基础模型出发，面向自动驾驶闭环仿真加入 action conditioning、world-scenario map control 与实时推理系统。
  - Why: 通用 physical-AI 世界基础模型提供视觉先验，但本文需要把它特化为可由策略动作驱动的闭环传感器生成器。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['Cosmos-Predict 2.5 backbone', 'rectified-flow objective', 'text encoder']

## R2: Diffusion Forcing
- **DOI**: 
- **Type**: training_method
- **Delta**:
  - What changed: OmniDreams 采用 Diffusion Forcing 将双向视频模型转换为因果自回归生成模型。
  - Why: 闭环仿真要求每次生成只能依赖过去观测与当前条件，不能使用未来帧信息。
- **Claims affected**: ['C2']
- **Adopted elements**: ['causal masking', 'per-token noise schedule', 'autoregressive factorization']

## R3: Self Forcing 与 DMD
- **DOI**: 
- **Type**: distillation
- **Delta**:
  - What changed: OmniDreams 采用 Self Forcing 的自 rollout 训练，并结合 DMD 的全视频分布匹配以减少 exposure bias。
  - Why: 长时程自回归视频容易累积误差，训练时用自身生成上下文能更贴近推理分布。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['self-rollout', 'rolling KV cache', 'Distribution Matching Distillation']

## R4: NVIDIA NuRec 与 3D Gaussian Splatting reconstruction
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: OmniDreams 与 NuRec 在同一 AlpaSim 闭环栈中比较；NuRec 作为重建式传感器仿真器基线。
  - Why: 重建式方法在原始采集走廊内保真，但对新视角、动态内容与未采集条件外推较弱，本文用生成式世界模型补足这些限制。
- **Claims affected**: ['C4']
- **Adopted elements**: ['NuRec closed-loop baseline', '3DGS reconstruction comparison']

## R5: AlpaSim 与 Alpamayo 1.5
- **DOI**: 
- **Type**: simulation_stack
- **Delta**:
  - What changed: OmniDreams 被接入 AlpaSim 微服务闭环系统，并与 Alpamayo 1.5 策略及其协议共同评估。
  - Why: 论文需要在真实闭环策略交互中验证传感器生成器是否会改变策略比较结论。
- **Claims affected**: ['C4', 'C5']
- **Adopted elements**: ['microservice simulator', 'closed-loop protocol', 'policy comparison setup']
