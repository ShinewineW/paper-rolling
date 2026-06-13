# Transition-aware future modeling strategies ablation
- **Source**: Table 10
- **Caption**: "NAVSIM navtest split 上 transition-aware future modeling strategies 的消融；Future State Only 不显式解码相邻状态转移，Latent Difference 用直接 adjacent-feature differences 替代 learned IDM。"

| Transition Modeling | NC↑ | DAC↑ | TTC个 | Comf. 个 | EP个 | PDMS个 |
| --- | --- | --- | --- | --- | --- | --- |
| Future State Only | 98.4 | 96.6 | 95.2 | 100 | 82.6 | 88.6 |
| Latent Difference | 98.6 | 96.8 | 95.7 | 100 | 82.8 | 89.0 |
| IDM | 98.8 | 97.6 | 95.9 | 100 | 83.8 | 90.0 |
