# distribution_vs_distortion
- **Source**: Table 2
- **Caption**: "held-out test上t+16的distribution与distortion指标对比；KID和FID越低越好，CosSim越高越好，Diffusion (calib.)使用train-derived calibration。"

| Model | KID↓ | FID↓ | CosSim↑ |
| --- | --- | --- | --- |
| Direct (regression) | 0.375 | 370.8 | 0.471 |
| Diffusion (raw) | 0.294 | 341.9 | 0.233 |
| Interp (α=.5) | 0.084 | 166.6 | 0.316 |
| Diffusion (calib.) | 0.078 | 162.5 | 0.260 |
| VAE-GT ceiling | ~0 | ~0 | 1.000 |
