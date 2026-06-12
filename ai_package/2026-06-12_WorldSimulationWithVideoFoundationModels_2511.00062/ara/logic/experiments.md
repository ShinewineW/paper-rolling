# Experiments

## E1: Cosmos-Predict2.5 训练与配置核验
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos-Predict2.5-2B 与 Cosmos-Predict2.5-14B
  - Hardware: 论文未在该实验段落单独指定硬件；训练效率另由基础设施实验报告
  - Dataset: 通用预训练视频与 Physical AI 领域数据
  - System: flow matching DiT，WAN2.1 VAE，Cosmos-Reason1 文本编码，Text2World、Image2World、Video2World 统一条件接口
- **Procedure**:
  1. 检查模型配置、预训练阶段与多输入模式设计。
  2. 核对 frame-replacement、条件掩码和 progressive training 是否支持图像、视频与文本条件。
  3. 用模型配置表与训练阶段表确认不同规模模型和训练任务覆盖。
- **Metrics**: ['模型配置项', '训练阶段覆盖', '任务模式覆盖']
- **Expected outcome**: 统一模型应覆盖多种输入模式，并具备不同规模配置。
- **Baselines**: ['Cosmos-Predict1']
- **Dependencies**: ['Table 3', 'Table 4']

## E2: VideoAlign 强化学习后训练评估
- **Verifies**: C2
- **Setup**:
  - Model: Cosmos-Predict2.5-2B pre-train 与 merged 版本，分别比较 RL 前后
  - Hardware: 论文未在该实验段落给出具体硬件型号
  - Dataset: PAI-Bench
  - System: VideoAlign 奖励模型，GRPO 风格组内优势归一化，扩散损失正则
- **Procedure**:
  1. 对每个输入条件生成多个候选视频。
  2. 使用 VideoAlign 计算文本对齐、运动质量与视觉质量奖励。
  3. 比较 RL 前后在 Text2World 与 Image2World 设置下的奖励变化。
  4. 用人工投票补充验证 RL 前后偏好方向。
- **Metrics**: ['Text Alignment', 'Motion Quality', 'Visual Quality', 'Sum', 'human voting']
- **Expected outcome**: RL 后奖励与人工偏好应整体优于 RL 前。
- **Baselines**: ['Predict2.5-2B [pre-train]', 'Predict2.5-2B [merged]']
- **Dependencies**: ['Table 6']

## E3: rCM 时间步蒸馏评估
- **Verifies**: C3
- **Setup**:
  - Model: Cosmos-Predict2.5-2B teacher 与 distilled
  - Hardware: 论文未在该实验段落给出具体硬件型号
  - Dataset: PAI-Bench-Predict-Text2World 与 PAI-Bench-Predict-Image2World
  - System: hybrid forward-reverse joint distillation，连续时间 consistency distillation 与 distribution matching distillation
- **Procedure**:
  1. 以 teacher 模型为参考训练 distilled 模型。
  2. 在 Text2World 与 Image2World 两个 PAI-Bench predict 基准上评测。
  3. 比较 Domain Score、Quality Score 与 Overall Score 的相对趋势。
- **Metrics**: ['Domain Score', 'Quality Score', 'Overall Score']
- **Expected outcome**: distilled 模型应接近 teacher，并在部分设置中保持或改善质量方向。
- **Baselines**: ['Cosmos-Predict2.5-2B [teacher]']
- **Dependencies**: ['Table 7', 'Table 8']

## E4: PAI-Bench Predict 自动基准评估
- **Verifies**: C4
- **Setup**:
  - Model: Cosmos-Predict2.5 pre-train 与 post-train，以及 Wan 系列基线
  - Hardware: 论文未在结果段落指定硬件
  - Dataset: PAI-Bench predict task
  - System: Text2World 与 Image2World 生成评测，Domain Score 来自 VQA，Quality Score 来自 VBench 风格指标
- **Procedure**:
  1. 在 PAI-Bench Text2World 上运行各模型并统计分数。
  2. 在 PAI-Bench Image2World 上运行各模型并统计分数。
  3. 比较 pre-trained、post-trained 与外部基线的 Domain Score、Quality Score 与 Overall Score。
- **Metrics**: ['Domain Score', 'Quality Score', 'Overall Score']
- **Expected outcome**: post-trained 模型应优于对应 pre-trained 版本，并在 Image2World 中处于领先方向。
- **Baselines**: ['Wan2.1-1.3B', 'Wan2.1-14B', 'Wan2.2-5B', 'Wan2.2-27B-A14B']
- **Dependencies**: ['Table 10', 'Table 11']

## E5: PAIBench-Transfer 多控制模态评估
- **Verifies**: C5
- **Setup**:
  - Model: Cosmos-Transfer2.5-2B 与 Cosmos-Transfer1-7B
  - Hardware: 论文未在该实验段落指定硬件
  - Dataset: PAIBench-Transfer
  - System: control-net style world translation，输入控制包含 blur、edge、depth、segmentation 与均匀多模态权重
