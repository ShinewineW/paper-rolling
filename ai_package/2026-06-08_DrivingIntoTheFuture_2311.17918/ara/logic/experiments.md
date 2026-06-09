# Experiments

## E1: 多视角视频生成质量对比实验
- **Verifies**: C1
- **Setup**:
  - Model: Drive-WM（含时序层与多视角层，初始化自 Stable Diffusion 权重）
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集（150 段视频，布局条件驱动，图像分辨率 384×192）
  - System: nuScenes 6 摄像头环视配置；FID/FVD 基于 900 段视频片段（6 视角×150 场景）计算
- **Procedure**:
  1. 以 nuScenes 训练集训练模型，在验证集布局条件下生成多视角图像或视频
  2. 计算生成图像的 FID，与多视角图像生成基线（BEVGen、BEVControl、MagicDrive）比较
  3. 计算生成视频的 FID 与 FVD，与单视角视频生成基线（DriveGAN、DriveDreamer）比较
- **Metrics**: ['FID（图像质量，越低越好）', 'FVD（视频质量，越低越好）']
- **Expected outcome**: Drive-WM 在 FID 上优于所有多视角图像生成基线；在 FID 和 FVD 上均优于单视角视频生成基线
- **Baselines**: ['BEVGen', 'BEVControl', 'MagicDrive', 'DriveGAN', 'DriveDreamer']
- **Dependencies**: []

## E2: 多视角视频生成可控性评估
- **Verifies**: C1, C3
- **Setup**:
  - Model: Drive-WM（布局条件：3D 框、HD 地图、BEV 分割）
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集
  - System: 预训练评估模型：BEVFormer（目标检测）、MapTR（在线地图构建）、CVT（BEV 分割）
- **Procedure**:
  1. 在生成的多视角视频上运行预训练 3D 目标检测器与在线地图预测模型
  2. 报告前景目标检测 mAPobj、地图预测 mAPmap、前景分割 mIoUfg、背景分割 mIoUbg
  3. 与 BEVGen、LayoutDiffusion、GLIGEN、BEVControl、MagicDrive 比较
- **Metrics**: ['mAPobj↑（目标可控性）', 'mAPmap↑（地图可控性）', 'mIoUfg↑（前景分割）', 'mIoUbg↑（背景分割）']
- **Expected outcome**: Drive-WM 在 mAPobj 和 mIoUbg 等多项可控性指标上优于所有基线
- **Baselines**: ['BEVGen', 'LayoutDiffusion', 'GLIGEN', 'BEVControl', 'MagicDrive']
- **Dependencies**: []

## E3: 模型组件消融实验（统一条件 / 时序视角层 / 分解生成）
- **Verifies**: C2, C3
- **Setup**:
  - Model: Drive-WM 各消融变体
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集（布局条件驱动）
  - System: nuScenes 6 摄像头；KPM 指标使用 LoFTR 匹配算法，每场景均匀采样 8 帧
- **Procedure**:
  1. 消融一（统一条件）：逐一移除布局条件或时序嵌入，对比 FID/FVD/KPM 变化
  2. 消融二（时序视角层）：比较「无时序无视角层」、「仅时序层」、「时序+视角层」三个变体
  3. 消融三（分解生成）：对比联合建模（无分解）与分解式生成的 KPM/FVD/FID
- **Metrics**: ['FID（图像质量）', 'FVD（视频质量）', 'KPM（多视角一致性，%）']
- **Expected outcome**: 布局条件和时序嵌入均正向贡献生成质量；分解式生成在 KPM 上大幅超越联合建模
- **Baselines**: ['仅时序嵌入（无布局条件）', '仅布局条件（无时序嵌入）', '仅时序层（无视角层）', '联合建模（无分解）']
- **Dependencies**: []

## E4: 树状规划性能评估
- **Verifies**: C4
- **Setup**:
  - Model: Drive-WM + VAD 规划器，动作条件化视频生成，树状规划含三个候选指令
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集，开环评估
  - System: VAD 采样「直行/左转/右转」三条候选轨迹；Drive-WM 为每条轨迹预测未来多视角视频
- **Procedure**:
  1. 从 VAD 按三种驾驶指令采样候选轨迹并提取对应动作序列
  2. Drive-WM 为每条候选轨迹生成未来多视角视频
  3. 图像奖励函数（地图奖励×目标奖励）选择最优轨迹
  4. 以 L2 距离与碰撞率评估，与 VAD（随机指令）及 VAD（真值指令）比较
- **Metrics**: ['L2 距离(m)（1s/2s/3s/平均）', '碰撞率(%)（1s/2s/3s/平均）']
- **Expected outcome**: 树状规划结果优于随机指令基线，接近真值指令上界
- **Baselines**: ['VAD（随机指令）', 'VAD（真值指令，上界）']
- **Dependencies**: ['E3']

## E5: 图像奖励函数组合消融实验
- **Verifies**: C4
- **Setup**:
  - Model: Drive-WM 树状规划，分别使用不同奖励子模块组合
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集
  - System: BEVFormer 目标检测器提供目标距离感知，MapTR 提供地图感知
- **Procedure**:
  1. 实验配置：无奖励（随机选择）、仅地图奖励、仅目标奖励、地图+目标联合奖励
  2. 在 nuScenes 验证集上以 L2 距离与碰撞率对比各配置的规划性能
- **Metrics**: ['L2 距离(m)（1s/2s/3s/平均）', '碰撞率(%)（1s/2s/3s/平均）']
- **Expected outcome**: 联合奖励在碰撞率指标上明显优于任一单一子奖励
- **Baselines**: ['无奖励（随机选择）', '仅地图奖励', '仅目标奖励']
- **Dependencies**: ['E4']

## E6: 域外自车偏移场景规划鲁棒性实验
- **Verifies**: C5
- **Setup**:
  - Model: Drive-WM 生成 OOD 数据用于微调 VAD 规划器
  - Hardware: A40 (48GB) GPU
  - Dataset: nuScenes 验证集，将自车横向位置偏移 0.5 米构造 OOD 场景
  - System: Drive-WM 在像素空间合成偏离车道的视角图像，并标注「驾回车道」的参考轨迹
- **Procedure**:
  1. 横向偏移自车位置 0.5 米，构造未见过的 OOD 输入
  2. 评估原始 VAD 规划器在 OOD 场景下的性能退化程度
  3. 以 Drive-WM 生成的 OOD 场景视频与恢复轨迹微调 VAD 规划器
  4. 重新评估微调后规划器在 OOD 场景上的 L2 距离与碰撞率
- **Metrics**: ['L2 距离(m)（1s/2s/3s/平均）', '碰撞率(%)（1s/2s/3s/平均）']
- **Expected outcome**: 世界模型数据微调后，OOD 场景的碰撞率与 L2 距离均显著低于未微调的 OOD 基线
- **Baselines**: ['正常场景 VAD（性能参考上界）', 'OOD 场景 VAD（无世界模型微调，退化下界）']
- **Dependencies**: ['E3']
