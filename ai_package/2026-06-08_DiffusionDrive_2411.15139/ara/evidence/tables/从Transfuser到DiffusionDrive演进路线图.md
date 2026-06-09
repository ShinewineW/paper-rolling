# 从Transfuser到DiffusionDrive演进路线图
- **Source**: Table 2
- **Caption**: "从Transfuser到DiffusionDrive的演进路线图（NAVSIM navtest分割）。Transfuser_DP为替换MLP为原始DDIM扩散UNet的变体；Transfuser_TD为使用截断扩散策略的变体。Step Time为每个去噪步骤的运行时间；FPS和运行时间在NVIDIA 4090 GPU上测量；D为公式(3)定义的模式多样性分数。"

| Method | NC↑ | DAC↑ | TTC↑ | Comf.↑ | EP↑ | PDMS↑ | Arch. | Step Time↓ | Steps | Total↓ | D↑ | Para. | FPS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Transfuser | 97.7 | 92.8 | 92.8 | 100 | 79.2 | 84.0 | MLP | 0.2ms | 1 | 0.2ms | 0% | 56M | 60 |
| Transfuser_DP | 97.5 | 93.7 | 92.7 | 100 | 79.4 | 84.6+0.6 | UNet | 6.5ms | 20 | 130.0ms | 11% | 101M | 7 |
| Transfuser_TD | 97.9 | 94.2 | 93.9 | 100 | 80.2 | 85.7+1.7 | UNet | 6.9ms | 2 | 13.8ms | 70% | 102M | 27 |
| DiffusionDrive | 98.2 | 96.2 | 94.7 | 100 | 82.2 | 88.1+4.1 | Dec. | 3.8ms | 2 | 7.6ms | 74% | 60M | 45 |
