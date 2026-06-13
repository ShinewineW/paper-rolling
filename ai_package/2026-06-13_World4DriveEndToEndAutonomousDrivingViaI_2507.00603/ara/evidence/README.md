# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/nuScenes 主结果.md](tables/nuScenes 主结果.md) | Table 1 | ['C1'] | nuScenes benchmark 上的端到端规划结果。 |
| [tables/NavSim 主结果.md](tables/NavSim 主结果.md) | Table 2 | ['C2'] | NavSim benchmark 上的端到端规划结果。 |
| [tables/组件消融.md](tables/组件消融.md) | Table 3 | ['C3'] | 各提出组件的消融研究。 |
| [tables/不同驾驶条件.md](tables/不同驾驶条件.md) | Table 4 | ['C4'] | 不同天气与光照条件下的性能。 |
| [tables/不同驾驶机动.md](tables/不同驾驶机动.md) | Table 5 | ['C4'] | 不同驾驶机动下的性能；此表按 Markdown 中解析出的单行单元格逐字保留。 |
| [tables/扩展性消融.md](tables/扩展性消融.md) | Table 6 | ['C5'] | World4Drive 的扩展性消融研究。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/6a917d99ff3f64ea543eb84ea23e197c9eb32b5abacdb0c3c9b24c0e97ffd540.jpg` | result | Figure 1. Our proposed World4Drive demonstrates superior convergence efficiency and performance compared to PerAct on the nuScenes dataset. As shown in the figure, where the x-axis represents training epochs (same iterations) and the y-axis shows normalized performance (calculated as the ratio of ou |
| `images/20f0c662b728e34a8f7d87003c14816d84444a0eb0653c3d2c82f09ac474e74c.jpg` | result | Figure 2. We propose World4Drive, a novel approach that constructs an intention-aware latent world model to generate, evaluate, and rank multi-modal trajectories under multi-modal driving intentions. |
| `images/c31963ffa31b50a39ef9384becbf3267f794597d611fcb190b16722cc6789c99.jpg` | architecture | Figure 3. Detailed pipeline of context encoder. It consists of a 3D spatial encoding module and a semantic understanding module, achieving a holistic understanding of the physical world. |
| `images/a269c086d9577cf4ec1725213750b66463a503702635f9a7d8757bf5b95d5e34.jpg` | architecture | Figure 4. Detailed pipeline of World Model Selector. By computing and comparing feature distances between predicted latents and actual latent, the model selects the most plausible latent and its corresponding trajectory as output. The selector employs reconstruction loss between the selected latent  |
| `images/5fc6a7e3a0e8dd1094399cb243bf65484659d1c5bf84efbef6607f3eec781d93.jpg` | result | Figure 5. Visualization of World4Drive. Since World4Drive does not predict explicit perception results, we render the ground truth annotations as the perception results. |
