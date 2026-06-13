# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/NAVSIM v1 navtest closed-loop metrics.md](tables/NAVSIM v1 navtest closed-loop metrics.md) | Table 1 | ['C5'] | NAVSIM v1 navtest split 上 closed-loop metrics 的性能比较；论文说明 C 和 L 分别表示 camera 与 LiDAR 输入，所有结果均在 ResNet-34 image-backbone 设置下报告。 |
| [tables/NAVSIM v2 navhard two-stage pseudo-simulation.md](tables/NAVSIM v2 navhard two-stage pseudo-simulation.md) | Table 2 | ['C5'] | NAVSIM v2 navhard split 的性能比较；PDM-Closed 被论文单列为使用 ground-truth perception 的 privileged planner。 |
| [tables/IDM and closed-loop refinement ablation.md](tables/IDM and closed-loop refinement ablation.md) | Table 3 | ['C1', 'C2'] | NAVSIM navtest split 上 inverse dynamics model 与 closed-loop refinement 的主消融；IDM 表示 inverse dynamics model，CL 表示 closed-loop refinement。 |
| [tables/IDM temporal decoding ablation.md](tables/IDM temporal decoding ablation.md) | Table 4 | ['C3'] | inverse dynamics model 的 temporal decoding 消融；two-frame variant 解码相邻 BEV transitions，four-frame variant 使用更长 future window。 |
| [tables/Spatial and global dynamics branch ablation.md](tables/Spatial and global dynamics branch ablation.md) | Table 5 | ['C4'] | inverse-dynamics-guided refinement network 中 spatial dynamics branch 与 global dynamics branch 的消融。 |
| [tables/NAVSIM v2 navtest extended closed-loop metrics.md](tables/NAVSIM v2 navtest extended closed-loop metrics.md) | Table 8 | ['C5'] | NAVSIM v2 navtest split 上 extended closed-loop metrics 的性能比较；论文说明 learned methods 中 best 与 second-best 被标注。 |
| [tables/NAVSIM-v2 navhard stage-1-only protocol.md](tables/NAVSIM-v2 navhard stage-1-only protocol.md) | Table 9 | ['C5'] | NAVSIM-v2 navhard split 的 stage-1-only protocol 比较；论文说明 † 表示 V2-99 backbone 结果。 |
| [tables/Transition-aware future modeling strategies ablation.md](tables/Transition-aware future modeling strategies ablation.md) | Table 10 | ['C1'] | NAVSIM navtest split 上 transition-aware future modeling strategies 的消融；Future State Only 不显式解码相邻状态转移，Latent Difference 用直接 adjacent-feature differences 替代 learned IDM。 |
| [tables/Global dynamics fusion strategies ablation.md](tables/Global dynamics fusion strategies ablation.md) | Table 11 | ['C4'] | inverse-dynamics-guided refinement network 中 global dynamics fusion strategies 的消融；所有变体使用相同 spatial branch，仅替换 refined ego query 与 global dynamics feature 之间的 fusion operation。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/2f6c42ecfece244d877e64a93ebc3bb192d04d86eed590c2658d7d168d66ef28.jpg` | result | Figure 1: Comparison of three planning paradigms. (a) Traditional methods directly map sensor inputs to a predicted trajectory. (b) World-model-based methods additionally predict future latent BEV states to support planning, but these predicted futures are only loosely connected to motion generation |
| `images/03b652926d2fe2aa535f368e07c1c55c2731af87a09202463ce1547257ce3b05.jpg` | architecture | Figure 2: Overview of the proposed IDOL framework. (a) The closed-loop refinement module rolls out future latent BEV states with the BEV world model and refines the planning query through inverse-dynamics feedback. (b) The planning network fuses the refined query with trajectory anchors, predicts ca |
| `images/3091222dff504e6138df979d87e241ef5e9b28d25a886a96bfba445035aaf7d0.jpg` | result | Figure 3: Qualitative visualization of inverse-dynamics-guided refinement on the NAVSIM navtest split. |
| `images/23cc672c59be988d73ba95f79bd1cb7d786499cc7d3036015d16331b55408764.jpg` | result | Figure 4: Qualitative visualization of inverse-dynamics refinement under three representative driving maneuvers on the NAVSIM navtest split. From top to bottom: straight driving, left turn, and right turn. In each row, panels (a)–(d) show the latent BEV change, the IDM dynamics inferred from adjacen |
| `images/e45d76d6de10d11ac89abf2ba449fa98c2a504230ec05bfa690b890923123d53.jpg` | result | Figure 5: Representative failure cases on navtest. |
