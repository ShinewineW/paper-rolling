# Transfer 模型多控制配置评估
- **Source**: Table 12
- **Caption**: "不同单模态和均匀权重多模态 Transfer 配置的控制对齐与整体质量。"

| Model | Blur SSIM↑ | Edge F1↑ | Depth si-RMSE↓ | Mask mIoU↑ | Quality Score↑ |
| --- | --- | --- | --- | --- | --- |
| Cosmos-Transfer1-7B [Blur] | 0.89 | 0.20 | 0.66 | 0.73 | 6.56 |
| Cosmos-Transfer1-7B [Edge] | 0.77 | 0.38 | 0.85 | 0.73 | 6.76 |
| Cosmos-Transfer1-7B [Depth] | 0.67 | 0.15 | 0.76 | 0.71 | 6.89 |
| Cosmos-Transfer1-7B [Seg] | 0.62 | 0.11 | 1.13 | 0.70 | 6.02 |
| Cosmos-Transfer1-7B Uniform Weights | 0.82 | 0.26 | 0.70 | 0.74 | 9.24 |
| Cosmos-Transfer2.5-2B [Blur] | 0.90 | 0.26 | 0.59 | 0.75 | 9.75 |
| Cosmos-Transfer2.5-2B [Edge] | 0.79 | 0.49 | 0.76 | 0.75 | 8.73 |
| Cosmos-Transfer2.5-2B [Depth] | 0.71 | 0.19 | 0.70 | 0.73 | 8.85 |
| Cosmos-Transfer2.5-2B 3 [ | 0.68 | 0.14 | 1.02 | 0.71 | 8.81 |
| Cosmos-Transfer2.5-2B Uniform Weights | 0.87 | 0.41 | 0.67 | 0.76 | 9.31 |
