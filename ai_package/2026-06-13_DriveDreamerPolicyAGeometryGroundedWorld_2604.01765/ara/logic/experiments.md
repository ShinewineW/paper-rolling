# Experiments

## E1: Navsim v1 与 Navsim v2 闭环规划基线对比
- **Verifies**: C1
- **Setup**:
  - Model: DriveDreamer-Policy，LLM 使用 Qwen3-VL-2B，depth generator 初始化自 PPD，video generator 初始化自 Wan-2.1-T2V-1.3B
  - Hardware: NVIDIA H20 GPUs
  - Dataset: Navsim navtrain/navtest
  - System: 统一 driving world-action model，输入 language instruction、multi-view RGB observations 与 current action，输出 depth、future video 与 future actions
- **Procedure**:
  1. 按标准 Navsim 协议在 navtrain 训练，在 navtest 评估。
  2. 在 Navsim v1 使用 PDMS 及其规划子指标对比 Vision-Based End-to-End Methods、Vision-Language-Action Methods 与 World-Model-Based Methods。
  3. 在 Navsim v2 使用 EPDMS 及扩展规划子指标进行同类对比。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'C↑$', 'EP↑', 'PDMS↑', 'DDC↑', 'TLC↑', 'LK↑ HC↑', 'EC↑', 'EPDMS↑']
- **Expected outcome**: DriveDreamer-Policy 的总体规划指标应高于论文列出的同类和跨类基线，并在若干安全与质量子指标上保持竞争力。
- **Baselines**: ['Human', 'TransFuser', 'UniAD', 'PARA-Drive', 'Diff usionDrive', 'AutoVLA', 'Recogdrive*', 'DriveVLA-W0', 'LAW', 'DrivingGPT', 'WoTE', 'Epona', 'FSDrive', 'PWM', 'Drivesuprim', 'ARTEMs', 'DriveVLA-Wo']
- **Dependencies**: ['Navsim', 'Qwen3-VL-2B', 'PPD', 'Wan-2.1-T2V-1.3B', 'AdamW']

## E2: Navsim 世界生成视频与深度评测
- **Verifies**: C2
- **Setup**:
  - Model: DriveDreamer-Policy，视频生成专家与深度生成专家由 LLM world embeddings 条件化
  - Hardware: NVIDIA H20 GPUs
  - Dataset: Navsim，视频以 recorded future RGB frames 为 ground truth，深度以 DA3 dense depth targets 为训练与评测目标
  - System: latent-space video generator 与 pixel-space depth generator 作为 modular experts
- **Procedure**:
  1. 对未来视频生成，按照 PWM 的设置报告感知质量和时序一致性指标。
  2. 由于 PWM 只支持 single-view generation，论文评估 single-view front quality 以便公平比较。
  3. 对深度预测，将 DriveDreamer-Policy 与 zero-shot PPD 以及 fine-tune PPD on Navsim 比较。
- **Metrics**: ['LPIPS↓', 'PSNR↑', 'FVD↓', 'AbsRel↓', '$δ_↑$', '$δ2↑}$', '$δ3↑$']
- **Expected outcome**: DriveDreamer-Policy 应在视频生成中取得更低感知距离和更好时序质量，并在深度预测中取得更低误差和更高阈值准确率。
- **Baselines**: ['PWM', 'PPD', 'PPD-Fintuned']
- **Dependencies**: ['Navsim', 'DA3', 'PPD', 'Wan-2.1-T2V-1.3B']

## E3: World Learning 对规划的消融
- **Verifies**: C3
- **Setup**:
  - Model: DriveDreamer-Policy 消融变体，包括 action-only、depth+action、video+action、depth+video+action
  - Hardware: NVIDIA H20 GPUs
  - Dataset: Navsim
  - System: 在相同训练预算下切换 depth 与 video world representation
- **Procedure**:
  1. 构造 Without World Learning 的 action-only 版本。
  2. 构造只加入 depth world learning 的 depth+action 版本。
  3. 构造只加入 video world learning 的 video+action 版本。
  4. 构造同时加入 depth 与 video world learning 的完整版本。
  5. 比较各变体的规划子指标与 PDMS。
- **Metrics**: ['NC↑', 'DAC↑', 'TTC↑', 'C↑$', 'EP↑', 'PDMS↑']
- **Expected outcome**: 任一 world learning 策略应优于从头训练的 action-only 设置，而 depth 与 video 联合策略应表现最好。
- **Baselines**: ['Without World Learning', 'With World Learning depth-only', 'With World Learning video-only']
- **Dependencies**: ['Navsim', 'DriveDreamer-Policy query groups', 'depth generator', 'video generator', 'action generator']

## E4: Depth Learning 对视频生成的消融
- **Verifies**: C4
- **Setup**:
  - Model: DriveDreamer-Policy 的 video-only 与 depth+video 变体
  - Hardware: NVIDIA H20 GPUs
  - Dataset: Navsim
  - System: 比较不使用 depth joint learning 的视频生成器与使用 depth joint learning 且 video queries 依赖 depth queries 的视频生成器
- **Procedure**:
  1. 训练 video-only 变体，使 video generator 只条件化于 backbone features。
  2. 训练 depth+video 变体，使 depth 联合训练并让 video queries 因果条件化于 depth queries。
  3. 在相同训练数据和计算预算下报告视频指标。
- **Metrics**: ['LPIPS↓', 'PSNR↑', 'FVD↓']
- **Expected outcome**: With Depth Learning 应取得更好的视频生成准确性和时序质量。
- **Baselines**: ['Without Depth Learning']
- **Dependencies**: ['Navsim', 'depth queries', 'video queries', 'video generator']

## E5: Number of Queries 查询预算消融
- **Verifies**: C5
- **Setup**:
  - Model: DriveDreamer-Policy 的默认查询配置与较小查询配置
  - Hardware: NVIDIA H20 GPUs
  - Dataset: Navsim
  - System: 比较 depth、video、action query tokens 数量变化对 depth、video 与 action 指标的影响
- **Procedure**:
  1. 使用较小 query budget 训练并评估深度、视频与规划指标。
  2. 使用默认 query budget 训练并评估相同指标。
  3. 比较两种 query budget 下的世界生成和规划表现。
- **Metrics**: ['AbsRel↓', '$\\delta _ { 1 } \\uparrow$', '$\\delta _ { 2 } \\uparrow$', '$\\delta _ { 3 } \\uparrow$', 'LPIPS↓', 'PSNR↑', 'FVD↓', 'NC↑', 'DAC↑', 'TTC↑', '$C↑$', 'EP↑', 'PDMS↑']
- **Expected outcome**: 更大的 query budget 应整体改善深度、视频与规划指标。
- **Baselines**: ['smaller budgets']
- **Dependencies**: ['Navsim', 'depth-query tokens', 'video-query tokens', 'action-query tokens']
