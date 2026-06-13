# Global dynamics fusion strategies ablation
- **Source**: Table 11
- **Caption**: "inverse-dynamics-guided refinement network 中 global dynamics fusion strategies 的消融；所有变体使用相同 spatial branch，仅替换 refined ego query 与 global dynamics feature 之间的 fusion operation。"

| Fusion Strategy | NC↑ | DAC 个 | TTC个 | Comf. 个 | EP个 | PDMS 个 |
| --- | --- | --- | --- | --- | --- | --- |
| Additive | 98.7 | 97.2 | 95.7 | 100 | 83.5 | 89.5 |
| Concat-MLP | 98.7 | 97.6 | 95.5 | 100 | 83.8 | 89.8 |
| MLN | 98.8 | 97.6 | 95.9 | 100 | 83.8 | 90.0 |
