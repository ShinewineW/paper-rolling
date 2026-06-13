# Experiments

## E1: 标准感知指标对比 visual–pose 与 RGB-only 世界模型
- **Verifies**: C1
- **Setup**:
  - Model: COMBAT: Pose 与 COMBAT: Non-Pose
  - Hardware: 论文所述 GPU 训练集群
  - Dataset: Tekken 3 gameplay held-out test set
  - System: 以真实 Player 1 action sequence 为条件生成 gameplay video，并与对应 ground-truth video 比较
- **Procedure**:
  1. 从测试集中抽取真实 Player 1 action sequence。
  2. 分别用 COMBAT: Pose 和 COMBAT: Non-Pose 生成对应视频。
  3. 将生成视频与动作来源对应的 ground-truth video 逐项比较。
  4. 报告 FD、FVD 和 LPIPS，所有指标方向均为越低越好。
- **Metrics**: ['FD', 'FVD', 'LPIPS']
- **Expected outcome**: visual–pose 版本应在视觉保真度和时间一致性相关指标上优于 RGB-only 版本。
- **Baselines**: ['COMBAT: Non-Pose']
- **Dependencies**: ['DCAE', 'Diffusion Transformer', 'FID', 'FVD', 'LPIPS']

## E2: 人工标注的 Player 2 emergent behavior checkpoint 评估
- **Verifies**: C2
- **Setup**:
  - Model: COMBAT training checkpoints
  - Hardware: 论文未为该评估单独指定硬件
  - Dataset: generated gameplay sequences 与 human gameplay
  - System: 人工标注 offensive actions，并比较生成 agent 与 original gameplay 的动作总量和拳脚比例
- **Procedure**:
  1. 在多个训练 checkpoint 生成 gameplay sequences。
  2. 人工标注 ground-truth 与 generated gameplay 中观察到的 offensive actions。
  3. 计算 Total Action Adherence 以比较总体攻击活动量。
  4. 计算 Action Ratio Consistency 以比较 punch-to-kick ratio。
  5. 按 checkpoint 汇总 TAA 和 ARC，并与 Ground Truth 对照。
- **Metrics**: ['TAA', 'ARC']
- **Expected outcome**: 训练进展应使生成 Player 2 的攻击活动量和动作比例从早期不稳定状态转向更接近 human gameplay 的模式，但后期可能出现一致性下降。
- **Baselines**: ['Ground Truth']
- **Dependencies**: ['human annotations', 'Total Action Adherence', 'Action Ratio Consistency']

## E3: 基于 health data 的行为一致性分析
- **Verifies**: C3
- **Setup**:
  - Model: COMBAT
  - Hardware: 论文未为该评估单独指定硬件
  - Dataset: generated rounds 与 ground-truth test rounds
  - System: 使用 in-game health data 比较动作后果与整局节奏
- **Procedure**:
  1. 从生成序列和 ground-truth 序列中提取 player health。
  2. 计算每帧 damage distribution，并用 Wasserstein distance 比较生成与真实分布。
  3. 计算归一化时间下的平均 health trajectory。
  4. 用 Mean Squared Error 比较生成 rounds 与 ground-truth rounds 的平均 health trajectory。
- **Metrics**: ['Wasserstein distance', 'MSE']
- **Expected outcome**: 更好的世界模型应产生更接近 ground-truth 的伤害分布，并呈现更真实的比赛节奏。
- **Baselines**: ['ground-truth test set']
- **Dependencies**: ['health annotations', 'Wasserstein distance', 'Mean Squared Error']

## E4: 蒸馏后的实时推理与质量权衡评估
- **Verifies**: C4
- **Setup**:
  - Model: CausVid DMD distilled COMBAT models
  - Hardware: single NVIDIA A100 GPU
  - Dataset: Tekken 3 gameplay latent world model setting
  - System: 使用 decoder distillation 与 step distillation 降低渲染和采样开销
- **Procedure**:
  1. 先对 VAE decoder 进行 student-teacher distillation。
  2. 再用 CausVid DMD 将 fully-trained DiT 蒸馏为 few-step sampler。
  3. 将蒸馏模型应用于 RGB-only 和 pose-augmented world models。
  4. 比较蒸馏后视觉质量、交互速度和行为响应性趋势。
- **Metrics**: ['visual quality', 'inference speed', 'agent responsiveness', 'attack frequency']
- **Expected outcome**: 蒸馏模型应保留可观视觉质量并提升交互速度，但可能牺牲部分行为保真。
- **Baselines**: ['full RGB-only model', 'fully-trained DiT']
- **Dependencies**: ['CausVid DMD', 'Distribution Matching Distillation', 'decoder distillation']
