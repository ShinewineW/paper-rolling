# Claims

## C1: 统一的 Cosmos-Predict2.5 世界生成模型
- **Statement**: Cosmos-Predict2.5 采用 flow matching 架构，并将 Text2World、Image2World 与 Video2World 统一到单一模型中，用 Cosmos-Reason1 提供更丰富的文本表征与更细粒度控制。
- **Status**: supported
- **Falsification criteria**: 若统一模型在 Text2World、Image2World 或 Video2World 任一设置下无法完成论文所述生成任务，或并未使用 Cosmos-Reason1 文本表征，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该主张界定了本文核心系统边界：一个基础模型覆盖多种世界生成条件，而不是为每种输入模式维护完全分离的生成器。
- **Tags**: ['descriptive', 'scoping']

## C2: RL 后训练提升生成奖励与人类偏好
- **Statement**: 在 VideoAlign 奖励模型下进行强化学习后，Cosmos-Predict2.5-2B 在 Text2World 与 Image2World 设置中的文本对齐、运动质量、视觉质量综合奖励整体提高，论文还报告 RL 生成结果在人工投票中平均更受偏好。
- **Status**: supported
- **Falsification criteria**: 若相同 PAI-Bench 设置下 RL 后模型的综合奖励不高于 RL 前模型，或人工偏好不再倾向 RL 模型，则该改进主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 证据支持 RL 后训练作为质量与对齐改进步骤，但奖励模型本身仍是代理指标，人工投票提供了互补验证。
- **Tags**: ['improvement', 'causal']

## C3: 时间步蒸馏保持相近质量并减少推理步数
- **Statement**: rCM 时间步蒸馏后的 Cosmos-Predict2.5-2B 在 PAI-Bench Text2World 与 Image2World 上取得与 teacher 相近的定量结果，论文称其可用更少步骤生成高保真样本。
- **Status**: supported
- **Falsification criteria**: 若 distilled 模型在同一基准上相对 teacher 出现明显质量退化，或无法按论文所述低步数采样，则该主张被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该结果说明蒸馏主要面向推理效率，同时保持自动基准质量接近原模型。
- **Tags**: ['improvement']

## C4: PAI-Bench 上的 Predict2.5 后训练模型具有竞争力
- **Statement**: 在 PAI-Bench-Predict 的 Text2World 和 Image2World 基准中，Cosmos-Predict2.5 post-trained 模型相对自身 pre-trained 版本提升，并在 Image2World 中达到论文所称最佳表现。
- **Status**: supported
- **Falsification criteria**: 若同一评测协议下 post-trained 版本不优于 pre-trained 版本，或 Image2World 排名不再领先，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 该主张把训练配方的收益落到公开式自动基准上，体现基础模型对物理 AI 生成任务的泛化表现。
- **Tags**: ['improvement', 'generalization']

## C5: Cosmos-Transfer2.5 提升多控制模态转译质量
- **Statement**: Cosmos-Transfer2.5-2B 在 PAIBench-Transfer 的多种控制配置中，相比 Cosmos-Transfer1-7B 展示更好的整体质量，并在单模态与均匀权重多模态设置中改善多项控制对齐指标。
- **Status**: supported
- **Falsification criteria**: 若相同控制模态与评测指标下 Cosmos-Transfer2.5-2B 不再优于 Cosmos-Transfer1-7B，则该主张被削弱。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 结果支持较小 Transfer2.5 模型在控制输入遵循和视频质量之间取得更好的权衡。
- **Tags**: ['improvement']

## C6: Transfer2.5 增强真实机器人策略泛化
- **Statement**: 用 Cosmos-Transfer2.5-2B 生成的视觉增强数据训练策略后，真实机器人在多种未见物体与环境变化场景中的成功率高于仅用原始演示或标准图像增强的策略。
- **Status**: supported
- **Falsification criteria**: 若相同机器人任务与测试场景中 Proposed 策略未超过 Base 或 Baseline 策略，则该主张不成立。
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 该实验把世界模型从视频质量推进到下游控制性能，说明语义级视觉增强可覆盖标准图像增强难以表达的环境变化。
- **Tags**: ['generalization', 'causal']

## C7: 多视角驾驶仿真提升视觉质量与控制遵循
- **Statement**: Cosmos-Predict2.5 和 Cosmos-Transfer2.5 的多视角驾驶版本在 RDS-HQ-HL 生成视频评测中，相比上一代模型改善 FVD、FID 等视觉指标，并在车道与三维框检测指标上提升控制遵循。
- **Status**: supported
- **Falsification criteria**: 若相同 RDS-HQ-HL 协议下视觉指标或检测指标未优于上一代基线，则该主张被削弱。
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 该结果表明多视角世界生成不仅追求逼真度，也用下游感知检测作为控制信号遵循的代理验证。
- **Tags**: ['improvement', 'generalization']

## C8: 动作条件机器人视频预测优于上一代并验证 TimeEmbedding 设计
- **Statement**: Cosmos-Predict2.5-2B/robot/action-cond 在 Bridge 数据集上优于 Cosmos-Predict1 动作条件基线；消融显示通过 TimeEmbedding 注入动作优于 CrossAtten 与 ChannelConcat。
- **Status**: supported
- **Falsification criteria**: 若相同 Bridge 测试协议下 Predict2.5 动作条件模型不优于 Predict1 基线，或 TimeEmbedding 不再优于其他注入方式，则该主张不成立。
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: 该结论同时覆盖模型代际提升与动作条件注入位置的设计选择。
- **Tags**: ['improvement', 'causal']
