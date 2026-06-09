# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/LIBERO 基准综合对比结果.md](tables/LIBERO 基准综合对比结果.md) | Table 2 | ['C1', 'C2'] | LIBERO 基准各子任务成功率对比，WorldVLA 在无预训练设定下超过同等离散动作模型基线 OpenVLA |
| [tables/动作模型消融研究结果.md](tables/动作模型消融研究结果.md) | Table 3 | ['C2', 'C4', 'C5', 'C7'] | 动作模型各组件消融：行 2 vs 行 1 显示世界模型提升动作性能；行 3 vs 行 1 显示默认遮蔽动作块生成导致 Spatial 和 Long 任务严重退化；行 4 vs 行 3 显示新注意力遮蔽的显著改善 |
| [tables/世界模型消融研究结果.md](tables/世界模型消融研究结果.md) | Table 4 | ['C3'] | 纯世界模型与动作世界模型视频生成质量对比，50 帧长序列上 WorldVLA 的 FVD 更低、PSNR 更高，体现动作模型对视觉理解的增益 |
| [tables/历史图像输入帧数消融结果.md](tables/历史图像输入帧数消融结果.md) | Table 5 | ['C1'] | 不同历史输入帧数下的成功率与推理帧率，2 帧配置在性能与效率间取得平衡 |
| [tables/世界模型预训练消融结果.md](tables/世界模型预训练消融结果.md) | Table 6 | ['C6'] | 使用世界模型预训练权重初始化动作模型可提升各子任务成功率，Long 任务提升最显著 |
