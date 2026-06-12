# Related Work

## R1: Ha and Schmidhuber, 2018
- **DOI**: 
- **Type**: world_model
- **Delta**:
  - What changed: 早期 world models 主要学习抽象潜在状态用于预测与规划；本文采用像素空间高保真视频预测路线，并扩展到文本、图像、视频、动作、相机和空间控制信号。
  - Why: 物理 AI 下游策略学习和仿真需要保留丰富视觉细节，像素级视频生成更适合生成可直接用于训练和评估的合成观测。
- **Claims affected**: ['C1', 'C8']
- **Adopted elements**: ['world dynamics prediction', 'planning-oriented simulator framing']

## R2: NVIDIA, 2025
- **DOI**: 
- **Type**: predecessor
- **Delta**:
  - What changed: Cosmos-Predict1 和 Cosmos-Transfer1 是本文直接前身；本文用 Cosmos-Predict2.5 和 Cosmos-Transfer2.5 改进数据过滤、统一模型架构、文本编码器、后训练和控制分支设计。
  - Why: 与上一代模型的对比构成本文主要改进证据，覆盖 PAI-Bench、Transfer、驾驶多视角和动作条件预测。
- **Claims affected**: ['C2', 'C4', 'C5', 'C7', 'C8']
- **Adopted elements**: ['Cosmos world model family', 'Physical AI benchmark framing', 'control-net style transfer']

## R3: Liu et al., 2025
- **DOI**: 
- **Type**: reward_model
- **Delta**:
  - What changed: 本文采用 VideoAlign 作为 VLM-based reward model，用于评估文本对齐、运动质量与视觉质量，并驱动 Cosmos-Predict2.5-2B 的 RL 后训练。
  - Why: 该奖励模型为视频世界生成提供可优化的偏好代理信号，使 RL 可以直接改善生成质量与对齐。
- **Claims affected**: ['C2']
- **Adopted elements**: ['VideoAlign reward', 'text alignment reward', 'motion quality reward', 'visual quality reward']

## R4: Guo et al., 2025
- **DOI**: 
- **Type**: rl_algorithm
- **Delta**:
  - What changed: 本文按 GRPO 思路在 rollout group 内归一化奖励来计算 advantage，并将其用于流式世界生成模型后训练。
  - Why: 组内归一化为多候选视频采样提供了稳定的相对优势信号，支撑 RL 后训练流程。
- **Claims affected**: ['C2']
- **Adopted elements**: ['GRPO-style grouped advantage normalization']

## R5: Zheng et al., 2025
- **DOI**: 
- **Type**: distillation
- **Delta**:
  - What changed: 本文采用 rCM hybrid forward-reverse joint distillation，将 consistency distillation 与 distribution matching distillation 结合，用于降低视频生成推理步数。
  - Why: 蒸馏目标是保持 teacher 质量的同时加速扩散式世界生成推理。
- **Claims affected**: ['C3']
- **Adopted elements**: ['rCM', 'continuous-time consistency distillation', 'distribution matching distillation']

## R6: Zhou et al., 2025
- **DOI**: 
- **Type**: benchmark
- **Delta**:
  - What changed: 本文使用 PAI-Bench 与 PAIBench-Transfer 评估 Physical AI 生成和控制转译能力。
  - Why: 这些基准为视频质量、物理 AI 领域任务和控制遵循提供统一评测框架。
- **Claims affected**: ['C4', 'C5']
- **Adopted elements**: ['PAI-Bench', 'PAIBench-Transfer', 'Domain Score', 'Quality Score']

## R7: Ren et al., 2025
- **DOI**: 
- **Type**: driving_and_policy_benchmark
- **Delta**:
  - What changed: 本文使用 RDS-HQ、RQS-HQ 相关多视角驾驶数据和评价协议，并在机器人策略学习中引用 Diffusion Policy 训练设置。
  - Why: 这些数据与协议支持评估多视角驾驶仿真和真实机器人策略泛化。
- **Claims affected**: ['C6', 'C7']
- **Adopted elements**: ['RDS-HQ', 'RQS-HQ', 'multi-view driving evaluation', 'Diffusion Policy setup']

## R8: Walke et al., 2023
- **DOI**: 
- **Type**: robot_dataset
- **Delta**:
  - What changed: 本文在 Bridge 数据集上训练和评估动作条件视频预测，并比较上一代动作条件世界模型。
  - Why: Bridge 提供带动作序列的机器人操作视频，适合验证动作条件未来帧生成。
- **Claims affected**: ['C8']
- **Adopted elements**: ['Bridge dataset', 'robot action-conditioned evaluation']
