# Experiments

## E1: NAVSIM v1 主结果比较
- **Verifies**: C1
- **Setup**:
  - Model: DriveWAM；对比 classical end-to-end pipelines、VLA-based policies、WA-based methods
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: NAVSIM v1
  - System: 单前视相机设置；按 NAVSIM 标准协议评测
- **Procedure**:
  1. 按论文实现训练 DriveWAM。
  2. 在 NAVSIM v1 测试协议下与表中方法比较。
  3. 报告规划相关指标与综合分数。
- **Metrics**: ['NC', 'DAC', 'TTC', 'C.', 'EP', 'PDMS']
- **Expected outcome**: DriveWAM 的综合规划表现应优于可比自动驾驶规划方法。
- **Baselines**: ['Human', 'UniAD', 'TransFuser', 'PARA-Drive', 'LAW', 'DiffusionDrive', 'WoTE', 'ReCogDrive', 'DriveVLA-W0', 'AutoVLA', 'DriveDreamer-Policy', 'DriveVLA-W0t', 'Epona', 'WorldDrive']
- **Dependencies**: ['NAVSIM', 'Wan2.2-TI2V-5B', 'Qwen3-VL-8B']

## E2: PhysicalAI-Autonomous-Vehicles 主结果比较
- **Verifies**: C2
- **Setup**:
  - Model: DriveWAM；对比 VaVAM 与 Alpamayo-1.5
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles 精选测试子集
  - System: 前视相机输入；单轨迹输出
- **Procedure**:
  1. 使用前视相机流和 ego-motion 标签训练 DriveWAM。
  2. 在精选测试子集上评测未来轨迹。
  3. 与论文列出的 WA-based 与 VLA-based 基线比较。
- **Metrics**: ['ADE@3s', 'FDE@3s', 'ADE@4s', 'FDE@4s']
- **Expected outcome**: DriveWAM 的位移误差应低于表中基线。
- **Baselines**: ['VaVAM', 'Alpamayo-1.5']
- **Dependencies**: ['PhysicalAI-Autonomous-Vehicles', 'Wan2.2-TI2V-5B', 'Qwen3-VL-8B']

## E3: scene-evolving guidance 消融
- **Verifies**: C3
- **Setup**:
  - Model: DriveWAM variants with fixed global prompt or scene-evolving guidance
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles
  - System: 相同训练设置下改变 guidance 条件
- **Procedure**:
  1. 在不同数据规模下训练对应变体。
  2. 将固定全局 prompt 与 scene-evolving guidance 的结果并列比较。
  3. 观察轨迹误差方向是否一致改善。
- **Metrics**: ['ADE@4s', 'FDE@4s']
- **Expected outcome**: 使用 scene-evolving guidance 的变体应获得更低轨迹误差。
- **Baselines**: ['fixed global prompt as text conditioning']
- **Dependencies**: ['Qwen3-VL-8B', 'PhysicalAI-Autonomous-Vehicles']

## E4: 训练数据规模扩展实验
- **Verifies**: C4
- **Setup**:
  - Model: DriveWAM with and without scene-evolving guidance
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles 的训练子集
  - System: 固定训练流程，改变训练 clips 规模
- **Procedure**:
  1. 从论文构建的训练子集中采样多个规模。
  2. 在固定训练流程下训练对应模型。
  3. 比较随着数据规模增加时轨迹误差的趋势。
- **Metrics**: ['ADE@4s', 'FDE@4s']
- **Expected outcome**: 训练数据增加时，误差应呈下降趋势。
- **Baselines**: ['较小训练子集', 'fixed global prompt variant']
- **Dependencies**: ['PhysicalAI-Autonomous-Vehicles', 'dataset curation pipeline']

## E5: 视频骨干初始化与联合视频监督消融
- **Verifies**: C5
- **Setup**:
  - Model: DriveWAM variants with different pretrained init and video supervision settings
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles
  - System: 相同优化设置下移除预训练初始化或视频监督
- **Procedure**:
  1. 训练从头开始的变体。
  2. 训练保留预训练初始化但移除视频监督的变体。
  3. 与完整配置比较轨迹误差。
- **Metrics**: ['ADE@4s', 'FDE@4s']
- **Expected outcome**: 完整配置应优于去除预训练初始化或去除视频监督的变体。
- **Baselines**: ['training from scratch', 'action-only adaptation without video supervision']
- **Dependencies**: ['Wan2.2-TI2V-5B', 'joint flow-matching objective']

## E6: KV memory 策略消融
- **Verifies**: C6
- **Setup**:
  - Model: DriveWAM with Full、FIFO、Selective KV memory
  - Hardware: 论文实现细节使用 NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles
  - System: 轨迹误差在常规 clips 上测量，缓存开销在长时 rollout 下 profile
- **Procedure**:
  1. 分别启用 Full KV、FIFO 和 selective KV memory。
  2. 在相同模型和缓存预算设定下测量轨迹误差。
  3. profile 长时 rollout 的 KV memory 与 attention GFLOPs。
- **Metrics**: ['ADE@4s', 'FDE@4s', 'Mem.(GB)', 'GFLOPs']
- **Expected outcome**: Selective 应比 FIFO 更接近 Full 的精度，并显著降低 Full 的资源开销。
- **Baselines**: ['Full', 'FIFO']
- **Dependencies**: ['FlowCache', 'selective KV memory']

## E7: per-chunk 推理成本分析
- **Verifies**: C7
- **Setup**:
  - Model: DriveWAM、DriveWAM*、Alpamayo-1.5
  - Hardware: single NVIDIA H20 GPU
  - Dataset: PhysicalAI-Autonomous-Vehicles
  - System: 按每个 chunk 分解 VLM guidance、Video Gen 与 Action stages
- **Procedure**:
  1. 在单卡上 profile 每个推理阶段耗时。
  2. 比较默认动作去噪与低步数动作去噪变体。
  3. 同时报告轨迹误差以检查效率与精度折中。
- **Metrics**: ['VLM (ms)', 'Video Gen (ms)', 'Action (ms)', 'ADE@4s', 'FDE@4s']
- **Expected outcome**: 低步数 DriveWAM 变体应保持相近误差并降低 action stage 耗时。
- **Baselines**: ['Alpamayo-1.5', 'DriveWAM default action denoising']
- **Dependencies**: ['Qwen3-VL-8B', 'Euler ODE solver', 'NVIDIA H20 GPU']
