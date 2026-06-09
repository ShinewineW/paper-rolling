# Heuristics

## H1: 锚点数量 N_anchor=20，由训练集轨迹K-Means聚类获得
- **Rationale**: 以远少于VADv2(8192个)的锚点数覆盖多模态驾驶动作空间，大幅降低计算开销同时保持覆盖度
- **Sensitivity**: 中等；Table 6消融显示 N_infer=10 时 PDMS=84.9，N_infer=20 时 PDMS=88.1，N_infer=40 时 PDMS=88.2，边际收益递减
- **Bounds**: 训练固定使用20个锚点；推理时 N_infer 可灵活调整，消融范围10至40
- **Code ref**: [N_anchor]
- **Source**: Section 3.3, Section 4.2, Table 6

## H2: 截断扩散时间步比例 T_trunc=50/1000，即从完整扩散调度中截取前50步用于训练期加噪
- **Rationale**: 仅向锚点添加少量噪声以构建锚定高斯分布；初始分布更靠近目标驾驶策略，从而大幅减少所需去噪步数
- **Sensitivity**: 高；截断比例直接决定锚定噪声强度与初始分布偏移量，过大趋近vanilla扩散，过小则去噪空间不足
- **Bounds**: 论文固定使用50步截断；对应推理步数缩减至2步
- **Code ref**: [T_trunc]
- **Source**: Section 3.3, Section 4.2

## H3: 推理时去噪步数为2步
- **Rationale**: 截断扩散策略使初始噪声点已靠近目标分布，2步去噪即可达到高质量，保障45 FPS实时速度
- **Sensitivity**: 低；Table 4显示1步 PDMS=87.9，2步=88.1，3步=88.1，1步到2步有小幅提升后收敛
- **Bounds**: 消融范围1至3步，2步为推荐配置
- **Code ref**: [denoising_steps]
- **Source**: Section 3.3, Section 4.5, Table 4

## H4: 级联扩散解码器堆叠2层，参数跨去噪步骤共享
- **Rationale**: 多层级联在每个去噪步骤内迭代细化轨迹，增强对BEV/PV场景上下文的层次化利用；参数共享控制模型规模
- **Sensitivity**: 中等；Table 5显示1层 PDMS=87.4，2层=88.1，4层=88.2，继续增加层数收益趋于饱和且参数量上升至65M
- **Bounds**: 消融范围1至4层，2层配置参数量为60M
- **Code ref**: [cascade_stages]
- **Source**: Section 4.5, Table 5

## H5: 训练配置：AdamW优化器，学习率6×10^-4，共100个epoch，总批量大小512，使用8块NVIDIA 4090 GPU
- **Rationale**: 沿用Transfuser训练配方以保证公平比较，直接从头训练(NAVSIM实验，无需感知预训练初始化)
- **Sensitivity**: 未在论文中对学习率或epoch进行消融
- **Bounds**: 学习率6×10^-4；epoch=100；batch size=512
- **Code ref**: [lr, num_epochs, batch_size]
- **Source**: Section 4.2
