## learning_rate
- **Value**: 1×10^-4
- **Rationale**: AdamW优化器学习率，适用于全部训练设置
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## weight_decay
- **Value**: 0.01
- **Rationale**: AdamW权重衰减，防止过拟合
- **Search range**: None
- **Sensitivity**: low
- **Source**: Sec 4.1

## lr_schedule
- **Value**: cosine annealing
- **Rationale**: 余弦退火学习率调度，全部训练设置统一使用
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## gradient_clipping
- **Value**: 1.0
- **Rationale**: 梯度裁剪阈值，防止梯度爆炸
- **Search range**: None
- **Sensitivity**: low
- **Source**: Sec 4.1

## action_horizon
- **Value**: 32
- **Rationale**: 单次生成的动作块长度H
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 4.1

## video_temporal_downsampling
- **Value**: 4×
- **Rationale**: 视频帧时序下采样倍率，降低序列长度从而减小计算量
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## video_frames_per_chunk
- **Value**: 9
- **Rationale**: 时序下采样4×后每个动作块对应的视频帧数
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## training_steps_libero
- **Value**: 20k
- **Rationale**: LIBERO基准上所有模型的训练步数
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.2

## training_steps_robotwin_realworld
- **Value**: 30k
- **Rationale**: RoboTwin 2.0和真实世界任务上的训练步数
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.2

## noise_schedule
- **Value**: logit-normal over t
- **Rationale**: 遵循Wan2.2的设定，训练和推理均采用logit-normal分布采样去噪时间步
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## mixed_precision
- **Value**: 启用
- **Rationale**: 混合精度训练，加速训练并减少显存占用
- **Search range**: None
- **Sensitivity**: low
- **Source**: Sec 4.1

## idm_noise_augmentation_prob
- **Value**: 0.5
- **Rationale**: Fast-WAM-IDM变体中对真值视频token添加噪声增强的概率p
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## video_cotraining_weight
- **Value**: λ（论文未给出具体数值）
- **Rationale**: 联合训练目标中平衡动作损失与视频协同训练损失的权重超参数，见公式(9)
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 3.2, 公式(9)
