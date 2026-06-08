# Experiments

## E1: TransferBench单模态与多模态均匀权重配置对比实验
- **Verifies**: C1, C3, C5
- **Setup**:
  - Model: Cosmos-Transfer1-7B（各单模态变体及均匀权重多模态变体）
  - Hardware: NVIDIA H100 GPU（训练阶段，每分支1024块，训练2-4周）
  - Dataset: TransferBench（600样本：200 AgiBot World机器人操作 + 200 OpenDV驾驶 + 200 Ego-Exo-4D自我中心日常场景）
  - System: Cosmos-Transfer1-7B，生成5秒 1280x704p 24fps 视频（56K tokens）
- **Procedure**:
  1. 在TransferBench上分别运行单模态变体（[Vis]、[Edge]、[Depth]、[Seg]）
  2. 运行多模态均匀权重变体（全四模态各权重0.25）及逐一排除单模态的变体
  3. 对每个配置计算Blur SSIM、Edge F1、Depth si-RMSE、Mask mIoU、Diversity LPIPS、Quality Score
- **Metrics**: ['Blur SSIM（高=好）', 'Edge F1（高=好）', 'Depth si-RMSE（低=好）', 'Mask mIoU（高=好）', 'Diversity LPIPS（高=多样）', 'Quality Score（高=好，基于DOVER-technical）']
- **Expected outcome**: 多模态均匀权重配置在整体生成质量上高于单模态基线；密集结构模态（Vis/Edge）在对应对齐指标上最高但多样性最低
- **Baselines**: ['Cosmos-Transfer1-7B [Vis]', 'Cosmos-Transfer1-7B [Edge]', 'Cosmos-Transfer1-7B [Depth]', 'Cosmos-Transfer1-7B [Seg]']
- **Dependencies**: []

## E2: SalientObject算法时空控制图消融实验（前景/背景权重互换）
- **Verifies**: C2
- **Setup**:
  - Model: Cosmos-Transfer1-7B
  - Hardware: 未在该实验中特别说明
  - Dataset: TransferBench
  - System: VLM（GPT-4o）辅助分类前/背景掩码；GroundingDINO+SAM2提取分割掩码；对各模态权重（0、0.333、0.5）进行消融
- **Procedure**:
  1. 使用SalientObject算法，将VLM分类的前/背景掩码与不同模态权重组合
  2. 配置一：前景赋予Vis+Edge（各0.5），背景赋予Depth+Seg（各0.5）
  3. 配置二：前景赋予Depth+Seg（各0.5），背景赋予Vis+Edge（各0.5），即前后景互换
  4. 分别在TransferBench上计算前景（FG）和背景（BG）区域的各对齐指标及多样性指标
- **Metrics**: ['FG/BG Blur SSIM', 'FG/BG Edge F1', 'FG/BG Depth si-RSME', 'FG/BG Mask mIoU', 'FG/BG Diversity LPIPS', 'Quality Score']
- **Expected outcome**: 将密集模态移至某区域时该区域对应对齐指标提升、多样性下降；前后景互换导致相应指标的系统性变化
- **Baselines**: ['TransferBench均匀权重基线（E1各配置）']
- **Dependencies**: ['E1']

## E3: 机器人Sim2Real数据生成定量评估实验
- **Verifies**: C6
- **Setup**:
  - Model: Cosmos-Transfer1-7B（单模态变体及Setting1/Setting2多模态时空控制图配置）
  - Hardware: NVIDIA Omniverse + Isaac Lab（仿真数据生成）
  - Dataset: 20个机器人操作场景（基础厨房场景）x 6种文本提示 = 120个视频；任务含开/关橱柜及厨房物品拾取摆放
  - System: Setting1: 前景Edge+Vis（权重均为1），背景Seg（权重1）；Setting2: 前景Edge（权重1），背景Seg（权重1）
- **Procedure**:
  1. 使用NVIDIA Omniverse和Isaac Lab生成20个仿真机器人操作场景（含RGB、分割和深度图）
  2. 对每个场景用6种不同文本提示运行各Cosmos-Transfer1-7B配置生成视频（共120个）
  3. 计算全局及前景区域的对齐、多样性和质量指标，FG Mask mIoU仅计算机器人前景区域
- **Metrics**: ['Blur SSIM', 'Edge F1', 'Depth si-RMSE', 'Mask mIoU', 'FG Mask mIoU', 'Diversity LPIPS', 'Quality Score']
- **Expected outcome**: 时空控制图设置（Setting1/Setting2）在FG Mask mIoU和Quality Score上优于单模态基线，且保持较高多样性
- **Baselines**: ['Cosmos-Transfer1-7B [Vis]', 'Cosmos-Transfer1-7B [Edge]', 'Cosmos-Transfer1-7B [Depth]', 'Cosmos-Transfer1-7B [Seg]']
- **Dependencies**: ['E1']

## E4: 自动驾驶视频生成多模态控制定量评估实验
- **Verifies**: C7
- **Setup**:
  - Model: Cosmos-Transfer1-7B-Sample-AV（[HDMap]、[LiDAR]及融合变体）
  - Hardware: NVIDIA驾驶平台（数据采集）
  - Dataset: RDS-HQ（360小时高质量自动驾驶数据集，65K个20秒环视视频片段，含10 Hz LiDAR扫描）
  - System: HDMap+LiDAR融合：w_map=0.3，w_lidar=0.7；3D检测使用StreamPetr+Hydra-MDP（IoU阈值0.2）；车道分割使用Grounded SAM2；3D一致性用光度重投影误差（L1损失）评估
- **Procedure**:
  1. 分别用HDMap单模态、LiDAR单模态及HDMap+LiDAR融合配置生成自动驾驶视频
  2. 用StreamPetr+Hydra-MDP在生成视频上计算3D-Bbox mAP
  3. 用Grounded SAM2计算Lane mIoU
  4. 用光度重投影误差评估生成视频与LiDAR点云的3D一致性
- **Metrics**: ['3D-Bbox mAP（高=好）', 'Lane mIoU（高=好）', 'Reprojection Error（低=好）']
- **Expected outcome**: HDMap+LiDAR融合在Lane mIoU上超过LiDAR单模态，在Reprojection Error上优于HDMap单模态，实现综合最优
- **Baselines**: ['Cosmos-Transfer1-7B-Sample-AV [HDMap]', 'Cosmos-Transfer1-7B-Sample-AV [LiDAR]']
- **Dependencies**: []

## E5: GB200 NVL72实时推理扩展实验
- **Verifies**: C4
- **Setup**:
  - Model: Cosmos-Transfer1-7B
  - Hardware: NVIDIA GB200 NVL72机架（36个Grace CPU + 72个Blackwell GPU，每块B200具有192GB HBM，NVLink互联）
  - Dataset: 生成5秒720p视频（56K tokens）
  - System: 非注意力层采用纯数据并行；注意力层采用注意力头并行（all-to-all集合通信）；正向/负向条件去噪分组到不同GPU集合，共64块GPU参与注意力并行
- **Procedure**:
  1. 在1、4、8、16、32、64块B200 GPU配置下分别测量生成一个5秒视频的时间
  2. 分别记录纯扩散时间（Diffusion only）和端到端总时间（End-to-end）
  3. 分析从1到64 GPU的加速比
- **Metrics**: ['纯扩散时间（秒）', '端到端时间（秒）']
- **Expected outcome**: 随GPU数量增加，生成时间近线性缩短；64 GPU时端到端时间低于5秒，实现实时生成吞吐量
- **Baselines**: ['单GPU（1块B200）基线']
- **Dependencies**: []
