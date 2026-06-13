# Navsim v2 规划性能对比
- **Source**: Table 2
- **Caption**: "Navsim v2 navtest 上与 state-of-the-art methods 的比较；原 MD 表格存在合并单元格与抽取错位，本表按 MD 单元格文本保留。"

| Methods | Venue | NC↑ | DAC↑ | DDC↑ | TLC↑ | EP↑ | TTC↑ | LK↑ HC↑ | EC↑ | EPDMS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Vision-Based End-to-End Methods |  |  |  |  |  |  |  |  |  |
| TransFuser (Chitta et al., 2022) DiffusionDrive (Liao et al., 2025) | TPAMI&#x27;23 | 96.9 | 89.9 | 97.8 | 99.7 | 87.1 | 95.4 | 92.7 98.3 | 87.2 | 76.7 |
|  | CVPR25 | 98.2 | 95.9 99.4 | 99.8 | 87.5 | 97.3 | 96.8 | 98.3 | 87.7 | 84.5 |
| Drivesuprim (Yao et al., 2025) | AAAI&#x27;26 | 97.5 | 96.5 99.4 | 99.6 | 88.4 | 96.6 | 95.5 | 98.3 | 77.0 | 83.1 |
| ARTEMs (Feng et al., 2026) | RAL&#x27;26 | 98.3 95.1 | 98.6 |  | 99.8 81.5 |  | 97.4 96.5 | 98.3 | 89.1 | 83.1 |
| DriveVLA-Wo (Li et al., 2025) | Vision-Language-Action Methods ICLR&#x27;26 |  |  |  |  |  |  |  |  |  |
|  |  | 98.5 | 99.1 | 98.0 | 99.7 | 86.4 | 98.1 | 93.2 97.9 | 58.9 | 86.1 |
| DriveDreamer-Policy (Ours) |  | 98.4  97.1 | World-Model-Based Methods | 99.5 99.9 | 87.9 | 97.7 |  | 97.698.3 | 79.4 | 88.7 |
