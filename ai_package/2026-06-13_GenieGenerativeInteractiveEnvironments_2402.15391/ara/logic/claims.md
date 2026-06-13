# Claims

## C1: 视频-only 训练仍能形成可交互世界模型
- **Statement**: Genie 将 latent action model、video tokenizer 与 dynamics model 组合起来，在没有 ground-truth action labels 或 text annotations 的训练条件下，仍能通过 learned latent action space 进行逐帧控制。
- **Status**: supported
- **Falsification criteria**: 若在相同视频-only 条件下，替换或移除 learned latent action space 后仍不能产生一致可控的下一帧，或需要 action labels 才能控制，则该主张被削弱。
- **Proof**: [E1, E7]
- **Evidence basis**: ['E1', 'E7']
- **Interpretation**: 该主张定义了 Genie 区别于传统 World Models 与 Video Models 的核心范围：训练输入只依赖视频，但推理时提供可由用户选择的离散 latent actions。
- **Tags**: ['descriptive', 'scoping']

## C2: Pixel-input 的 latent action model 更有利于可控性
- **Statement**: 相比 token-input 版本，使用原始图像作为 latent action model 输入的 Pixel-input Genie 在两个评估环境中表现出更高的 controllability。
- **Status**: supported
- **Falsification criteria**: 若在相同 dynamics model、tokenizer、数据与评估流程下，token-input 在 ΔPSNR 上稳定优于 Pixel-input，则该设计判断不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 论文将差异解释为 tokenization 可能丢失了与视频动态和运动相关的信息，因此让 LAM 直接读取 raw videos 更适合学习控制信号。
- **Tags**: ['improvement', 'causal']

## C3: ST-ViViT tokenizer 提升生成质量与可控性
- **Statement**: 在 tokenizer architecture ablation 中，ST-ViViT 相比 spatial-only ViT 与 C-ViViT 同时带来更好的 video generation fidelity 与 controllability。
- **Status**: supported
- **Falsification criteria**: 若在相同 patch size、batch size、sequence length 以及后续 dynamics 和 latent action model 下，ViT 或 C-ViViT 在 FVD 与 ΔtPSNR 上整体优于 ST-ViViT，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该结果支持论文对 ST-transformer tokenizer 的设计选择：它在引入时间信息的同时避免 C-ViViT 的 full space-time attention 计算和过拟合问题。
- **Tags**: ['improvement', 'causal']

## C4: 数据筛选质量优先于原始规模
- **Statement**: 对 Platformers 数据进行 curated filtering 后，虽然数据量更小，但训练出的模型在 FVD 上优于使用 original dataset 的模型。
- **Status**: supported
- **Falsification criteria**: 若同等模型规模和训练设置下，original dataset 在 FVD 上持续优于 curated dataset，则筛选流程的价值被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 论文将该现象与 prior work 的结论保持一致：高质量数据比单纯增加数量更重要。
- **Tags**: ['improvement', 'causal']

## C5: 模型与 batch 扩展改善训练表现
- **Statement**: 在固定 tokenizer 与 action model 的 scaling studies 中，增大 dynamics model 尺寸以及增大 batch size 均带来更有利的训练表现趋势。
- **Status**: supported
- **Falsification criteria**: 若扩展 model size 或 batch size 后训练损失不下降或明显恶化，则该 scaling 结论不成立。
- **Proof**: [E5, E6]
- **Evidence basis**: ['E5', 'E6']
- **Interpretation**: 该主张主要来自 Figure 9 的趋势描述，Table 10 和 Table 12 提供了对应 scaling 与最终模型的架构和 compute usage 背景。
- **Tags**: ['improvement', 'generalization']

## C6: Genie 的 learned latent actions 可迁移到 imitation from observation
- **Statement**: 冻结的 Genie LAM 可为 unseen videos 推断 latent action labels，并支持在 CoinRun 中训练 LAM-based policy，其表现可接近 oracle BC 的上界。
- **Status**: supported
- **Falsification criteria**: 若使用 frozen LAM 标注的 latent actions 无法支持 policy 在 held out CoinRun 测试中明显优于 random agent，或需要大量 ground-truth actions 才能工作，则该迁移主张被削弱。
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: 该实验说明 learned latent action space 不只是生成控制接口，也可作为 action-free videos 到 agent policy 的中间表示。
- **Tags**: ['generalization', 'descriptive']

## C7: Robotics 视频也能学习一致 latent actions
- **Statement**: 在 Robotics dataset 上训练的 Genie 变体能够从无 action labels 的视频中学习 distinct and consistent actions，并生成可控的 robotic trajectories。
- **Status**: supported
- **Falsification criteria**: 若在 Robotics videos 上训练后，相同 latent action 在不同 prompt frames 中没有一致语义或无法控制轨迹，则该跨域泛化主张不成立。
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 该结果将 Genie 的 video-only latent action 学习从 Platformers 扩展到 robotic manipulation 场景。
- **Tags**: ['generalization', 'descriptive']
