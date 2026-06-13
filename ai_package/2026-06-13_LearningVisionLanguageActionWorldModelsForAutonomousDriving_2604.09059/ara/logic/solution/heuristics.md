# Heuristics

## H1: 采用 visual pretraining、SFT、GRPO 的渐进式训练，而不是直接用 RL 学完整多步推理。
- **Rationale**: 论文指出 SFT 为因果链和 coherent policies 提供冷启动基础，RL without cold-start supervision 难以在结构化多步推理任务的大搜索空间中有效导航。
- **Sensitivity**: 对阶段顺序敏感；跳过 SFT 会削弱后续 RL 的探索稳定性，跳过预训练会削弱 spatiotemporal understanding。
- **Bounds**: 只在完成视觉生成能力激活和 SFT 冷启动后进入 GRPO；不要把 RL 奖励反灌为预训练损失。
- **Code ref**: [3.3 Visual Pretraining；3.4 Supervised Fine-Tuning；3.5 Reinforcement Learning；Table 4。]
- **Source**: 论文正文训练策略与 ablation study。

## H2: 视觉预训练显式执行 multi-view consistency，而不是只生成 front view。
- **Rationale**: 论文称该设计让模型在 SFT 和 RL 阶段可为不同 camera viewpoint 生成 coherent future images，并形成统一 spatiotemporal prior。
- **Sensitivity**: 对相机视角覆盖和 goal-conditioned 指令敏感；如果只训练单视角，后续转向或不同视角请求时一致性会下降。
- **Bounds**: 输入应包含 multi-view image set、ego state 与描述 desired view 或 driving intent 的 instruction。
- **Code ref**: [3.3 Visual Pretraining of VLA-World；Eq. (5)。]
- **Source**: 论文 3.3 对 FSDrive 差异和多视角一致性的描述。

## H3: SFT 与 RL 输出采用结构化 causal reasoning sequence，按 Perception、Prediction、Visual、Think、Action、Answer 分段。
- **Rationale**: 论文把结构化输出作为 format reward 的约束，并让 imagined future 进入 think block 之后再决定 action 与 trajectory。
- **Sensitivity**: 对标签格式和 tag 完整性敏感；格式不合规会直接影响 rule-based verifiers 与下游轨迹解析。
- **Bounds**: 感知、短期预测、视觉 token、推理、高层动作和长期轨迹各自放在对应结构槽位中。
- **Code ref**: [3.5 Reinforcement Learning of VLA-World；B.1 SFT and RL Stages。]
- **Source**: 论文 3.5 Format Reward 与补充材料 B.1。

## H4: 短期预测使用 physics-grounded trajectory predictor，把历史惯性与任务意图做线性融合后再作为生成条件。
- **Rationale**: 论文称该模块为后续 frame generation 提供 robust geometric prior，并在 momentum-based continuity 与 intention-based maneuvering 之间切换。
- **Sensitivity**: 对历史轨迹、ego kinematics、mission goal 和自适应权重敏感；权重偏向历史会保守，偏向目标会更强调 maneuver。
- **Bounds**: 有效加速度由历史惯性项和 goal-conditioned acceleration 项融合，权重限制在论文给定区间内。
- **Code ref**: [A.2 Short-term Trajectory Prediction；Eq. (9)-(11)。]
- **Source**: 补充材料 A.2。

## H5: GRPO 使用 lightweight rule-based verifiers，而不是 neural reward model。
- **Rationale**: 论文称 verifier 覆盖 collision checking、generation quality、temporal consistency 和 strict output structure，可降低高维视觉动态下的训练负担。
- **Sensitivity**: 对 verifier 设计敏感；奖励若只看格式或视觉 token，可能不足以优化最终 driving safety。
- **Bounds**: 奖励至少覆盖 format、short-term prediction、visual constraint、action 和 trajectory 几类组件。
- **Code ref**: [3.5 Reinforcement Learning；A.1 Group Relative Policy Optimization。]
- **Source**: 论文 3.5 与补充材料 A.1。

## H6: Visual Constrain Reward 要求 visual tokens 数量符合重建长度且每个 token 属于 valid visual codebook。
- **Rationale**: 论文说明该约束保证生成帧可解码且 meaningful，避免视觉 token 无法重建。
- **Sensitivity**: 对 visual tokenizer 与 codebook 边界敏感；无效 token 或长度错误会破坏未来帧生成。
- **Bounds**: 只接受可由 VQGAN visual tokenizer 解码的 token 序列。
- **Code ref**: [3.3 Visual Pretraining；3.5 Visual Constrain Reward。]
- **Source**: 论文 3.3 与 3.5。
