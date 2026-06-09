# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/NAVSIM navtest闭环评测对比.md](tables/NAVSIM navtest闭环评测对比.md) | Table 1 | ['C2'] | 在NAVSIM navtest分割闭环指标上的方法对比。「C&L」表示同时使用相机和LiDAR输入。「V8192」表示8192个锚点。Hydra-MDP-V8192-W-EP额外使用规则评分器监督和加权置信度后处理。DiffusionDrive直接从人类示范学习，推理不含后处理。粗体和下划线分别表示最优和次优结果。 |
| [tables/从Transfuser到DiffusionDrive演进路线图.md](tables/从Transfuser到DiffusionDrive演进路线图.md) | Table 2 | ['C1', 'C2', 'C3'] | 从Transfuser到DiffusionDrive的演进路线图（NAVSIM navtest分割）。Transfuser_DP为替换MLP为原始DDIM扩散UNet的变体；Transfuser_TD为使用截断扩散策略的变体。Step Time为每个去噪步骤的运行时间；FPS和运行时间在NVIDIA 4090 GPU上测量；D为公式(3)定义的模式多样性分数。 |
| [tables/扩散解码器设计选择消融.md](tables/扩散解码器设计选择消融.md) | Table 3 | ['C4'] | 扩散解码器设计选择消融实验。「Cascade Decoder」表示堆叠2层级联扩散解码器。ID-1对应Table 2中的Transfuser_TD，使用条件UNet和自车查询交互。 |
| [tables/nuScenes开环评测对比.md](tables/nuScenes开环评测对比.md) | Table 7 | ['C5'] | nuScenes数据集开环评测对比。FPS在单块NVIDIA 4090 GPU上按SparseDrive评测流程测量，指标计算遵循ST-P3方法。 |
| [tables/驾驶先验对比（锚定高斯分布 vs 外推轨迹）.md](tables/驾驶先验对比（锚定高斯分布 vs 外推轨迹）.md) | Table 8 | ['C6'] | 驾驶先验对比实验。「Anchored Dist.」表示锚定高斯分布；「Extra. Traj.」表示基于当前状态的外推轨迹。Row-1（蓝色标注）为DiffusionDrive主论文基线。结果验证了多模式锚定高斯分布先验优于单一外推轨迹先验。 |
| [tables/去噪步数消融.md](tables/去噪步数消融.md) | Table 4 | ['C1'] | 去噪步数消融实验（NAVSIM navtest分割）。由于锚定高斯分布提供了合理的初始起点，1步去噪即可获得接近2步的规划质量。 |
