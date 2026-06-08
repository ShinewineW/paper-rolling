# Table 3: 机器人Sim2Real数据生成定量评估
- **Source**: Table 3
- **Caption**: "Cosmos-Transfer1在机器人Sim2Real数据生成任务上的定量评估（120个视频）。Setting2在Quality Score（10.42）和FG Mask mIoU（0.63）上均取得最优，两种时空控制图设置在前景保留和整体质量上均优于单模态基线。"

| Model | Blur SSIM↑ | Edge F1↑ | Depth si-RMSE↓ | Mask mIoU↑ | FG Mask mIoU↑ | Diversity LPIPS↑ | Quality Score↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cosmos-Transfer1-7B [Vis] | 0.95 | 0.19 | 0.82 | 0.65 | 0.56 | 0.20 | 9.11 |
| Cosmos-Transfer1-7B [Edge] | 0.63 | 0.40 | 1.01 | 0.63 | 0.57 | 0.36 | 7.70 |
| Cosmos-Transfer1-7B [Depth] | 0.66 | 0.13 | 0.84 | 0.59 | 0.57 | 0.43 | 9.17 |
| Cosmos-Transfer1-7B [Seg] | 0.47 | 0.10 | 1.34 | 0.55 | 0.54 | 0.60 | 9.29 |
| Cosmos-Transfer1-7B, Setting1 | 0.51 | 0.12 | 1.30 | 0.59 | 0.61 | 0.57 | 9.57 |
| Cosmos-Transfer1-7B, Setting2 | 0.50 | 0.14 | 1.41 | 0.60 | 0.63 | 0.58 | 10.42 |
