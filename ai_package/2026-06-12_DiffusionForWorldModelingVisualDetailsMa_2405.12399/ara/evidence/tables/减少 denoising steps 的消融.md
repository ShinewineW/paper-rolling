# 减少 denoising steps 的消融
- **Source**: Table 7
- **Caption**: "将 DIAMOND EDM diffusion world model 的 denoising steps 从默认设置减少到单步后的定量消融。"

| Game | Random | Human | DIAMOND (n = 3) | DIAMOND (n = 1) |
| --- | --- | --- | --- | --- |
| Amidar | 5.8 | 1719.5 | 225.8 | 191.8 |
| Assault | 222.4 | 742.0 | 1526.4 | 782.5 |
| Asterix | 210.0 | 8503.3 | 3698.5 | 6687.0 |
| Boxing | 0.1 | 12.1 | 86.9 | 41.9 |
| Breakout | 1.7 | 30.5 | 132.5 | 50.8 |
| CrazyClimber | 10780.5 | 35829.4 | 99167.8 | 87233.0 |
| Kangaroo | 52.0 | 3035.0 | 5382.2 | 1710.0 |
| Krull | 1598.0 | 2665.5 | 8610.1 | 9105.1 |
| Pong | -20.7 | 14.6 | 20.4 | 20.9 |
| RoadRunner | 11.5 | 7845.0 | 20673.2 | 5084.0 |
| Mean HNS (↑) | 0.000 | 1.000 | 3.052 | 1.962 |
