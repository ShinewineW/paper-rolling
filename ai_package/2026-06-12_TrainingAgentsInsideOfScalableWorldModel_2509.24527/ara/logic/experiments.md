# Experiments

## E1: 离线钻石挑战智能体评估
- **Verifies**: C1, C5
- **Setup**:
  - Model: Dreamer 4、WM+BC、VLA (Gemma 3)、BC、VPT
  - Hardware: 论文未将环境评估硬件作为核心设置报告
  - Dataset: VPT contractor dataset
  - System: Minecraft 离线钻石挑战，原始像素输入和低层 mouse 与 keyboard actions
- **Procedure**:
  1. 用固定离线数据训练各类行为克隆、VLA、WM+BC 与 imagination RL 智能体。
  2. 按 VPT evaluation protocol 从空 inventory 和随机 Minecraft 世界开始评估。
  3. 用线性 prompt sequence 引导智能体依次完成通向 Diamond 的里程碑任务。
  4. 记录每个 milestone item 的成功率，以及成功 episode 中到达该 item 的用时。
- **Metrics**: ['success rate', 'time to reach milestone item']
- **Expected outcome**: Dreamer 4 应在更难里程碑上取得更高成功率，并在成功时更快到达关键物品。
- **Baselines**: ['VPT (pretrained)', 'VPT (finetuned)', 'BC (notask)', 'WM+BC (notask)', 'VLA (Gemma 3)', 'WM+BC']
- **Dependencies**: ['Table 3', 'Table 7', 'Table 8', 'Figure 3', 'Figure 4']

## E2: Minecraft 世界模型人工交互评估
- **Verifies**: C2
- **Setup**:
  - Model: Dreamer 4、Oasis、Lucid-v1、MineWorld
  - Hardware: H100
  - Dataset: Minecraft VPT dataset
  - System: 人在世界模型内用 mouse 和 keyboard 完成交互任务
- **Procedure**:
  1. 训练 Dreamer 4 世界模型并与已有 Minecraft 世界模型比较。
  2. 由 human player 在世界模型中从任务起始帧开始执行任务。
  3. 任务覆盖挖坑、建墙、砍树、放置和乘船、看开再看回物体、与 crafting bench 和 furnace 交互等复杂机制。
  4. 比较可交互速度、上下文长度和任务完成情况。
- **Metrics**: ['FPS', 'context', 'success']
- **Expected outcome**: Dreamer 4 应在复杂交互任务成功数和上下文长度上优于先前 Minecraft 世界模型，同时保持实时交互。
- **Baselines**: ['MineWorld', 'Lucid-v1', 'Oasis (small)', 'Oasis (large)']
- **Dependencies**: ['Table 1', 'Figure 5', 'Figures 12 to 14']

## E3: 动作数据量与跨维度动作泛化
- **Verifies**: C3
- **Setup**:
  - Model: Dreamer 4
  - Hardware: 论文未将该实验硬件作为核心设置单独报告
  - Dataset: VPT dataset、Overworld split、Nether and End split
  - System: action-conditioned multi-step generation
- **Procedure**:
  1. 在全部视频上训练 Dreamer 4，但只给不同子集提供 action labels。
  2. 当 action labels 不可用时，dynamics model 使用 learned embedding 条件化。
  3. 在 holdout set 上比较 action-conditioned multi-step generations 与 ground truth videos。
  4. 进一步只在 Overworld 提供 actions，同时在 Nether and End 上评估从无标签视频场景中学到的 action conditioning。
- **Metrics**: ['PSNR', 'SSIM']
- **Expected outcome**: 较少配对动作数据应显著提升动作条件化质量，且只在 Overworld 给动作时应能泛化到 Nether 和 End。
- **Baselines**: ['no actions', 'all actions', 'Overworld-only action labels']
- **Dependencies**: ['Figure 7']

## E4: 模型目标与架构级联消融
- **Verifies**: C4
- **Setup**:
  - Model: Dreamer 4 world model variants
  - Hardware: H100
  - Dataset: Minecraft VPT holdout dataset
  - System: 无上下文视频生成与交互动作 rollout
- **Procedure**:
  1. 从朴素 diffusion forcing transformer baseline 开始。
  2. 逐步加入更少采样步、Shortcut model、X-Prediction、X-Loss、Ramp weight、交替 batch 长度、长上下文层频率调整、GQA、time factorized long context、register tokens 和更多 spatial tokens。
  3. 每个模型训练相同固定时长。
  4. 生成无上下文视频并切分为短片段，与 holdout dataset 计算分布距离，同时测量单卡推理速度。
- **Metrics**: ['Train stepseconds', 'FPS', 'FVD']
- **Expected outcome**: 完整级联设计应比朴素基线生成质量更好，并达到实时交互所需的推理速度方向。
- **Baselines**: ['Diffusion Forcing Transformer', 'Fewer sampling steps', 'Shortcut model', 'v-space prediction and losses variants']
- **Dependencies**: ['Table 2', 'Figure 8']
