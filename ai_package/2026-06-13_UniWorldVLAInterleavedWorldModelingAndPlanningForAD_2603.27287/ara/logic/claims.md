# Claims

## C1: NAVSIM 主结果支持整体有效性
- **Statement**: Uni-World VLA 在 NAVSIM 测试划分上相对传统端到端方法与世界模型方法取得更强的闭环规划综合表现，同时保持有竞争力的未来视频生成质量。
- **Status**: supported
- **Falsification criteria**: 若在同一 NAVSIM 协议、同一指标下，Uni-World VLA 的 PDMS 不再领先，或其 FVD 明显劣于表中世界模型基线，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 表中结果表明，该方法并非只优化规划或只优化生成，而是在闭环规划指标与视频生成指标之间取得较好的联合表现。
- **Tags**: ['improvement', 'generalization']

## C2: 交错 frame-action 生成优于替代生成顺序
- **Statement**: 将未来帧与动作按评测频率对齐并严格交错生成，比高频动作帧交替、滑动动作窗口等替代生成方案带来更好的规划表现。
- **Status**: supported
- **Falsification criteria**: 若在相同训练设置、无 depth fusion、同一 NAVSIM 评测协议下，其他生成 scheme 的 PDMS 或关键子指标稳定超过 Scheme E，则该主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Table 4 将生成顺序作为主要变量，支持论文关于时间一致性与评测协议匹配有利于规划质量的解释。
- **Tags**: ['causal', 'improvement']

## C3: depth fusion 改善未来帧质量并补充规划收益
- **Statement**: 在预训练与未来帧建模均启用时，加入 Depth Anything 3 提供的 monocular depth 信息并通过 cross-attention 融合，可改善未来帧生成质量，并在部分规划子指标上带来补充收益。
- **Status**: supported
- **Falsification criteria**: 若去除 depth fusion 后 FVD 不升高，或加入 depth fusion 后规划与生成指标没有一致改善，则该主张被削弱。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: Table 3 的 ablation 将 depth 作为单独变量，显示 depth 对视频质量尤其关键；规划指标则体现为整体组合最优和部分子指标提升。
- **Tags**: ['causal', 'improvement']

## C4: 历史视觉信息的 context 与 dynamic 互补
- **Statement**: 同时使用 contextual tokens 与 dynamic tokens 的历史视觉信息，比只使用 dynamic tokens 更稳健；较长历史在整体规划与生成质量上更有优势。
- **Status**: supported
- **Falsification criteria**: 若仅 dynamic tokens 或较短历史在相同协议下稳定取得更好的 PDMS 与 FVD，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 5 支持论文对 contextual tokens 提供空间语义、dynamic tokens 提供运动线索的解释；两类信息结合形成更均衡的表现。
- **Tags**: ['descriptive', 'improvement']
