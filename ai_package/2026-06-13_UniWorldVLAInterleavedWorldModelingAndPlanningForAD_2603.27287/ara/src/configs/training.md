## 初始化检查点
- **Value**: 从 Policy World Model 初始化，PWM 本身由 Show-o 微调而来
- **Rationale**: 利用已有统一世界模型与多模态 LLM 能力作为起点，论文消融显示预训练是关键增益来源。
- **Search range**: 预训练初始化或无预训练初始化
- **Sensitivity**: 高；无预训练时规划质量明显下降。
- **Source**: Sec 4.1 Implementation details; Sec 4.3 Table 3

## 优化器
- **Value**: AdamW
- **Rationale**: 论文在实现细节中明确采用 AdamW 训练模型。
- **Search range**: 论文未报告替代优化器。
- **Sensitivity**: 未知；论文未做优化器消融。
- **Source**: Sec 4.1 Implementation details

## 学习率调度
- **Value**: cosine annealing schedule
- **Rationale**: 用于完整训练过程中的学习率变化。
- **Search range**: 论文未报告替代调度。
- **Sensitivity**: 未知；论文未做调度消融。
- **Source**: Sec 4.1 Implementation details

## Stage 1 训练设置
- **Value**: 训练 CDE 和 DDE，5 epochs，学习率 $3 \times 1 0 ^ { - 5 }$，action-free video prediction，10 Hz 内 1 second 未来帧监督，冻结 pre-trained foundation model，其余可训练参数解冻
- **Rationale**: 先稳定训练深度特征提取模块，同时保留预训练 foundation model 的表征能力。
- **Search range**: 论文仅报告该阶段配置。
- **Sensitivity**: 中到高；该阶段服务于深度融合收敛稳定性，但论文未单独消融 epoch 或学习率。
- **Source**: Sec 4.1 Stage 1

## Stage 2 训练设置
- **Value**: 冻结预训练 CDE 和 DDE，解冻 fusion module 和 foundation model，采用 Scheme E，16 epochs，学习率 $2 \times 1 0 ^ { - 5 }$
- **Rationale**: 在保持深度特征提取能力的同时，让融合模块和 foundation model 协同学习未来帧与轨迹监督。
- **Search range**: 论文报告 Scheme A 到 Scheme E 的生成方案消融；Stage 2 epoch 与学习率未报告替代值。
- **Sensitivity**: 高；Scheme E 在生成方案消融中表现最好，说明监督频率与生成顺序敏感。
- **Source**: Sec 4.1 Stage 2; Sec 4.3 Table 4

## 完整微调轮数与检查点选择
- **Value**: 在 NAVSIM 上 fine-tune 30 epochs，按 PDMS 选择最佳 checkpoint，最佳出现在 epoch 16
- **Rationale**: 以闭环规划指标选择模型，避免只按视频生成质量或训练损失选择。
- **Search range**: 训练到 30 epochs，选择 epoch 16 checkpoint。
- **Sensitivity**: 中；论文说明最佳 checkpoint 基于 PDMS，但未报告不同 epoch 曲线。
- **Source**: Sec 4.1 Implementation details

## 批量大小
- **Value**: training batch size of 3
- **Rationale**: 论文在 32 NVIDIA H20 GPUs 设置下使用该 batch size。
- **Search range**: 论文未报告其他 batch size。
- **Sensitivity**: 未知；论文未做 batch size 消融。
- **Source**: Sec 4.1 Implementation details

## 历史与预测时间配置
- **Value**: 2 seconds historical observations，预测 8 future frames 和对应 waypoints，4-second horizon，固定 0.5 s interval
- **Rationale**: 用历史视觉与状态信息自回归生成未来世界状态和轨迹，和 NAVSIM 2 Hz 评测协议对齐。
- **Search range**: 历史信息消融包含 2.0 s Context+Dynamic、1.0 s Context+Dynamic、Context Only、Dynamic Only。
- **Sensitivity**: 高；历史信息消融显示 Context+Dynamic 的 2.0 s 配置整体最好。
- **Source**: Sec 4.1 Dataset; Sec 4.1 Implementation details; Sec 4.3 Table 5

## 输入相机设置
- **Value**: Only the front-view camera is used as input
- **Rationale**: 以 single-view camera 输入验证方法在较少传感器下的规划与生成能力。
- **Search range**: 主方法使用 Front/single-view camera；对比方法含 C、SC、C&L。
- **Sensitivity**: 中；论文强调 ResWorld 使用 camera + LiDAR，而本文 single-view camera-only 仍取得较好综合表现。
- **Source**: Sec 4.1 Implementation details; Table 1

## 训练目标
- **Value**: 联合监督 future visual token generation 和 trajectory prediction；视觉使用 Dynamic Focal Loss，轨迹使用 L1 loss，最终为加权和
- **Rationale**: 视觉分支强调动态区域，动作分支回归未来 ego positions，使生成与规划共同优化。
- **Search range**: 权重为 $\lambda _ { 1 }$ 与 $\lambda _ { 2 }$，论文未给具体数值。
- **Sensitivity**: 中；论文说明 Dynamic Focal Loss 用于缓解相邻帧 token 大量不变的问题，但未消融损失权重。
- **Source**: Sec 3 Training objectives
