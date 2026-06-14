# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/NAVSIM v1 比较.md](tables/NAVSIM v1 比较.md) | Table 1 | ['C1'] | NAVSIM v1 比较。∗ 表示使用 imitation learning 的结果；† 表示使用来自 [53] 的 multiple trajectory anchors 训练；MV 表示 multi-view cameras，SV 表示 single-view camera，L 表示 LiDAR。 |
| [tables/PhysicalAI-Autonomous-Vehicles 主结果.md](tables/PhysicalAI-Autonomous-Vehicles 主结果.md) | Table 2 | ['C2'] | 在 PhysicalAI-Autonomous-Vehicles benchmark 的 curated 1,000-clip test subset 上比较。# Params 表示模型参数数量；SV 表示 single-view camera；∗ 表示使用 released checkpoint 评测，且只支持 up to 3s prediction。 |
| [tables/scene-evolving guidance 与数据规模消融.md](tables/scene-evolving guidance 与数据规模消融.md) | Table 3 | ['C3', 'C4'] | 在 PhysicalAI-Autonomous-Vehicles benchmark 上，不同训练数据规模下 scene-evolving driving guidance 的消融。✗ 表示 fixed global prompt as text conditioning。 |
| [tables/视频骨干初始化与联合视频监督消融.md](tables/视频骨干初始化与联合视频监督消融.md) | Table 4 | ['C5'] | 视频骨干初始化和 joint video supervision 的消融；所有模型在 100k clips 上训练 50k iterations。 |
| [tables/KV memory 策略消融.md](tables/KV memory 策略消融.md) | Table 5 | ['C6'] | KV memory strategies 消融。ADE/FDE 在 20s clips 上测量，KV memory 和 GFLOPs 在 300s clip 下 profile。 |
| [tables/per-chunk 推理成本与轨迹精度.md](tables/per-chunk 推理成本与轨迹精度.md) | Table 6 | ['C7'] | 在 single H20 GPU 上的 per-chunk inference cost 和 trajectory prediction accuracy。∗ 表示 action denoising steps 从 10 reduced to 5。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/3313dfdb6a6bfb9d6026bd6d1ae92ca6e39c671207e648cdc4a92dc6c45c7efa.jpg` | architecture | Figure 1: Overview of DriveWAM, which adapts a pretrained video generation backbone into a unified video-action policy. Building on this backbone, DriveWAM uses a frozen VLM to provide chunk-specific scene-evolving guidance for high-level scene reasoning and introduces selective KV memory to preserv |
| `images/a936cf5be549e3bc2067ac68567e80a2ae387c511e0a6ca7fa4bee59e9bd7097.jpg` | result | Figure 2: Attention mask used during Drive-WAM training. Colored entries indicate allowed attention; blank entries are masked. |
| `images/c7ff4bb249156ba232d2ed84cfbbc57bf5a589566da2ebad42e13067221bef5a.jpg` | result | Figure 3: Video-token retention under selective KV memory. Columns 2 and $^ 3$ visualize the tokens retained after query chunks 4 and 5. |
| `images/8502fa8faf4225649d764d681373236807786a920048ae1e30a4959127cfeee9.jpg` | result | Figure 4: Qualitative results on NAVSIM (left) and PhysicalAI-Autonomous-Vehicles benchmark (right). The predicted ego trajectories are consistent with the jointly generated future scenes. |
| `images/ebb47b84a7561e9dc11676f7eab5ecc246ed92f20768b545a1428fcc02ea5794.jpg` | result | Figure 5: Data scaling on PhysicalAI-Autonomous-Vehicles. |
| `images/403312fd6872669bcf0f9ff3d86ff6e986c91cd1c94d437c895328080aaac49f.jpg` | result | Figure 6: Representative scene tagging results for dataset curation. For each clip, the left panel shows Qwen3-VL-8B detected scene attributes, events, and the resulting interest score, while the right panel shows sampled front-view frames. High-score clips capture rare or interaction-rich scenarios |
| `images/5a5c9daa839060c8f99254c43e0766835dfc2013ed36d51a5af11b708f6ce40e.jpg` | result | Figure 7: Examples of scene-evolving VLM guidance. The guidance adapts to changing scene context and route intent, such as pedestrians, traffic lights, construction barriers. |
| `images/276c5235c6a954df112690b8020379920250117066f461a169b218e5e6c5effc.jpg` | result | Figure 8: Qualitative results on NAVSIM (top two rows) and PhysicalAI-Autonomous-Vehicles (bottom two rows) benchmarks. Each row shows the predicted ego trajectory alongside the jointly generated future frames at T=1,2,3,4. |
