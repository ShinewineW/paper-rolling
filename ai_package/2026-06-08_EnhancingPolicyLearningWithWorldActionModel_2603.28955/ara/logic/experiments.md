# Experiments

## E1: CALVIN 验证集生成质量对比实验
- **Verifies**: C1, C5
- **Setup**:
  - Model: WAM（DreamerV2 + 逆动力学头，训练约 230K 步）对比 DreamerV2 基线（DreamingV2 [17]，训练约 2M 步）
  - Hardware: 论文未明确指定
  - Dataset: CALVIN 验证集，随机采样 100 条序列；世界模型训练数据约 512K 帧 CALVIN play 数据
  - System: CALVIN 基准环境 D，7-DoF Franka Emika Panda 机器人，64×64 RGB 静态相机与夹爪相机
- **Procedure**:
  1. 从 CALVIN 验证集随机采样 100 条序列
  2. 以各序列首帧真实观测和全程真实动作为条件，进行 50 步开环想象 rollout
  3. 分别使用 WAM 和 DreamerV2 生成预测帧序列
  4. 计算预测序列与真实序列之间的 PSNR、SSIM、LPIPS、FVD 指标，报告均值±标准差
- **Metrics**: ['PSNR（↑）', 'SSIM（↑）', 'LPIPS（↓）', 'FVD（↓）']
- **Expected outcome**: WAM 在 PSNR 与 SSIM 上高于基线，在 LPIPS 与 FVD 上低于基线
- **Baselines**: ['DreamerV2（由 Okada & Taniguchi 2022 [17] 实现的 DreamingV2）']
- **Dependencies**: []

## E2: CALVIN 8 任务行为克隆成功率评估
- **Verifies**: C2, C4
- **Setup**:
  - Model: DiffusionMLP 扩散策略，特征来自冻结 WAM 编码器（或 DreamerV2，即 DiWA 流程）
  - Hardware: 论文未明确指定
  - Dataset: CALVIN 环境 D 8 个操控任务，每任务 50 条专家演示用于 BC 训练，每任务 29 个保留初始配置用于评估
  - System: CALVIN 基准，7-DoF Franka Emika Panda，64×64 RGB 图像，CALVIN 内置任务检测器判断成功
- **Procedure**:
  1. 冻结 WAM（或 DreamerV2）编码器和 RSSM，从专家演示中提取 f_t 特征
  2. 以相同超参数训练 DiffusionMLP 策略（K=20 去噪步，动作时域 T_a=4，5000 轮，批大小 256）
  3. 在 29 个保留初始配置上滚动评估，每回合最多 72 步（最多 18 个决策点），由 CALVIN 内置检测器确认成功
  4. 对 8 个任务均报告任务成功率（%）及 8 任务均值
- **Metrics**: ['各任务成功率（%）', '8 任务平均成功率（%）']
- **Expected outcome**: WAM 特征训练的策略平均成功率高于 DiWA 基线，大部分单项任务均有提升
- **Baselines**: ['DiWA（使用 DreamerV2 特征的相同 DiffusionMLP 架构）']
- **Dependencies**: ['E1（需先完成世界模型训练）']

## E3: 冻结世界模型内 DPPO 精调成功率评估
- **Verifies**: C3, C4, C5
- **Setup**:
  - Model: BC 预训练的 DiffusionMLP 策略，使用 DPPO [16] 在冻结 WAM 或 DreamerV2 潜空间内精调
  - Hardware: 论文未明确指定
  - Dataset: CALVIN 8 个操控任务，使用冻结世界模型生成想象 rollout，无真实环境物理交互
  - System: CALVIN 基准，二值奖励分类器（精确率≥0.97，召回率 1.00）提供奖励信号
- **Procedure**:
  1. 针对两组 BC 预训练策略（WAM 特征 / DiWA 特征），分别在对应冻结世界模型内运行 800 轮 PPO 精调
  2. 每轮生成 50 条并行想象 rollout，扩散策略使用 10 步去噪配合 BC 正则化（α_BC=0.025）防止遗忘
  3. 每 25 轮评估一次策略成功率
  4. 额外记录「WAM/视觉基线匹配 DiWA 精调性能所需的环境步数」以衡量样本效率
  5. 报告 800 轮后 8 个任务的最终成功率（%）及均值
- **Metrics**: ['各任务最终成功率（%）', '8 任务平均成功率（%）', '匹配 DiWA 所需环境步数（WM 编码器路径与纯视觉路径）']
- **Expected outcome**: WAM 精调后平均成功率高于 DiWA，多个任务达到满分，WM 编码器路径所需环境步数显著少于纯视觉路径
- **Baselines**: ['DiWA（DreamerV2 内 DPPO 精调）', '纯视觉策略基线（Vision Env）']
- **Dependencies**: ['E2（BC 预训练策略作为 PPO 初始化）']
