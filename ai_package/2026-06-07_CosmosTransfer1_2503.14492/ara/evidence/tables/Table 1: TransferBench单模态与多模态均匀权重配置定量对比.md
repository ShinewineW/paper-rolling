# Table 1: TransferBench单模态与多模态均匀权重配置定量对比
- **Source**: Table 1
- **Caption**: "各Cosmos-Transfer1配置在TransferBench上的定量评估。单模态模型在对应对齐指标上最优，但整体质量低于均匀权重多模态模型；均匀权重多模态模型在Quality Score（8.54）和Depth si-RMSE上取得最优。"

| Model | Blur SSIM↑ | Edge F1↑ | Depth si-RMSE↓ | Mask mIoU↑ | Diversity LPIPS↑ | Quality Score↑ |
| --- | --- | --- | --- | --- | --- | --- |
| Cosmos-Transfer1-7B [Vis] | 0.96 | 0.16 | 0.49 | 0.72 | 0.19 | 5.94 |
| Cosmos-Transfer1-7B [Edge] | 0.77 | 0.28 | 0.53 | 0.71 | 0.28 | 5.48 |
| Cosmos-Transfer1-7B [Depth] | 0.71 | 0.14 | 0.49 | 0.70 | 0.39 | 6.51 |
| Cosmos-Transfer1-7B [Seg] | 0.66 | 0.11 | 0.75 | 0.68 | 0.42 | 6.30 |
| Cosmos-Transfer1-7B Uniform Weights, no Vis | 0.68 | 0.13 | 0.57 | 0.67 | 0.37 | 8.02 |
| Cosmos-Transfer1-7B Uniform Weights, no Edge | 0.81 | 0.10 | 0.53 | 0.66 | 0.31 | 7.68 |
| Cosmos-Transfer1-7B Uniform Weights, no Depth | 0.83 | 0.15 | 0.52 | 0.69 | 0.25 | 7.49 |
| Cosmos-Transfer1-7B Uniform Weights, no Seg | 0.84 | 0.15 | 0.43 | 0.70 | 0.23 | 7.83 |
| Cosmos-Transfer1-7B Uniform Weights | 0.87 | 0.20 | 0.47 | 0.72 | 0.22 | 8.54 |
