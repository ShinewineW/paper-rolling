# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/NAVSIM navtest split闭环评估对比.md](tables/NAVSIM navtest split闭环评估对比.md) | Table 1 | ['C2'] | 在规划导向的NAVSIM navtest split上进行闭环指标对比。C&L表示同时使用相机和激光雷达传感器输入。V8192表示8192个锚点。Hydra-MDP-V8192-W-EP是Hydra-MDP的变体,使用规则评估器额外监督和加权置信度后处理。DiffusionDrive仅从人类演示中学习且无后处理。 |
| [tables/从Transfuser到DiffusionDrive演进路线图.md](tables/从Transfuser到DiffusionDrive演进路线图.md) | Table 2 | ['C1', 'C2'] | 在NAVSIM navtest split上从Transfuser到DiffusionDrive的路线图。TransfuserDP表示使用原始DDIM扩散策略的Transfuser。TransfuserTD表示使用截断扩散策略的Transfuser。Step Time为每个去噪步骤的运行时间。FPS和运行时在NVIDIA 4090 GPU上测量。D为模态多样性得分。 |
| [tables/扩散解码器设计选择消融.md](tables/扩散解码器设计选择消融.md) | Table 3 | ['C3'] | 扩散解码器设计选择消融实验。「Cascade Decoder」表示堆叠2个级联扩散解码器层。ID-1对应Table 2中的TransfuserTD,使用条件UNet和自我查询交互。 |
| [tables/去噪步数消融.md](tables/去噪步数消融.md) | Table 4 | ['C1'] | 去噪步数对规划性能的影响。即使仅1步去噪也能取得较好质量,进一步步数提供质量改善和复杂环境的推理灵活性。 |
| [tables/级联阶段数消融.md](tables/级联阶段数消融.md) | Table 5 | ['C3'] | 级联阶段数对规划性能和参数量的影响。增加阶段数提升规划质量但在4阶段后趋于饱和且参数量增大。 |
| [tables/采样噪声数量N_infer消融.md](tables/采样噪声数量N_infer消融.md) | Table 6 | ['C2'] | 推理时采样噪声数量N_infer对规划性能的影响。采样更多噪声可覆盖更大的潜在动作空间并改善规划质量。 |
| [tables/nuScenes数据集开环指标对比.md](tables/nuScenes数据集开环指标对比.md) | Table 7 | ['C4'] | 在nuScenes数据集上以开环指标进行对比。FPS在单张NVIDIA 4090 GPU上按SparseDrive的测量方案进行测量。指标计算遵循ST-P3的方案。 |
| [tables/驾驶先验类型对比.md](tables/驾驶先验类型对比.md) | Table 8 | ['C5'] | 驾驶先验类型对比。「Anchored Dist.」表示锚定高斯分布。「Extra. Traj.」表示基于当前状态的外推轨迹。蓝色Row-1为论文正文DiffusionDrive基准配置。 |
| [tables/锚点来源跨域泛化性实验(CARLA Longest6).md](tables/锚点来源跨域泛化性实验(CARLA Longest6).md) | Table 9 | ['C6'] | 锚点来源泛化性实验。在CARLA Longest6基准上测试使用NAVSIM数据集聚类锚点训练的DiffusionDrive。†表示结果引自Transfuser原论文。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/c15f15d9341cc12fc60f9289b3a4a22d25cd6b7f210ecf80444de8478ea0984f.jpg` | result | Figure 1. The comparison of different end-to-end paradigms. (a) Single mode regression [7, 16, 20]. (b) Sampling from vocabulary [3, 25]. (c) Vanilla diffusion policy [6, 19]. (d) The proposed truncated diffusion policy. |
| `images/d8ca26f641edc501ef825d559b265b45ef76d6cf2152855d59e91e2ffe03e6de.jpg` | result | Figure 2. Qualitative comparison of Transfuser, TransfuserDP and DiffusionDrive on challenging scenes of NAVSIM navtest split. With the same inputs from front cameras and LiDAR, DiffusionDrive achieves the highest planning quality of top-1 scoring trajectory as illustrated in Tab. 2. We render the h |
| `images/d9a02c1cc5a9229c38c8eb2d18bfced2d1e45b4d043660b9394d140085168795.jpg` | result | Figure 2. Qualitative comparison of Transfuser, TransfuserDP and DiffusionDrive on challenging scenes of NAVSIM navtest split. With the same inputs from front cameras and LiDAR, DiffusionDrive achieves the highest planning quality of top-1 scoring trajectory as illustrated in Tab. 2. We render the h |
| `images/45def8b6beb7505c6b6485eb186463e017a4fcbf55adbb38b1a730034f3b69b2.jpg` | result | Figure 3. Illustration of truncated diffusion policy by comparing with vanilla diffusion policy. We truncate the diffusion process and only add a small portion of Gaussian noise to diffuse the anchor trajectories. Then, we train the diffusion model to reconstruct the ground-truth trajectory from the |
| `images/d21fd369588e5f60a493cd17a5ff602afb4e5526b6f24a67ca4b65165a5408b9.jpg` | result | Figure 3. Illustration of truncated diffusion policy by comparing with vanilla diffusion policy. We truncate the diffusion process and only add a small portion of Gaussian noise to diffuse the anchor trajectories. Then, we train the diffusion model to reconstruct the ground-truth trajectory from the |
| `images/f6953525c323f6d2024116bab59b7c80fe48deab63da60a7ed44638a0949357b.jpg` | architecture | Figure 4. Overall architecture of DiffusionDrive. (a) DiffusionDrive can integrate various existing perception modules and sensor inputs. (b) The designed diffusion decoder takes the sampled noisy trajectories from anchored Gaussian distribution as input and progressively denoises them with enhanced |
| `images/a388d4b554b245eae86fefa7ed75bd1d911648a08da06f08f5a0cfc83c837419.jpg` | result | Figure 5. Qualitative comparison of Transfuser, TransfuserDP and DiffusionDrive on going straight scenarios of NAVSIM navtest split. |
| `images/c5e993217de6521f441410c2015842e654cb1b409e7286dd16d245f5adbe2985.jpg` | result | Figure 6. Qualitative comparison of Transfuser, TransfuserDP and DiffusionDrive on turning left scenarios of NAVSIM navtest split. |
| `images/cede027d548a4f94986db0bbb92d6066b49e3d7efb6895e2e9ef5dd72ae576ca.jpg` | result | Figure 7. Qualitative comparison of Transfuser, TransfuserDP and DiffusionDrive on turning right scenarios of NAVSIM navtest split. |
