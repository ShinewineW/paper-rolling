# NAVSIM v1 比较
- **Source**: Table 1
- **Caption**: "NAVSIM v1 比较。∗ 表示使用 imitation learning 的结果；† 表示使用来自 [53] 的 multiple trajectory anchors 训练；MV 表示 multi-view cameras，SV 表示 single-view camera，L 表示 LiDAR。"

| Method | Ref | Sensors | NC个 | DAC↑ | TTC↑ | C.↑ | EP个 | PDMS ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Human | 1 | 1 | 100 | 100 | 100 | 99.9 | 87.5 | 94.8 |
| UniAD [54] | CVPR'23 | MV | 97.8 | 91.9 | 92.9 | 100.0 | 78.8 | 83.4 |
| TransFuser [55] | TPAMI'23 | MV&L | 97.7 | 92.8 | 92.8 | 100.0 | 79.2 | 84.0 |
| PARA-Drive [56] | CVPR'24 | MV | 97.9 | 92.4 | 93.0 | 99.8 | 79.3 | 84.0 |
| LAW [57] | ICLR'25 | SV | 96.4 | 95.4 | 88.7 | 99.9 | 81.7 | 84.6 |
| DiffusionDrive [58] | CVPR'25 | MV&L | 98.2 | 96.2 | 94.7 | 100.0 | 82.2 | 88.1 |
| WoTE [59] | ICCV'25 | MV&L | 98.5 | 96.8 | 94.4 | 99.9 | 81.9 | 88.3 |
| VLA-based Methods |  |  |  |  |  |  |  |  |
| ReCogDrive* [4] | ICLR'26 | MV | 98.1 | 94.7 | 94.2 | 100.0 | 80.9 | 86.5 |
| DriveVLA-W0 [3] | ICLR'26 | SV | 98.7 | 96.2 | 95.5 | 100.0 | 82.2 | 88.4 |
| AutoVLA [37] | NeurIPS'25 | MV | 98.4 | 95.6 | 98.0 | 99.9 | 81.9 | 89.1 |
| DriveDreamer-Policy [14] | arXiv'26 | MV | 98.4 | 97.1 | 95.1 | 100.0 | 83.5 | 89.2 |
| DriveVLA-W0t [3] | ICLR'26 | SV | 98.7 | 99.1 | 95.3 | 99.3 | 83.3 | 90.2 |
| WA-based Methods |  |  |  |  |  |  |  |  |
| Epona [24] | ICCV'25 | Sv | 97.9 | 95.1 | 93.8 | 99.9 | 80.4 | 86.2 |
| WorldDrive [22] | arXiv'26 | SV | 98.4 | 95.8 | 95.2 | 99.8 | 83.3 | 89.0 |
| DriveWAM | 一 | sv | 98.3 | 98.1 | 95.2 | 100.0 | 84.3 | 90.1 |
