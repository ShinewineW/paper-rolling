# Experiments

## E1: NAVSIM Navtest 闭环规划对比
- **Verifies**: C1
- **Setup**:
  - Model: DriveVA；Wan2.2-TI2V-5B 作为预训练 backbone
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM v1 Navtest
  - System: 闭环评估，指标包括 NC、DAC、TTC、Comf.、EP、PDMS
- **Procedure**:
  1. 在 NAVSIM v1 上训练 DriveVA。
  2. 在 NAVSIM Navtest 上按闭环指标评估。
  3. 与 Traditional End-to-End Methods 和 WorldModel Methods 对比。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: DriveVA 的闭环综合表现应高于列出的比较方法。
- **Baselines**: ['Constant Velocity Ego Status MLP', 'VADv2-V8192', 'UniAD', 'TransFuser', 'PARA-Drive', 'ReCogDrive-IL', 'DiffusionDrive', 'DrivingGPT', 'LAW', 'Epona', 'Resim', 'WoTE', 'DriveVLA-W0', 'PWM']
- **Dependencies**: ['Table 1']

## E2: nuScenes 与 Bench2Drive 零样本迁移对比
- **Verifies**: C2
- **Setup**:
  - Model: DriveVA；所有方法在 NAVSIM 训练后直接迁移
  - Hardware: NVIDIA H20 GPUs
  - Dataset: nuScenes validation split；Bench2Drive validation split
  - System: 无 target-domain fine-tuning 的端到端 motion planning 评估
- **Procedure**:
  1. 在 NAVSIM 上训练模型。
  2. 不进行目标域微调，直接在 nuScenes 与 Bench2Drive 上评估。
  3. 记录不同预测时域下的 L2 与 Collision 指标。
- **Metrics**: ['L2(m)↓', 'Collision (%)↓']
- **Expected outcome**: DriveVA 在两个目标域中应表现出更低误差与更低碰撞趋势。
- **Baselines**: ['DriveVLA-W0', 'PWM']
- **Dependencies**: ['Table 2']

## E3: nuScenes 规划性能与 finetune 方法对比
- **Verifies**: C2
- **Setup**:
  - Model: DriveVA；Camera* 输入；无 Auxiliary Supervision
  - Hardware: NVIDIA H20 GPUs
  - Dataset: nuScenes
  - System: 端到端 motion planning 评估，比较包含是否 nuScenes Finetune
- **Procedure**:
  1. 将 DriveVA 以零样本方式评估到 nuScenes。
  2. 收集已 finetune 或训练在 nuScenes 上的视觉规划方法结果。
  3. 按 L2 与 Collision Rate 对齐比较。
- **Metrics**: ['L2(m)↓', 'Collision Rate (%)↓']
- **Expected outcome**: DriveVA 即使无目标域 finetune，也应达到更低误差与更低碰撞趋势。
- **Baselines**: ['ST-P3', 'UniAD', 'OccNet', 'OccWorld', 'VAD-Tiny', 'VAD-Base', 'GenAD', 'Doe-1', 'Epona']
- **Dependencies**: ['Table 3']

## E4: DPVO 外部视频轨迹一致性验证
- **Verifies**: C3
- **Setup**:
  - Model: DriveVA
  - Hardware: 未在该实验段落单独说明
  - Dataset: NAVSIM；zero-shot nuScenes
  - System: 用 DPVO 从 ground-truth future videos 与 generated future videos 重建 camera trajectories，并做 2D similarity alignment
- **Procedure**:
  1. 在 ground-truth future video clip 和 DriveVA generated future video clip 上运行 DPVO。
  2. 将重建轨迹与对应 reference trajectory 进行 2D similarity transform 对齐。
  3. 计算 future horizon 上的 average L2 error。
- **Metrics**: ['Avg.L2 (4s)↓']
- **Expected outcome**: 重建轨迹与对应参考轨迹应保持低误差趋势，说明生成视频隐含运动与预测轨迹一致。
- **Baselines**: ['GT traj. vs. GT-video recon.', 'Pred. traj. vs.Pred.-video recon.']
- **Dependencies**: ['Table 4']

