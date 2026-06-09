# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/Table1a_生成质量对比.md](tables/Table1a_生成质量对比.md) | Table 1a | ['C1'] | nuScenes 上多视角视频生成质量对比。Drive-WM 在多视角图像（FID 12.99）和多视角视频（FID 15.8、FVD 122.7）均超越各类型最强基线。 |
| [tables/Table1b_生成可控性对比.md](tables/Table1b_生成可控性对比.md) | Table 1b | ['C1', 'C3'] | nuScenes 上生成可控性对比。Drive-WM 在 mAPobj 和 mIoUbg 上达到各方法最优。 |
| [tables/Table2a_统一条件消融.md](tables/Table2a_统一条件消融.md) | Table 2a | ['C3'] | 统一条件消融：布局条件对生成质量和多视角一致性影响最显著，时序嵌入进一步提升生成质量。 |
| [tables/Table2b_时序视角层消融.md](tables/Table2b_时序视角层消融.md) | Table 2b | ['C1'] | 时序层与多视角层消融：时序层大幅提升视频质量，视角层进一步改善多视角一致性（KPM）。 |
| [tables/Table2c_分解生成消融.md](tables/Table2c_分解生成消融.md) | Table 2c | ['C2'] | 分解式生成使 KPM 从 45.8% 大幅提升至 94.4%，视角间一致性显著改善，FVD 也略有改善。 |
| [tables/Table3_树状规划性能.md](tables/Table3_树状规划性能.md) | Table 3 | ['C4'] | nuScenes 开环规划性能对比。Drive-WM 树状规划明显优于随机指令基线，接近真值指令上界。 |
| [tables/Table5_域外规划性能.md](tables/Table5_域外规划性能.md) | Table 5 | ['C5'] | 域外场景（横向偏移 0.5m）规划性能。世界模型数据微调后碰撞率和 L2 显著低于未微调的 OOD 基线。 |
