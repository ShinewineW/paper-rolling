# NAVSIM test split 闭环规划性能对比
- **Source**: Table 1
- **Caption**: "NAVSIM test split 上与 state-of-the-art methods 的闭环驾驶性能比较；PDMS 及其子指标衡量规划质量。"

| Method | Input | NC ↑ | DAC↑ | EP↑ | TTC↑ | Comf.个 | PDMS ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Traditional End-to-End Methods |  |  |  |  |  |  |  |
| VADv2-V8192 [6] | C | 97.2 | 89.1 | 76.0 | 91.6 | 100.0 | 80.9 |
| UniAD [17] | C | 97.8 | 91.9 | 78.8 | 92.9 | 100.0 | 83.4 |
| TransFuser [9] | C&L | 97.7 | 92.8 | 79.2 | 92.8 | 100.0 | 84.0 |
| ReCogDrive-IL [30] | SC | 98.1 | 94.7 | 80.9 | 94.2 | 100.0 | 86.5 |
| DiffusionDrive [33] | C&L | 98.2 | 96.2 | 82.2 | 94.7 | 100.0 | 88.1 |
| World Model Methods |  |  |  |  |  |  |  |
| DrivingGPT[7] | SC | 98.9 | 90.7 | 79.7 | 94.9 | 95.6 | 82.4 |
| Epona [61] | SC | 97.9 | 95.1 | 80.4 | 93.8 | 99.9 | 86.2 |
| ImagiDrive-A [26] | SC | 98.1 | 96.2 | 80.1 | 94.4 | 100.0 | 86.9 |
| DriveVLA-W0 [28] | SC | 98.4 | 95.3 | 80.9 | 95.4 | 100.0 | 87.2 |
| SGDrive-IL [25] | SC | 98.6 | 95.1 | 81.2 | 95.4 | 100.0 | 87.4 |
| PWM [62] | SC | 98.6 | 95.9 | 81.8 | 95.4 | 100.0 | 88.1 |
| WoTE [29] | C&L | 98.5 | 96.8 | 81.9 | 94.9 | 99.9 | 88.3 |
| ResWorld [60] | C&L | 98.9 | 96.5 | 83.1 | 95.6 | 100.0 | 89.0 |
| Uni-World VLA（Ours) | sC | 98.7 | 96.7 | 83.2 | 96.1 | 100.0 | 89.4 |
