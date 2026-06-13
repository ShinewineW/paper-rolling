# Claims

## C1: NAVSIM 闭环规划性能
- **Statement**: DriveVA 在 NAVSIM Navtest 闭环指标上优于论文比较的传统端到端方法和 WorldModel Methods。
- **Status**: 支持
- **Falsification criteria**: 若在相同 NAVSIM Navtest 设置下，DriveVA 的闭环聚合指标不再高于比较方法，或输入与评估协议不一致，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Table 1 给出闭环指标对比，作者将提升归因于统一的 video-action 生成形式，使想象的未来与规划动作更一致。
- **Tags**: ['improvement', 'descriptive']

## C2: 零样本跨数据集与跨域泛化
- **Statement**: 在从 NAVSIM 训练后直接评估到 nuScenes 与 Bench2Drive 的零样本设置中，DriveVA 相比论文中的 WorldModel Methods 表现更强。
- **Status**: 支持
- **Falsification criteria**: 若目标域进行了微调，或在相同零样本协议下平均位移误差与碰撞率不优于对应基线，则该主张不成立。
- **Proof**: [E2, E3]
- **Evidence basis**: ['E2', 'E3']
- **Interpretation**: Table 2 和 Table 3 支持作者关于跨数据集与 real-to-simulation 转移的说法，且 Table 3 进一步显示其在未进行 nuScenes finetune 时仍可与已 finetune 的方法比较。
- **Tags**: ['generalization', 'improvement']

## C3: 视频轨迹一致性
- **Statement**: DriveVA 生成的视频所隐含的运动与模型预测轨迹保持较强一致性。
- **Status**: 支持
- **Falsification criteria**: 若独立视觉里程计从生成视频恢复的轨迹与模型预测轨迹偏离明显，或定性案例中频繁出现视频演化与轨迹方向不一致，则该主张被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 4 使用 DPVO 重建作为外部验证，Fig. 4 和 Fig. 7 提供定性支撑；这说明轨迹不是独立下游规划器输出，而与生成视频共享同一 rollout。
- **Tags**: ['descriptive', 'causal']

## C4: 视频监督与双预测是关键设计
- **Statement**: 显式视频监督、Video Continuation、双向 video-action 交互以及 dual-prediction 对闭环规划表现有重要作用。
- **Status**: 支持
- **Falsification criteria**: 若去除 Video Loss、Video Continuation、双向交互或未来视频预测后性能不降，或替代训练策略在相同设置下达到相同表现，则该设计因果解释被削弱。
- **Proof**: [E5, E6, E7, E8, E9, E10]
- **Evidence basis**: ['E5', 'E6', 'E7', 'E8', 'E9', 'E10']
- **Interpretation**: Table 5、Table 6、Table 7、Table 8、Table 9 和 Table 10 从关键模块、未来帧数、训练策略、采样步数、模型规模与 dual-prediction 多个角度支撑该结论。
- **Tags**: ['causal', 'improvement']

## C5: 预训练视频模型适合作为 driving world model 基础
- **Statement**: DriveVA 将 Wan2.2-TI2V-5B 的视频先验用于联合未来视频与动作建模，论文认为这有助于学习可迁移的时空动态。
- **Status**: 支持
- **Falsification criteria**: 若从头训练或轻量适配在相同协议下不弱于完整微调，或零样本结果不能复现，则视频先验带来的迁移解释会被削弱。
- **Proof**: [E7, E9]
- **Evidence basis**: ['E7', 'E9']
- **Interpretation**: Table 7 与 Table 9 显示训练策略与模型规模相关差异；作者据此认为有效迁移需要在 joint video-level supervision 下端到端适配视频先验。
- **Tags**: ['scoping', 'generalization']
