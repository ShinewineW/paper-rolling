# Bridge 动作条件注入方式消融
- **Source**: Table 20
- **Caption**: "Bridge 数据集上动作条件注入方式的消融结果。"

| Method | PSNR↑ | SSIM↑ | Latent L2↓ | FVD↓ |
| --- | --- | --- | --- | --- |
| Cosmos-Predict2.5-2B/robot/action-cond with TimeEmbedding (proposed) | 24.95 | 0.85 | 0.28 | 146 |
| Cosmos-Predict2.5-2B/robot/action-cond with CrossAtten | 24.41 | 0.84 | 0.28 | 159 |
| Cosmos-Predict2.5-2B/robot/action-cond with ChannelConcat | 23.11 | 0.78 | 0.35 | 267 |
