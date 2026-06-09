# LIBERO 基准综合对比结果
- **Source**: Table 2
- **Caption**: "LIBERO 基准各子任务成功率对比，WorldVLA 在无预训练设定下超过同等离散动作模型基线 OpenVLA"

| 模型 | 预训练 | Spatial | Object | Goal | Long | Average |
| --- | --- | --- | --- | --- | --- | --- |
| Diffusion Policy (Chi et al., 2023) |  | 78.3 | 92.5 | 68.3 | 50.5 | 72.4 |
| Octo (Team et al., 2024) | x√ | 78.9 | 85.7 | 84.6 | 51.1 | 75.1 |
| DiT Policy (Hou et al., 2024) | √ | 84.2 | 96.3 | 85.4 | 63.8 | 82.4 |
| Seer (Tian et al., 2024) | × | — | — | — | 78.7 | — |
| Seer (Tian et al., 2024) | √ | — | — | — | 87.7 | — |
| OpenVLA-OFT (Kim et al., 2025) | √ | 96.9 | 98.1 | 95.5 | 91.1 | 95.4 |
| UVA (Li et al., 2025) | × | — | — | — | 93.0 | — |
| OpenVLA (Kim et al., 2024) | √ | 84.7 | 88.4 | 79.2 | 53.7 | 76.5 |
| WorldVLA (256 * 256) | × | 85.6 | 89.0 | 82.6 | 59.0 | 79.1 |
| WorldVLA (512 * 512) | × | 87.6 | 96.2 | 83.4 | 60.0 | 81.8 |
