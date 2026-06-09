# 从Transfuser到DiffusionDrive演进路线图
- **Source**: Table 2
- **Caption**: "在NAVSIM navtest split上从Transfuser到DiffusionDrive的路线图。TransfuserDP表示使用原始DDIM扩散策略的Transfuser。TransfuserTD表示使用截断扩散策略的Transfuser。Step Time为每个去噪步骤的运行时间。FPS和运行时在NVIDIA 4090 GPU上测量。D为模态多样性得分。"

| Method | NC↑ | DAC↑ | TTC↑ | Comf.↑ | EP↑ | PDMS↑ | Arch. | Step Time↓ | Steps | Total↓ | D↑ | Para. | FPS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Transfuser | 97.7 | 92.8 | 92.8 | 100 | 79.2 | 84.0 | MLP | 0.2ms | 1 | 0.2ms | 0% | 56M | 60 |
| TransfuserDP | 97.5 | 93.7 | 92.7 | 100 | 79.4 | 84.6+0.6 | UNet | 6.5ms | 20 | 130.0ms | 11% | 101M | 7 |
| TransfuserTD | 97.9 | 94.2 | 93.9 | 100 | 80.2 | 85.7+1.7 | UNet | 6.9ms | 2 | 13.8ms | 70% | 102M | 27 |
| DiffusionDrive | 98.2 | 96.2 | 94.7 | 100 | 82.2 | 88.1+4.1 | Dec. | 3.8ms | 2 | 7.6ms | 74% | 60M | 45 |
