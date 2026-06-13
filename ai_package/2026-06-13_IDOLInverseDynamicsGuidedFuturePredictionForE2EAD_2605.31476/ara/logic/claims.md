# Claims

## C1: 逆动力学把未来预测转化为可执行规划信号
- **Statement**: IDOL 的核心主张是：仅预测未来潜在 BEV 状态不足以稳定改善规划，显式解码相邻未来状态之间的转移可以生成面向轨迹优化的运动线索。
- **Status**: supported
- **Falsification criteria**: 若去掉 IDM 后闭环规划指标不下降，或用未来状态本身即可达到同等效果，则该主张被削弱。
- **Proof**: [E3, E6]
- **Evidence basis**: ['E3', 'E6']
- **Interpretation**: 主文消融和附录消融共同支持这一点：学习式 IDM 优于无 IDM、Future State Only 与 Latent Difference，说明收益不只是来自访问未来状态，而是来自显式转移建模。
- **Tags**: ['causal', 'improvement']

## C2: 闭环细化提升长时域一致性但存在过度修正风险
- **Statement**: IDOL 使用轻量闭环细化，将更新后的规划查询重新送入未来推理；论文认为这能改善长时域一致性，但过多迭代可能带来过度修正。
- **Status**: supported
- **Falsification criteria**: 若增加闭环迭代不带来指标改善，或更多迭代持续更优而无性能回落，则该主张需要修正。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Table 3 显示加入闭环细化优于仅使用 IDM，同时更多迭代略降，符合论文对闭环收益与过度修正的解释。
- **Tags**: ['causal', 'improvement']

## C3: 相邻两帧转移是更紧凑的 IDM 时间输入
- **Statement**: 论文主张，相邻两帧 BEV 转移比更长未来窗口更适合即时规划细化，因为长窗口可能稀释局部转移线索。
- **Status**: supported
- **Falsification criteria**: 若更长时间窗口在相同设置下稳定优于两帧输入，则该时间设计假设不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 4 的时间输入消融支持相邻转移作为更紧凑有效的规划细化依据。
- **Tags**: ['causal', 'descriptive']

## C4: 空间与全局动态分支互补
- **Statement**: IDOL 的逆动力学反馈同时保留空间动态图和全局动态特征；论文认为空间分支提供局部转移证据，全局分支提供整体校准，二者结合效果最好。
- **Status**: supported
- **Falsification criteria**: 若移除任一分支不影响或反而提升整体规划指标，则双分支互补性被削弱。
- **Proof**: [E4, E6]
- **Evidence basis**: ['E4', 'E6']
- **Interpretation**: Table 5 证明双分支优于只保留单一分支；Table 11 进一步表明全局动态特征的融合方式也会影响查询校准质量。
- **Tags**: ['causal', 'improvement']

## C5: IDOL 在 NAVSIM 多个设置上达到可比学习式方法中的领先表现
- **Statement**: 论文声称 IDOL 在 NAVSIM v1 navtest、NAVSIM v2 navtest、navhard stage-1-only 与两阶段 navhard 评测中，在可比学习式规划器里表现领先。
- **Status**: supported
- **Falsification criteria**: 若在相同官方闭环协议和可比输入设置下，多个强基线超过 IDOL 的主指标，则该泛化主张不成立。
- **Proof**: [E1, E2, E5]
- **Evidence basis**: ['E1', 'E2', 'E5']
- **Interpretation**: 主表与附录表覆盖标准场景和更困难长尾场景，支持论文关于鲁棒性与跨设置稳定性的结论；PDM-Closed 被论文单列为使用 ground-truth perception 的 privileged planner。
- **Tags**: ['generalization', 'improvement']
