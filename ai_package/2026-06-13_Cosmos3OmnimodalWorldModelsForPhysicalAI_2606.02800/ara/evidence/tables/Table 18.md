# Table 18
- **Source**: Table 18
- **Caption**: "forward dynamics 与 inverse dynamics 的 post-training comparison。"

| Model | Autonomous Vehicle (ID) | Camera Motion (FD) | Egocentric Motion (FD) | Robotics (FD) |
| --- | --- | --- | --- | --- |
| RRE(,) | RTE (m, ↓) | ATE (m, ↓) | RRE(，↓) | RTE (m, ↓) | ATE (m, ↓) | PSNR (↑) | PSNR (↑) |
| Cosmos3-Super (MT-init) | 0.232 | 0.014 | 0.90 | 0.142 | 0.026 | 0.99 | 16.19 | 26.04 |
| Cosmos3-Nano (MT-init) | 0.211 | 0.014 | 0.98 | 0.147 | 0.029 | 1.24 | 16.12 | 25.52 |
| Cosmos3-Super (PT-init) | 0.284 | 0.018 | 1.32 | 0.293 | 0.036 | 1.82 | 15.34 | 22.69 |
| Cosmos3-Nano (PT-init) | 0.249 | 0.017 | 1.20 | 0.172 | 0.034 | 1.61 | 15.22 | 23.24 |
| Lingbot-World | - | / | 一 | 0.299 | 0.057 | 2.88 | - | - |
| HY-World1.5 | - | - | - | 0.377 | 0.042 | 1.39 | - | - |
| VGGT | 0.596 | 0.768 | 23.46 | - | - | - | - | - |
| DepthAnything3 | 0.312 | 0.354 | 9.29 | - |  |  | - | 一 |
| LOME | - | - | - | - | 一 | 一 | 9.36 | - |
| Ctrl-World | - | - | - | - |  |  | - | 22.99 |