## E5: 关键设计消融
- **Verifies**: C4
- **Setup**:
  - Model: DriveVA variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 改变 Video Loss、CARLA Mix Training 与 Video Continuation 的闭环规划评估
- **Procedure**:
  1. 构造去除或保留关键模块的模型变体。
  2. 在相同 NAVSIM 规划指标上评估每个变体。
  3. 比较完整设置与去除模块后的变化方向。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: 保留 Video Loss、CARLA Mix Training 与 Video Continuation 的完整设置应更优；移除视频监督或 continuation 会降低表现。
- **Baselines**: ['去除 Video Loss 的变体', '去除 CARLA Mix Training 的变体', '去除 Video Continuation 的变体']
- **Dependencies**: ['Table 5']

## E6: 未来视频帧数消融
- **Verifies**: C4
- **Setup**:
  - Model: DriveVA variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 改变 future video frames，trajectory horizon 固定为 K=8
- **Procedure**:
  1. 分别设置不同 future video frames。
  2. 保持规划 horizon 设置一致。
  3. 在 NAVSIM 闭环指标上比较。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: 与动作块时间范围匹配的未来视频帧数应表现最好；过短会削弱视频 grounding，过长会累积漂移。
- **Baselines**: ['更短未来帧设置', '更长未来帧设置']
- **Dependencies**: ['Table 6']

## E7: 训练策略消融
- **Verifies**: C4, C5
- **Setup**:
  - Model: DriveVA training variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 比较 From Scratch、LoRA Fine-tune 与 Full Fine-tune
- **Procedure**:
  1. 使用不同训练策略适配模型。
  2. 保持评估指标一致。
  3. 比较闭环规划指标差异。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: Full Fine-tune 应优于 From Scratch 与 LoRA Fine-tune，说明端到端适配视频先验更有效。
- **Baselines**: ['From Scratch', 'LoRA Fine-tune']
- **Dependencies**: ['Table 7']

## E8: 采样步数消融
- **Verifies**: C4
- **Setup**:
  - Model: DriveVA sampling variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 改变 inference-time sampling steps
- **Procedure**:
  1. 在推理阶段使用不同 sampling steps。
  2. 保持模型与评估集一致。
  3. 比较闭环规划指标。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: 少量但非单步的采样应接近最佳表现，继续增加采样步数不带来明显收益。
- **Baselines**: ['更少 sampling steps', '更多 sampling steps']
- **Dependencies**: ['Table 8']

## E9: 模型规模与适配方式消融
- **Verifies**: C4, C5
- **Setup**:
  - Model: 5B LoRA；14B LoRA；5B Full Fine-tune
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 比较模型规模与微调方式对闭环规划指标的影响
- **Procedure**:
  1. 在不同 backbone scale 与 fine-tune strategy 下训练或适配。
  2. 在相同 NAVSIM 指标上评估。
  3. 比较 LoRA scale-up 与 full fine-tune 的趋势。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: 更大 LoRA 模型应比更小 LoRA 模型更强，但 full fine-tune 应明显更优。
- **Baselines**: ['5B LoRA', '14B LoRA']
- **Dependencies**: ['Table 9']

## E10: Causal Masking 与 Dual-Prediction 消融
- **Verifies**: C4
- **Setup**:
  - Model: DriveVA variants
  - Hardware: 未在附录该实验段落单独说明
  - Dataset: NAVSIM
  - System: 比较 causal mask、bidirectional、action only 与 default dual-prediction
- **Procedure**:
  1. 构造 future video tokens 不能 attend future action tokens 的 causal mask 变体。
  2. 构造只预测 future actions 的 Action Only 变体。
  3. 与默认 bidirectional 和 dual-prediction 设置比较。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'Comf.↑', 'EP↑', 'PDMS↑']
- **Expected outcome**: Bidirectional 与 Default dual-prediction 应优于 causal mask 与 action-only 变体。
- **Baselines**: ['Causal Mask', 'Action Only']
- **Dependencies**: ['Table 10']
