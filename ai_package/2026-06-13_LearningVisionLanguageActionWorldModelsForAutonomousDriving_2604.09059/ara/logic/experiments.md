# Experiments

## E1: nuScenes端到端轨迹规划主实验
- **Verifies**: C1
- **Setup**:
  - Model: VLA-World，基于Qwen2-VL-2B初始化
  - Hardware: 论文说明训练使用多块大显存GPU，补充材料说明推理也使用A100 GPU
  - Dataset: nuScenes
  - System: 按照ST-P3与UniAD协议评估L2误差和碰撞率
- **Procedure**:
  1. 收集nuScenes轨迹规划评测样本并沿用传统端到端方法、VLA方法和世界模型方法的协议。
  2. 将VLA-World与非自回归规划器、自回归VLA方法和世界模型基线比较。
  3. 分别报告ST-P3与UniAD指标下的L2误差和碰撞率。
- **Metrics**: ['L2 Error', 'Collision', 'ST-P3 metrics', 'UniAD metrics']
- **Expected outcome**: VLA-World应在平均轨迹误差与碰撞风险上低于主要自回归基线，并在长时域上更稳定。
- **Baselines**: ['ST-P3', 'VAD', 'UniAD', 'BEV-Planner', 'PreWorld', 'ELM', 'FeD', 'OccWorld', 'Doe-1', 'RDA-Driver', 'EMMA', 'OmniDrive', 'FSDrive']
- **Dependencies**: ['nuScenes', 'ST-P3 protocol', 'UniAD protocol', 'Qwen2-VL-2B']

## E2: nuScenes未来帧生成FID实验
- **Verifies**: C2
- **Setup**:
  - Model: VLA-World
  - Hardware: 论文说明训练使用多块大显存GPU
  - Dataset: nuScenes
  - System: 以生成未来帧的视觉质量为目标，使用Fréchet Inception Distance评估
- **Procedure**:
  1. 在nuScenes上生成短期未来帧。
  2. 将VLA-World与GAN、Diffusion和Autoregressive生成模型比较。
  3. 用FID衡量生成图像分布与真实图像分布的接近程度。
- **Metrics**: ['FID']
- **Expected outcome**: VLA-World应取得更低FID，表明未来帧视觉质量更好。
- **Baselines**: ['DriveGAN', 'DriveDreamer', 'Drive-WM', 'GenAD', 'GEM', 'Doe-1', 'FSDrive']
- **Dependencies**: ['nuScenes', 'Fréchet Inception Distance']

## E3: nuScenes动作预测实验
- **Verifies**: C3
- **Setup**:
  - Model: VLA-World，Qwen2-VL-2B及其nuScenes训练版本作为比较对象
  - Hardware: 论文说明训练使用多块大显存GPU
  - Dataset: nuScenes
  - System: 按横向与纵向动作类别计算F1分数
- **Procedure**:
  1. 在nuScenes动作预测设置下评估基础模型、训练后基础模型和VLA-World。
  2. 分别统计横向动作与纵向动作类别的F1表现。
  3. 比较VLA-World是否在每类动作上保持优势。
- **Metrics**: ['F1 score']
- **Expected outcome**: VLA-World应在横向和纵向动作类别上均高于比较模型。
- **Baselines**: ['Qwen2-VL-2B', 'Qwen2-VL-2B†']
- **Dependencies**: ['nuScenes', 'Qwen2-VL-2B']

## E4: 训练策略、管线组件与奖励设计消融
- **Verifies**: C4
- **Setup**:
  - Model: VLA-World及其消融变体
  - Hardware: 论文说明训练使用多块大显存GPU
  - Dataset: nuScenes
  - System: 使用ST-P3轨迹规划L2误差评估各组件贡献
- **Procedure**:
  1. 分别移除预训练、SFT、RL以评估训练阶段贡献。
  2. 分别移除感知、生成、推理以评估数据管线贡献。
  3. 分别移除预测、视觉、动作和轨迹奖励以评估RL奖励项贡献。
  4. 比较完整VLA-World与所有消融变体的L2误差方向。
- **Metrics**: ['L2 Error', 'ST-P3 metrics']
- **Expected outcome**: 完整VLA-World应优于去除训练阶段、管线组件或奖励项的变体。
- **Baselines**: ['w/o. P.T.', 'w/o. SFT', 'w/o. RL', 'w/o. Perception', 'w/o. Generation', 'w/o. Reasoning', 'w/o. R_pred', 'w/o. R_vis', 'w/o. R_act', 'w/o. R_traj']
- **Dependencies**: ['nuScenes', 'ST-P3 protocol', 'GRPO']

## E5: 补充分辨率、模型规模与混合训练消融
- **Verifies**: C5
- **Setup**:
  - Model: Qwen-VL系列骨干上的VLA-World变体
  - Hardware: 训练与推理使用A100 GPU
  - Dataset: nuScenes
  - System: 使用ST-P3轨迹规划L2误差比较输入分辨率、骨干规模和混合数据设置
- **Procedure**:
  1. 改变输入视图分辨率并比较轨迹规划L2误差。
  2. 在不同Qwen-VL系列骨干上比较轨迹规划L2误差。
  3. 移除混合任务数据并与完整训练设置比较。
- **Metrics**: ['L2 Error', 'ST-P3 metrics']
- **Expected outcome**: 更高视觉保真度、更大模型容量和混合任务训练应带来更好的平均规划表现。
- **Baselines**: ['lower input resolution', 'Qwen2-VL-2B', 'Qwen2.5-VL-3B', 'Qwen2-VL-7B', 'w/o. Mixed']
- **Dependencies**: ['nuScenes', 'Qwen-VL family', 'ST-P3 protocol']
