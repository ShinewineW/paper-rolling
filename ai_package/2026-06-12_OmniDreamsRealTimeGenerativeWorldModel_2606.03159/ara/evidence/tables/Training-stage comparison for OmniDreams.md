# Training-stage comparison for OmniDreams
- **Source**: Table 4
- **Caption**: "OmniDreams 在双向、因果 Diffusion Forcing 与 Self Forcing 蒸馏阶段的仿真质量比较。"

| Training stage | FVD↓ | Temp. Sampson ↓ | LET-AP ↑ | LET-APL ↑ | LET-APH ↑ | F1↑ | x-err. (far）↓ | Cat. Acc. ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bidirectional (AV adapted) | 26.8 | 1.83 | 0.378 | 0.240 | 0.366 | 0.823 | 0.337 | 0.957 |
| Causal (Diffusion Forcing) | 31.7 | 1.87 | 0.221 | 0.136 | 0.214 | 0.775 | 0.418 | 0.941 |
| Distilled (Self Forcing) | 24.8 | 1.90 | 0.400 | 0.255 | 0.388 | 0.828 | 0.313 | 0.961 |
