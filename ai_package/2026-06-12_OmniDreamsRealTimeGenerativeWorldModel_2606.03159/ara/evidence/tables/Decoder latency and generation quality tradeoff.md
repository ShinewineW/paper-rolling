# Decoder latency and generation quality tradeoff
- **Source**: Table 5
- **Caption**: "解码器延迟优化与生成质量之间存在权衡。"

| Training stage | FVD↓ | Temp.Sampson↓ | LET-AP ↑ | LET-APL ↑ | LET-APH ↑ | F1↑ | x-err. (far)↓ | Cat. Acc. 个 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Distilled (Original VAE) | 24.8 | 1.90 | 0.400 | 0.255 | 0.388 | 0.828 | 0.313 | 0.961 |
| Distilled (LightTAE decoder) | 45.4 | 2.02 | 0.376 | 0.237 | 0.365 | 0.813 | 0.352 | 0.952 |
