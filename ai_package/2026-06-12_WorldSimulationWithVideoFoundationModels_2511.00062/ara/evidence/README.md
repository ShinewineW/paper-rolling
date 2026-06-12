# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/模型配置.md](tables/模型配置.md) | Table 3 | ['C1'] | Cosmos-Predict2.5 两种规模模型的结构配置。 |
| [tables/渐进式预训练阶段.md](tables/渐进式预训练阶段.md) | Table 4 | ['C1'] | 渐进式预训练从图像生成扩展到视频与文本世界生成。 |
| [tables/RL 前后 VideoAlign 奖励.md](tables/RL 前后 VideoAlign 奖励.md) | Table 6 | ['C2'] | Cosmos-Predict2.5-2B 在 Text2World 与 Image2World 中 RL 前后的 VideoAlign 奖励。 |
| [tables/Text2World 蒸馏结果.md](tables/Text2World 蒸馏结果.md) | Table 7 | ['C3'] | PAI-Bench-Predict-Text2World 上 teacher 与 distilled 模型结果。 |
| [tables/Image2World 蒸馏结果.md](tables/Image2World 蒸馏结果.md) | Table 8 | ['C3'] | PAI-Bench-Predict-Image2World 上 teacher 与 distilled 模型结果。 |
| [tables/训练效率.md](tables/训练效率.md) | Table 9 | ['C1'] | 使用 4096 NVIDIA H100 GPUs、720p 分辨率和 93 帧时的训练效率。 |
| [tables/PAI-Bench Text2World 结果.md](tables/PAI-Bench Text2World 结果.md) | Table 10 | ['C4'] | PAI-Bench-Predict-Text2World 基准结果。 |
| [tables/PAI-Bench Image2World 结果.md](tables/PAI-Bench Image2World 结果.md) | Table 11 | ['C4'] | PAI-Bench-Predict-Image2World 基准结果。 |
| [tables/Transfer 模型多控制配置评估.md](tables/Transfer 模型多控制配置评估.md) | Table 12 | ['C5'] | 不同单模态和均匀权重多模态 Transfer 配置的控制对齐与整体质量。 |
| [tables/真实机器人策略定量评估.md](tables/真实机器人策略定量评估.md) | Table 13 | ['C6'] | Base、Baseline 与使用 Cosmos-Transfer2.5-2B 增强观测训练的 Proposed 策略在十种测试场景中的成功次数。 |
| [tables/多视角驾驶视频视觉指标.md](tables/多视角驾驶视频视觉指标.md) | Table 14 | ['C7'] | RDS-HQ-HL 多视角生成视频的视觉质量与多视角一致性指标。 |
| [tables/多视角驾驶检测指标.md](tables/多视角驾驶检测指标.md) | Table 15 | ['C7'] | RDS-HQ-HL 多视角生成视频上的三维框与车道检测评估。 |
| [tables/Camera Control 对比.md](tables/Camera Control 对比.md) | Table 16 | ['C1'] | Cosmos-Predict2.5 与 Cosmos-Predict1 在相机控制能力上的对比。 |
| [tables/多相机视频生成评估.md](tables/多相机视频生成评估.md) | Table 17 | ['C5'] | 机器人多相机视频生成中相机精度与视角同步评估。 |
| [tables/DreamGen GR1 指令跟随结果.md](tables/DreamGen GR1 指令跟随结果.md) | Table 18 | ['C4'] | DreamGen Bench GR1 指令跟随中对象、行为与环境泛化评估。 |
| [tables/Bridge 动作条件视频预测.md](tables/Bridge 动作条件视频预测.md) | Table 19 | ['C8'] | Bridge 数据集上的动作条件视频预测质量评估。 |
| [tables/Bridge 动作条件注入方式消融.md](tables/Bridge 动作条件注入方式消融.md) | Table 20 | ['C8'] | Bridge 数据集上动作条件注入方式的消融结果。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/696fdcf6715b74ae88016a64c48bc6876e5163f88b4016e063d7763516f8b05c.jpg` | architecture | Figure 1: Our video curation pipeline transforms raw, unstructured video data from diverse real-world sources into a high-quality, annotated, deduplicated, and sharded dataset optimized for large-scale training of video world foundation models. |
| `images/b0df84f4a36074b48ac5457db8c21b8990f7ac47361cc4274e414350a22a7f0d.jpg` | architecture | Figure 2: Overall architecture of [Cosmos-Predict2.5]. As shown on the right, in the latent space, the model applies repeated blocks of self-attention, cross-attention, and feed-forward MLP layers, modulated by adaptive layer normalization (scale, shift, gate) for a given time step ??. We leverage [ |
| `images/6dcccd02c58a6629766133f03514dc4b459dd24838ce43ccac20a4eac62f8edf.jpg` | result | Figure 4: Merged model gets the best of all the worlds while maintaining performance on the general domain. Win rate for pretrained is average across three comparisons. |
| `images/cdd69cddfb9cc80475833981d55baaf27809c4b804ace31f972821e926c5e4aa.jpg` | result | Figure 5: Human voting shows that RL can effectively improve the quality of the generated videos. |
| `images/3d6bb0045552cc0502f8350f271a83a0b183830107d259f14b69da57e8396523.jpg` | result | ## 4.2.2. Reinforcement Learning |
| `images/619b50fa595d6ca2950808a27e2e8b4db4e6adc7c0b04e059a4a37ead182d24d.jpg` | result | Figure 7: Across a diverse set of prompts, post-trained [Cosmos-Predict2.5-14B] is preferred more often than Wan 2.1 14B, and achieves on par performance to Wan 2.2 27B-A14B, despite having only half the parameter count. |
| `images/3041a4321de6ec71262799e70559ed33fa3403c36c835848e4d9886815780dc2.jpg` | result | ## 6. Applications |
| `images/ca5eee40338a52ccdd5d4322d3c6084598723c4d92a8c39031d6f25ec884d61d.jpg` | result | Figure 8: [Cosmos-Predict2.5-2B] post-trained prediction samples on the PAI-Bench dataset. |
| `images/4de2a58d015cf2a0aaf4ff06c7053f876e2b0d2f758889060fb21790c0b07cae.jpg` | result | Figure 9: Sample comparison results of [Cosmos-Transfer2.5-2B]. Compared to [Cosmos-Transfer1-7B], [Cosmos-Transfer2.5-2B] has better prompt alignment, better adherence to control input, and less hallucination and error accumulation (especially for long videos). |
| `images/00f7626b2f4298a770c3d7dda3047fb388f65758a831aab57283319aea7f353c.jpg` | result | Edge Control |
| `images/a9366f228991953bb1b0ff49a315eb2583a9034689d9547a05bae81e76ca1932.jpg` | result | Figure 10: Error accumulation for long video generations. These plots show the Normalized Relative Dover Score vs Chunk Index for auto-regressive multi-trunk long video generation where each trunk is 93 frames. As shown, for all four control modalities (edge/blur/depth/seg), compared to [Cosmos-Tran |
| `images/6b84e3c23d72fa4b41d05ca445a88cf36704337005c352520f9c5fab71c33371.jpg` | result | Figure 10: Error accumulation for long video generations. These plots show the Normalized Relative Dover Score vs Chunk Index for auto-regressive multi-trunk long video generation where each trunk is 93 frames. As shown, for all four control modalities (edge/blur/depth/seg), compared to [Cosmos-Tran |
| `images/7a4d7f65c4254ad844e23e6594d28ec89fc41653bdf1671826350b97332a3407.jpg` | result | Figure 10: Error accumulation for long video generations. These plots show the Normalized Relative Dover Score vs Chunk Index for auto-regressive multi-trunk long video generation where each trunk is 93 frames. As shown, for all four control modalities (edge/blur/depth/seg), compared to [Cosmos-Tran |
| `images/98c79a5aaf0a2e81eda9cc8b1baf3c77b2169442da25a4faefbd23eb94239730.jpg` | result | Figure 11: Real-Robot Teleoperation Samples. Two episodes of image observations captured from the egocentric camera during demonstration collection. We keep the object instances and scene fixed and only change the objects’ (apple and bowl) poses. |
| `images/bd68876b83ac55ee1aecf9244335cf0e328589600b7510c547703b89fb39813b.jpg` | result | Figure 12: Real-Robot Data Augmentation Gallery. We show the baseline (top row) and [Cosmos-Transfer2.5- 2B] (bottom two rows) data augmentation samples. |
| `images/f9518ac927b036184096ad3266db8e9c4506fb696e7a4429b8add8e771b36b90.jpg` | result | Figure 13: [Cosmos-Transfer2.5] Real-Robot Policy Rollouts. We present sample [Cosmos-Transfer2.5-2B] policy rollouts under the base setting and nine unseen test-time scenarios. |
| `images/9aebcc6a6f4313dadd7b4425ffe7f696f6fc2b025a459f18e837c73457560676.jpg` | result | Figure 14: Generated multi-view frames from [Cosmos-Transfer2.5-2B/auto/multiview]. The multi-view 720p control videos for driving simulation consist of HD map elements like lanes, road markings, poles, traffic signals, traffic lights (with state), all of which can represent complex road topologies  |
| `images/dd33ead48abdd6d6e8cb262a91270730f76f0fc461be0ee2025749639c684283.jpg` | result | Figure 14: Generated multi-view frames from [Cosmos-Transfer2.5-2B/auto/multiview]. The multi-view 720p control videos for driving simulation consist of HD map elements like lanes, road markings, poles, traffic signals, traffic lights (with state), all of which can represent complex road topologies  |
| `images/5dedd2b69e7e90a45ca7cff1aa31083343124cc259245add65b1155807fe94bf.jpg` | result | Figure 15: Comparative controlled generations between [Cosmos-Transfer1-7B-Sample-AV] and [Cosmos-Transfer2.5-2B/auto/multiview]. In example (1), we can observe that [Cosmos-Transfer1-7B-Sample-AV] hallucinates a distorted black car behind the silver vehicle, which is described neither in the text p |
| `images/47bf93d592b0250d39635c690e4d975b45a3fba6451f07264ad22e24bfd53cc5.jpg` | result | Figure 16: [Cosmos-Transfer2.5-2B/robot/multiview-agibot] generates temporally synchronized robotic manipulation videos from the left and right gripper viewpoints, conditioned on the head-view input. |
| `images/5bc5a204c8d9c94027021c13783e9f29926fc7f912447231891ddd075d034441.jpg` | result | Figure 17: [Cosmos-Transfer2.5-2B/robot/multiview] synthesizes synchronized videos under basic dynamic and static camera transformations, conditioned on the third-view robotic manipulation input. |
| `images/250577563228e14568fad6096dbde9e10f5c0bc32e4a558320cc10404a5dcc5e.jpg` | result | Cosmos-Transfer2.5-2B/robot/multiview-agibot |
| `images/b9e4c076e8f1383c3a9e95af5b601a77265b4fef1619547006226bdb612c0f5b.jpg` | result | Cosmos-Transfer2.5-2B/robot/multiview-agibot |
| `images/0ebeec302593bbcc55336e98dd05362ea1f111d5ee6c3e0eae6ac03cbabe9275.jpg` | result | Cosmos-Transfer2.5-2B/robot/singleview-agibot |
| `images/407b0f13d6a7a1d1dcf33b3a67d844d0f6e2e271df2af952b006d012136258ed.jpg` | result | Cosmos-Transfer2.5-2B/robot/multiview |
| `images/921654ac99ed54db85d6cc76e0a305692529f0cff443a5fa72cef066cb00c877.jpg` | result | Cosmos-Transfer2.5-2B/robot/multiview |
| `images/4d3a27c9698411746032fdfb07ea058db8d8459050906edfb2b6fe582530b4ca.jpg` | result | Figure 18: View synchronization comparison. [Cosmos-Transfer2.5-2B/robot/multiview] generates more coherent videos across multiple viewpoints, compared with the single-view targeted baseline (the red dotted box highlights the inconsistent parts). |
| `images/35ef069abfb19064c1fcd1e9451d8d7f2be73c29426c711d0fc8f8ee92bbd03a.jpg` | result | Figure 18: View synchronization comparison. [Cosmos-Transfer2.5-2B/robot/multiview] generates more coherent videos across multiple viewpoints, compared with the single-view targeted baseline (the red dotted box highlights the inconsistent parts). |
| `images/055ffa12571d0f34d1f3b71d4394a8407990a5b866755cd4407af0fa561c54bc.jpg` | result | Figure 18: View synchronization comparison. [Cosmos-Transfer2.5-2B/robot/multiview] generates more coherent videos across multiple viewpoints, compared with the single-view targeted baseline (the red dotted box highlights the inconsistent parts). |
| `images/ed81c6ed213bb6f1a709a8d7ab07f344768aed319e868fd09897cf67ac3ce8c6.jpg` | result | Figure 19: [Cosmos-Predict2.5-2B/robot/multiview-agibot] generates synchronized robotic manipulation videos conditioned on single-frame input of 3-camera views and their corresponding camera trajectories. |
| `images/da14541f951820ea4084762f0aea16bb38c883aba7e59a85d6b3a884729da3ae.jpg` | result | Figure 20: Action-conditioned video prediction samples on the Bridge dataset. Comparison of predicted rollouts from [Cosmos-Predict2.5-2B/robot/action-cond] and [Cosmos-Predict1-7B-Video2World-Sample-ActionCond] against the ground-truth frames. [Cosmos-Predict2.5-2B/robot/action-cond] demonstrates b |