- **Procedure**:
  1. 分别评估单控制模态模型。
  2. 评估四种控制模态均匀融合的多模态模型。
  3. 比较控制对齐指标与整体质量指标。
- **Metrics**: ['Blur SSIM', 'Edge F1', 'Depth si-RMSE', 'Mask mIoU', 'Quality Score']
- **Expected outcome**: Transfer2.5 应在整体质量和多项控制对齐方向上优于 Transfer1。
- **Baselines**: ['Cosmos-Transfer1-7B [Blur]', 'Cosmos-Transfer1-7B [Edge]', 'Cosmos-Transfer1-7B [Depth]', 'Cosmos-Transfer1-7B [Seg]', 'Cosmos-Transfer1-7B Uniform Weights']
- **Dependencies**: ['Table 12']

## E6: 真实机器人策略视觉增强实验
- **Verifies**: C6
- **Setup**:
  - Model: Cosmos-Transfer2.5-2B 用于生成增强观测，UNet-based Diffusion Policy 用于策略学习
  - Hardware: semi-humanoid 机器人平台，Kinova Gen3 arms，Robotiq 2F-140 gripper，Intel RealSense D455，Meta Quest 2 controllers
  - Dataset: 人工遥操作桌面双臂 pick-and-place 演示与多种测试场景
  - System: Real2Real 视觉增强，edge control 与 robot-pixel blur control，标准图像增强基线
- **Procedure**:
  1. 收集固定任务演示并训练基础策略。
  2. 用标准图像增强训练 baseline 策略。
  3. 用 Cosmos-Transfer2.5-2B 为每条演示生成语义视觉变体并训练 proposed 策略。
  4. 在 base 与未见物体、桌面、光照、干扰物、背景变化及组合场景中测试。
- **Metrics**: ['successes per trials', 'Total']
- **Expected outcome**: Proposed 策略应在总成功方向上明显优于 Base 与 Baseline。
- **Baselines**: ['Base', 'Baseline']
- **Dependencies**: ['Table 13']

## E7: 多视角驾驶仿真与检测评估
- **Verifies**: C7
- **Setup**:
  - Model: Predict2.5-2B/auto/mv 与 Transfer2.5-2B/auto/multiview
  - Hardware: 论文未在该实验段落指定硬件
  - Dataset: RDS-HQ-HL 与 RQS-HQ 多视角驾驶片段
  - System: 多视角 720p 世界生成，world scenario map 控制，LATR 车道检测与 BEVFormer 三维框检测评估
- **Procedure**:
  1. 训练多视角 Predict 与 Transfer 模型。
  2. 在生成多视角视频上评估视觉质量与跨相机一致性。
  3. 用车道检测和三维目标检测模型比较生成结果与人工标签。
- **Metrics**: ['FVD StyleGAN', 'FVD I3D', 'FID', 'TSE', 'CSE', 'LET-AP', 'LET-APL', 'LET-APH', 'F1', 'x-error (far)', 'Category Acc.']
- **Expected outcome**: Transfer2.5 与 Predict2.5 多视角模型应在视觉质量和检测遵循方向上优于上一代基线，并接近真实视频参考的部分一致性指标。
- **Baselines**: ['Predict1-7B-Sample-AV', 'Transfer1-7B-Sample-AV', 'Real Videos (Reference)']
- **Dependencies**: ['Table 14', 'Table 15']

## E8: Bridge 动作条件视频预测与注入方式消融
- **Verifies**: C8
- **Setup**:
  - Model: Cosmos-Predict2.5-2B/robot/action-cond
  - Hardware: 论文未在该实验段落指定硬件
  - Dataset: Bridge dataset
  - System: 单条件图像加动作序列生成未来帧，动作通过 action embedder MLP 注入 timestamp embeddings，并与 CrossAtten、ChannelConcat 消融比较
- **Procedure**:
  1. 在 Bridge 测试集上抽取官方测试 episode 并生成视频。
  2. 与 Cosmos-Predict1 动作条件基线对比生成质量。
  3. 固定模型族，比较 TimeEmbedding、CrossAtten 与 ChannelConcat 三种动作注入方式。
- **Metrics**: ['PSNR', 'SSIM', 'Latent L2', 'FVD']
- **Expected outcome**: Predict2.5 动作条件模型应优于上一代基线，TimeEmbedding 注入应优于其他注入方式。
- **Baselines**: ['Cosmos-Predict1-7B-Video2World- Sample-ActionCond', 'Cosmos-Predict2.5-2B/robot/action-cond with CrossAtten', 'Cosmos-Predict2.5-2B/robot/action-cond with ChannelConcat']
- **Dependencies**: ['Table 19', 'Table 20']
