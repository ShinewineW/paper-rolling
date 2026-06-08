# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/Table 1: TransferBench单模态与多模态均匀权重配置定量对比.md](tables/Table 1: TransferBench单模态与多模态均匀权重配置定量对比.md) | Table 1 | ['C1', 'C5'] | 各Cosmos-Transfer1配置在TransferBench上的定量评估。单模态模型在对应对齐指标上最优，但整体质量低于均匀权重多模态模型；均匀权重多模态模型在Quality Score（8.54）和Depth si-RMSE上取得最优。 |
| [tables/Table 2: SalientObject时空控制图配置定量评估.md](tables/Table 2: SalientObject时空控制图配置定量评估.md) | Table 2 | ['C2'] | 不同时空控制权重分配策略在TransferBench上的定量评估，展示前景（FG）和背景（BG）区域的对齐、多样性及质量指标。前后景互换导致对应区域指标的系统性变化，验证了时空控制图的细粒度控制能力。 |
| [tables/Table 3: 机器人Sim2Real数据生成定量评估.md](tables/Table 3: 机器人Sim2Real数据生成定量评估.md) | Table 3 | ['C6'] | Cosmos-Transfer1在机器人Sim2Real数据生成任务上的定量评估（120个视频）。Setting2在Quality Score（10.42）和FG Mask mIoU（0.63）上均取得最优，两种时空控制图设置在前景保留和整体质量上均优于单模态基线。 |
| [tables/Table 4: 自动驾驶视频生成定量评估.md](tables/Table 4: 自动驾驶视频生成定量评估.md) | Table 4 | ['C7'] | Cosmos-Transfer1-7B-Sample-AV在自动驾驶视频生成任务上的定量对比。融合模型在Lane mIoU（51.55）上优于两个单模态基线，在重投影误差上优于HDMap单模态，实现均衡的综合性能。 |
| [tables/Table 5: GB200 NVL72不同GPU数量下的生成时间.md](tables/Table 5: GB200 NVL72不同GPU数量下的生成时间.md) | Table 5 | ['C4'] | Cosmos-Transfer1-7B在不同并行GPU数量下生成一个5秒视频的计算时间。64块B200 GPU时端到端时间为4.2秒，低于5秒实现实时吞吐量；从1到64 GPU约实现40倍加速（纯扩散时间：141.0s→3.5s）。 |
