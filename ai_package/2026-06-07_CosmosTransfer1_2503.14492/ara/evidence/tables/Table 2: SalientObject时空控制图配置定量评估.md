# Table 2: SalientObject时空控制图配置定量评估
- **Source**: Table 2
- **Caption**: "不同时空控制权重分配策略在TransferBench上的定量评估，展示前景（FG）和背景（BG）区域的对齐、多样性及质量指标。前后景互换导致对应区域指标的系统性变化，验证了时空控制图的细粒度控制能力。"

| FG Vis | FG Edge | FG Depth | FG Seg | BG Vis | BG Edge | BG Depth | BG Seg | FG Blur SSIM↑ | BG Blur SSIM↑ | FG Edge F1↑ | BG Edge F1↑ | FG Depth si-RSME↓ | BG Depth si-RSME↓ | FG Mask mIoU↑ | BG Mask mIoU↑ | FG Diversity LPIPS↑ | BG Diversity LPIPS↑ | Quality Score↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 0.5 | 0 | 0 | 0 | 0 | 0.5 | 0.5 | 0.81 | 0.71 | 0.27 | 0.14 | 0.37 | 0.52 | 0.77 | 0.68 | 0.01 | 0.33 | 8.29 |
| 0 | 0 | 0.5 | 0.5 | 0.5 | 0.5 | 0 | 0 | 0.68 | 0.93 | 0.17 | 0.25 | 0.38 | 0.40 | 0.77 | 0.75 | 0.12 | 0.03 | 8.08 |
