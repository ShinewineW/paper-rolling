# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/NAVSIM test split 闭环规划性能对比.md](tables/NAVSIM test split 闭环规划性能对比.md) | Table 1 | ['C1'] | NAVSIM test split 上与 state-of-the-art methods 的闭环驾驶性能比较；PDMS 及其子指标衡量规划质量。 |
| [tables/driving world models 视频生成质量对比.md](tables/driving world models 视频生成质量对比.md) | Table 2 | ['C1'] | driving world models 的视频生成质量比较，FVD 4.1 衡量未来视频序列真实感，并报告预测时长、帧率、数据集和视角。 |
| [tables/pretrain、future-frame modeling 与 depth conditioning 消融.md](tables/pretrain、future-frame modeling 与 depth conditioning 消融.md) | Table 3 | ['C3'] | pretraining、future-frame modeling 与 depth conditioning 对规划质量和未来帧生成质量的影响。 |
| [tables/替代生成 scheme 消融.md](tables/替代生成 scheme 消融.md) | Table 4 | ['C2'] | 无 depth fusion 设置下五种 frame-action 生成 scheme 的规划性能消融。 |
| [tables/历史视觉信息消融.md](tables/历史视觉信息消融.md) | Table 5 | ['C4'] | 无 depth fusion 设置下历史视觉信息配置对规划与未来帧生成质量的影响。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/a9eea62e83eb434c9dd0ccb3cdcc5e8e4d9d88f1183b15ce9061a6634c8d5119.jpg` | result | Fig. 1: Different generative paradigms of unified world models for autonomous driving. (a) Unified world models perform video generation and planning as separate tasks; (b) World-conditioned trajectory prediction, where future trajectories are predicted conditioned on the generated world states; (c) |
| `images/45ad7aa4bb253039c0ebe704e475c9d85ddc4f52b8ba43efbbff4768f4ece984.jpg` | architecture | Fig. 2: Overview of the paradigm of alternative generation in Uni-World VLA. (a) The construction of multi-model historical information; (b) The interleaved frameaction generative paradigm. |
| `images/60dae5774150c1e5e6f69e445a8641ab142a9e7bc25f2c46bed1e0f07de4c194.jpg` | result | Fig. 3: Schematic illustration of training and inference process. (a) Interleaved sequence for joint video generation and trajectory supervision. (b) Causal attention mask. (c) Autoregressive interleaved inference with KV-cache reuse. |
| `images/bb295875498d19015a4baf170f68632328753c3e0a1d39e6b7daa15879c30867.jpg` | result | Fig. 4: Visualization of predicted frames and BEV trajectories |
| `images/4867fcec1f89d287d5808ee5113edd3326c98583e587dcebc9b08eb172cae6b2.jpg` | result | Fig. 5: Comparison of predicted future frames with and without depth fusion |
| `images/12a5633f427aae2f1f26126cfa56d9ef91184b3a1add0748462dff09ab3d4c39.jpg` | result | Fig. 6: Details of contextual, dynamic and action tokens |
| `images/90b510101dcb6603e7a974150e1097cc021e83b30d01ae2a0c470e1312d750c1.jpg` | result | Fig. 7: Visualization of predicted future frames (a) and the corresponding ground truth (b) in representative and challenging driving scenarios. |
| `images/60b64fa0e828ca3ec2135ef2a9c4850d853828f8e5a3415a19e521deba8d96b8.jpg` | result | Fig. 8: BEV visualization of the corresponding six scenarios (from left to right and top to bottom). Green polyline: ground-truth trajectory; red polyline: planned future trajectory. |
