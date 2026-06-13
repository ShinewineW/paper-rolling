# Experiments

## E1: NAVSIM 主基准闭环规划与视频生成评测
- **Verifies**: C1
- **Setup**:
  - Model: Uni-World VLA，初始化自 PWM，使用 Show-o 与 MagVIT-v2 tokenizer，front-view camera 输入
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM test split；视频生成对比还涉及表中列出的 nuScenes、OpenDV 与 NAVSIM 设置
  - System: 单视角 camera-only 的 interleaved world modeling and planning 系统
- **Procedure**:
  1. 按官方 train/validation/test split 训练与选择 checkpoint。
  2. 在 NAVSIM test split 上评测闭环规划。
  3. 用 PDMS 及 NC、DAC、EP、TTC、Comf. 子指标比较规划性能。
  4. 用 FVD 比较未来视频序列生成质量。
- **Metrics**: ['PDMS', 'NC', 'DAC', 'EP', 'TTC', 'Comf.', 'FVD']
- **Expected outcome**: 相对多数传统端到端方法与世界模型方法，整体规划分数更高；视频生成质量保持竞争力。
- **Baselines**: ['VADv2-V8192', 'UniAD', 'TransFuser', 'ReCogDrive-IL', 'DiffusionDrive', 'DrivingGPT', 'Epona', 'ImagiDrive-A', 'DriveVLA-W0', 'SGDrive-IL', 'PWM', 'WoTE', 'ResWorld', 'WoVoGen', 'DriveDreamer', 'SVD', 'GenAD']
- **Dependencies**: ['NAVSIM', 'MagVIT-v2', 'Show-o', 'PWM', 'Depth Anything 3']

## E2: pretrain、future frames 与 depth conditioning 消融
- **Verifies**: C3
- **Setup**:
  - Model: Uni-World VLA ablation variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 逐步启用 pretrained checkpoint、future-frame modeling 与 depth conditioning 的同一系统
- **Procedure**:
  1. 构造不启用 pretrain、future frames、depth 的基础变体。
  2. 在基础上加入 pretrained checkpoint。
  3. 继续加入 future-frame generation 以辅助 trajectory planning。
  4. 进一步加入 image depth conditioning。
  5. 比较规划指标与未来帧生成指标的方向性变化。
- **Metrics**: ['NC', 'DAC', 'EP', 'TTC', 'Comf.', 'PDMS', 'FVD']
- **Expected outcome**: pretrain 与 future frames 提升规划表现；depth conditioning 进一步改善视频生成质量并补充规划收益。
- **Baselines**: ['无 pretrain、无 future frames、无 depth', '启用 pretrain 但无 future frames、无 depth', '启用 pretrain 与 future frames 但无 depth']
- **Dependencies**: ['NAVSIM', 'Depth Anything 3', 'CDE', 'DDE', 'cross-attention']

## E3: 替代 frame-action 生成 scheme 消融
- **Verifies**: C2
- **Setup**:
  - Model: 不使用 depth fusion 的 Uni-World VLA variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: 五种 frame-action 生成顺序在同一评测协议下比较
- **Procedure**:
  1. 实现 A-cross-frequency alternation、B-high-frequency actions-frames、C-hybrid dense-then-coarse、D-sliding action windows 与 E-aligned interleaving。
  2. 保持无 depth fusion 设置。
  3. 在相同 NAVSIM 评测协议下运行规划评测。
  4. 比较各 scheme 的规划指标方向性差异。
- **Metrics**: ['NC', 'DAC', 'EP', 'TTC', 'Comf.', 'PDMS']
- **Expected outcome**: 与评测频率对齐的严格 F→A 交错方案整体表现最好；密集动作或滑动窗口方案表现更弱。
- **Baselines**: ['A-cross-frequency alternation', 'B-high-frequency actions-frames', 'C-hybrid dense-then-coarse', 'D-sliding action windows']
- **Dependencies**: ['NAVSIM', 'Scheme E']

## E4: 历史视觉信息配置消融
- **Verifies**: C4
- **Setup**:
  - Model: 不使用 depth fusion 的 Uni-World VLA variants
  - Hardware: NVIDIA H20 GPUs
  - Dataset: NAVSIM
  - System: contextual tokens 与 dynamic tokens 的历史视觉输入配置比较
- **Procedure**:
  1. 使用 Context+Dynamic 的较长历史作为主配置。
  2. 缩短 Context+Dynamic 历史窗口进行比较。
  3. 仅使用 Context tokens 进行比较。
  4. 仅使用 Dynamic tokens 进行比较。
  5. 比较规划与视频生成指标的方向性差异。
- **Metrics**: ['NC', 'DAC', 'EP', 'TTC', 'Comf.', 'PDMS', 'FVD']
- **Expected outcome**: Context+Dynamic 的较长历史在整体规划和生成质量上更均衡；Dynamic Only 明显退化。
- **Baselines**: ['1.0 s Context+Dynamic', 'Context Only', 'Dynamic Only']
- **Dependencies**: ['NAVSIM', 'contextual tokens', 'dynamic tokens']
