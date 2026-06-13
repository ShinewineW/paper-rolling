# Navsim v1 规划性能对比
- **Source**: Table 1
- **Caption**: "Navsim v1 navtest 上与 state-of-the-art methods 的比较；论文按 Vision-Based End-to-End Methods、Vision-Language-Action Methods 与 World-Model-Based Methods 分组。"

| Methods | Venue | Sensors | NC↑ | DAC↑ | TTC↑ | C↑$ | EP↑ | PDMS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Human | - | 一 | 100.0 | 100.0 | 100.0 | 99.9 | 87.5 | 94.8 |
| Vision-Based End-to-End Methods |  |  |  |  |  |  |  |  |
| TransFuser (Chitta et al., 2022) | TPAMI&#x27;23 | 3×C+L | 97.7 | 92.8 | 92.8 | 100.0 | 79.2 | 84.0 |
| UniAD (Hu et al., 2023) | CVPR23 | $6×C$ | 97.8 | 91.9 | 92.9 | 100.0 | 78.8 | 83.4 |
| PARA-Drive (Weng et al., 2024) | CVPR24 | 6xC | 97.9 | 92.4 | 93.0 | 99.8 | 79.3 | 84.0 |
| Diff usionDrive (Liao et al., 2025) | CVPR25 | 3×C+L | 98.2 | 96.2 | 94.7 | 100.0 | 82.2 | 88.1 |
| Vision-Language-Action Methods |  |  |  |  |  |  |  |  |
| AutoVLA (Zhou et al., 2025) | NeurIPS&#x27;25 | $3×C$ | 98.4 | 95.6 | 98.0 | 99.9 | 81.9 | 89.1 |
| Recogdrive* (Li et al., 2025) | ICLR26 | $3×C$ | 98.1 | 94.7 | 94.2 | 100.0 | 80.9 | 86.5 |
| DriveVLA-W0 (Li et al., 2025) | ICLR26 | $1×C$ | 98.7 | 96.2 | 95.5 | 100.0 | 82.2 | 88.4 |
| World-Model-Based Methods |  |  |  |  |  |  |  |  |
| LAW (Li et al., 2025) | ICLR&#x27;25 | $1xC$ | 96.4 | 95.4 | 88.7 | 99.9 | 81.7 | 84.6 |
| DrivingGPT (Chen et al., 2025) | ICCV25 | $1xC$ | 98.9 | 90.7 | 94.9 | 95.6 | 79.7 | 82.4 |
| WoTE (Li et al., 2025) | ICCV&#x27;25 | 3×C+L | 98.5 | 96.8 | 94.4 | 99.9 | 81.9 | 88.3 |
| Epona (Zhang et al., 2025) | ICCV&#x27;25 | $3×C$ | 97.9 | 95.1 | 93.8 | 99.9 | 80.4 | 86.2 |
| FSDrive (Zeng et al., 2025) | NeurIPS&#x27;25 | $3xC$ | 98.2 | 93.8 | 93.3 | 99.9 | 80.1 | 85.1 |
| PWM (Zhao et al., 2025) | NeurIPS&#x27;25 | $1×C$ | 98.6 | 95.9 | 95.4 | 100.0 | 81.8 | 88.1 |
| DriveDreamer-Policy (Ours) |  | 3×C | 98.4 | 97.1 | 95.1 | 100.0 | 83.5 | 89.2 |
