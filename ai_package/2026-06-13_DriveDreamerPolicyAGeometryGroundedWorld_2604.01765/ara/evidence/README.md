# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/Navsim v1 规划性能对比.md](tables/Navsim v1 规划性能对比.md) | Table 1 | ['C1'] | Navsim v1 navtest 上与 state-of-the-art methods 的比较；论文按 Vision-Based End-to-End Methods、Vision-Language-Action Methods 与 World-Model-Based Methods 分组。 |
| [tables/Navsim v2 规划性能对比.md](tables/Navsim v2 规划性能对比.md) | Table 2 | ['C1'] | Navsim v2 navtest 上与 state-of-the-art methods 的比较；原 MD 表格存在合并单元格与抽取错位，本表按 MD 单元格文本保留。 |
| [tables/Navsim 视频生成性能对比.md](tables/Navsim 视频生成性能对比.md) | Table 3(a) | ['C2'] | Navsim 上的视频生成性能比较；论文说明 PWM 仅支持 single-view generation，因此评估 single-view front quality。 |
| [tables/Navsim 深度生成性能对比.md](tables/Navsim 深度生成性能对比.md) | Table 3(b) | ['C2'] | Navsim 上的深度生成性能比较；论文将 DriveDreamer-Policy 与 zero-shot PPD 和 fine-tune PPD on Navsim 比较。 |
| [tables/World Learning for Planning 消融.md](tables/World Learning for Planning 消融.md) | Table 4 | ['C3'] | World Learning for Planning 消融；论文称所有 world learning strategies 都相较 training from scratch 改善规划表现。 |
| [tables/Depth Learning for Video Generation 消融.md](tables/Depth Learning for Video Generation 消融.md) | Table 5 | ['C4'] | Depth Learning 对 Video Generation 的消融；论文称 using depth as a prior in joint learning improves video generation accuracy。 |
| [tables/Number of Queries 消融.md](tables/Number of Queries 消融.md) | Table 6 | ['C5'] | Number of Queries 消融；论文称更多 query tokens 提供更高容量的上下文槽位，从而增强 generation 与 planning。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/b6d3a7fd0fa684f3a5865bfd56d7923d9a454d01877521ecd2f34e22cf12c352.jpg` | result | Figure 1: Comparison of our DriveDreamer-Policy with existing models. Items with dashed lines are optional. Vision-based and VLA planners directly map observations (and optional inputs) to actions without explicitly predicting the future world. World models generate future observations but often rel |
| `images/1fa1c8d5ce984a6962ab54a09eefb664c0a90e2cee1dad33292f9bd39a0f7ac2.jpg` | architecture | Figure 2: Overview of our DriveDreamer-Policy pipeline. The large language model takes the language instruction, multi-view images and current action, along with a set of learnable queries as inputs to reason and generate world and action embeddings. The generated embeddings are then passed into our |
| `images/128ef5613a399c4cdba870d25ddd8bf7e23c44bd1b5a949b3a66195d89a0f578.jpg` | architecture | Figure 3: Visualization Results of our method. We show the generated depth, video, and actions, respectively. Depth is truncated to below 80 meters for better visualization. Our generation results remain spatially stable, and the planning performs well compared with human trajectories (e.g., aligns  |
| `images/193a139c2fa8aa04673ccea494f9e172c1f806d64a97061c4668a3e98da20a36.jpg` | result | Figure 4: Visualization of world learning for planning. Columns compare Action-Only, Depth-Action, Video-Action, and Depth-Video-Action variants. Green denotes the human (expert) trajectory and red denotes the predicted trajectory. The three rows correspond to (top) avoiding potential collision by a |
