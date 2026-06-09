# Claims

## C1: 动作正则化提升世界模型生成质量
- **Statement**: 在 CALVIN 基准验证集上进行 50 步开环想象对比，WAM 在 PSNR、SSIM、LPIPS、FVD 四项生成质量指标上全面优于 DreamerV2 基线，且 WAM 使用的训练步数远少于基线。
- **Status**: supported
- **Falsification criteria**: 若在相同验证集上 WAM 的 PSNR/SSIM 不高于、LPIPS/FVD 不低于 DreamerV2，则本主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 逆动力学头迫使编码器预测状态转移动作，将动作相关结构编码进潜表示，从而提升了未来视觉状态的预测保真度，而非仅为像素重建服务。
- **Tags**: ['improvement', 'causal']

## C2: WAM 表示提升行为克隆阶段的策略成功率
- **Statement**: 在相同策略架构（DiffusionMLP）和训练超参数下，使用 WAM 特征训练的扩散策略在 CALVIN 8 个操控任务的行为克隆阶段，平均成功率高于使用 DreamerV2 特征的 DiWA 基线，8 个任务中 7 个取得更高成功率，关节型操控任务（如抽屉开关、滑轨移动）提升幅度最为显著。
- **Status**: supported
- **Falsification criteria**: 若控制策略架构和训练超参数后 WAM 平均 BC 成功率不高于 DiWA，则本主张不成立；摘要所引 59.4%→71.2% 与 Table III 及结论所引 45.8%→61.7% 数值不一致，本主张以 Table III 为准。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 动作感知的编码器输出 e_t 塑造后验 z_t，进而使特征 f_t 携带更丰富的动作相关信息，行为克隆直接从更优质的表示中获益，无需修改策略架构或训练流程。
- **Tags**: ['improvement', 'causal']

## C3: WAM 表示提升模型内 PPO 精调后的策略成功率
- **Statement**: 在冻结世界模型潜空间中进行 800 轮 PPO 精调后，WAM 在 8 个 CALVIN 任务上的平均成功率高于 DiWA 基线，其中两个任务达到 100% 成功，精调所需的总物理交互次数均为零。
- **Status**: supported
- **Falsification criteria**: 若 PPO 精调后 WAM 在 8 任务上的平均成功率不高于 DiWA 对应均值，则本主张不成立；论文正文所引 DiWA PPO 均值 79.8% 与从 Table IV 各行数据推算的均值（约 83.7%）存在不一致，前者可能为 DiWA 原文报告值，后者为本文复现值，以 Table IV 各行数值为准。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: WAM 先验分布 z_hat_t 经 KL 损失传播了动作感知结构，使想象回放中的潜状态质量更高，PPO 精调面临更利于策略提升的优化景观。
- **Tags**: ['improvement']

## C4: WAM 以远少于基线的训练步数实现更强下游策略性能
- **Statement**: WAM 世界模型使用约为基线 DreamerV2 八分之一强的训练步数（约 230K 对比约 2M 步，论文报告约 8.7 倍差距），即可在行为克隆和 PPO 精调两个阶段均取得更高任务成功率。
- **Status**: supported
- **Falsification criteria**: 若在相同训练步数条件下 WAM 不优于基线，或训练步数比与实际记录不符，则样本效率主张不成立。
- **Proof**: [E2, E3]
- **Evidence basis**: ['E2', 'E3']
- **Interpretation**: 逆动力学正则化加速了有效动作感知表示的学习，使世界模型在更短训练时间内即可为下游策略提供高质量特征，论文将此作为 WAM 的实用优势之一明确陈述。
- **Tags**: ['improvement', 'scoping']

## C5: 逆动力学头通过「级联效应」将动作结构传递至先验分布
- **Statement**: WAM 选择在编码器嵌入 e_t 而非 RSSM 特征 f_t 上附加动作预测头，由此形成「编码器→后验 z_t→先验 z_hat_t」的级联传播链，确保推理期仅依赖先验的想象回放同样携带动作相关信息。
- **Status**: supported
- **Falsification criteria**: 若在 f_t 而非 e_t 上附加动作头（使动作预测平凡可解），或移除 KL 正则化，则级联通路断裂，先验中应不含动作感知结构。
- **Proof**: [E1, E3]
- **Evidence basis**: ['E1', 'E3']
- **Interpretation**: 论文将「在 e_t 而非 f_t 上预测动作」明确标注为避免「平凡可解」问题的关键设计选择——f_t 已通过 GRU 接收 a_{t-1}，在其上预测动作不会迫使编码器学习有意义结构。此级联设计属于论文显式声明的因果机制。
- **Tags**: ['causal', 'descriptive']
