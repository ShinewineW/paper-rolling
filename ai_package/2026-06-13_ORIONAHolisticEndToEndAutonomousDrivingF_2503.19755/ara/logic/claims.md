# Claims

## C1: Bench2Drive闭环主结果
- **Statement**: ORION在Bench2Drive base set闭环评测中相对既有E2E-AD方法取得更优的Driving Score与Success Rate，并在相同NC条件与相机模态下超过DriveTransformer-Large。
- **Status**: supported
- **Falsification criteria**: 若在相同Bench2Drive base set、相同官方闭环协议与相同输入条件下，ORION不再优于表中主要基线，则该主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 论文将该结果归因于将VLM推理空间与轨迹动作空间对齐，使语义推理能够指导数值轨迹生成。
- **Tags**: ['improvement']

## C2: 多能力评测表现
- **Statement**: ORION在Bench2Drive多能力评测的平均能力上领先主要闭环基线，并在Overtaking、Emergency Brake与Traffic Sign能力上表现突出；但在Merging与Give Way上落后于DriveAdapter。
- **Status**: supported
- **Falsification criteria**: 若按同一Multi-Ability协议复测后，ORION的平均能力不领先主要基线，或Merging与Give Way不再呈现论文所述短板，则该主张需修正。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文认为强项体现了VLM对自车、动态元素和静态交通元素因果交互的理解；弱项可能来自变道决策时机更复杂。
- **Tags**: ['improvement', 'descriptive']

## C3: 生成式规划器选择
- **Statement**: 在ORION框架中，VAE式生成规划器相对Diffusion式生成规划器在闭环、开环和能力均值指标上整体更优。
- **Status**: supported
- **Falsification criteria**: 若仅替换生成规划器并保持其余设置一致时，Diffusion达到或超过VAE的主要闭环与能力指标，则该主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 论文解释为VAE潜在空间更直接地把VLM推理信息对齐到多模态动作空间，且训练过程更稳定。
- **Tags**: ['causal', 'improvement']

## C4: QT-Former设计有效性
- **Statement**: QT-Former中的交通状态监督、运动预测与Memory Bank等设计共同提升闭环表现；同样设计下，Instructed Generator输出方式明显优于Plain Text输出方式。
- **Status**: supported
- **Falsification criteria**: 若逐步加入这些QT-Former设计后闭环指标不提升，或Plain Text输出在相同设计下不低于Instructed Generator，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 论文认为交通状态理解有助于减少闭环违规，Memory Bank与历史QA监督让模型受益于长时视觉记忆。
- **Tags**: ['causal', 'improvement']

## C5: 历史查询数量影响
- **Statement**: 历史查询数量对ORION存在非单调影响；适量历史查询能提升闭环表现，继续增加会使性能下降。
- **Status**: supported
- **Falsification criteria**: 若在相同训练设置下增加历史查询数量始终带来单调提升，或不存在性能下降拐点，则该主张不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 论文推断过多历史查询会妨碍VLM捕获当前帧特征，而当前帧信息在驾驶场景中更关键。
- **Tags**: ['causal', 'descriptive']

## C6: 辅助VQA与规划联合训练
- **Statement**: 单独训练VQA或规划任务无法同时获得两类能力，而联合训练能同时保持规划与语言侧能力。
- **Status**: supported
- **Falsification criteria**: 若单任务训练已经同时达到联合训练的规划与语言指标，或联合训练不再改善规划任务，则该主张不成立。
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 论文据此认为Chat-B2D自动生成数据具有有效性，并且联合任务训练促进推理与规划空间的对齐。
- **Tags**: ['causal', 'improvement']

## C7: nuScenes开环泛化边界
- **Statement**: 在nuScenes开环规划评测中，修改后的ORION相对部分经典非VLM方法表现可比，但相对若干VLM-Based方法并非最优。
- **Status**: supported
- **Falsification criteria**: 若在同一nuScenes协议下ORION全面领先VLM-Based方法，或无法达到经典非VLM方法的可比区间，则该边界判断需修正。
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 论文将该现象归因于VAE潜在空间更适合Bench2Drive的多模态轨迹分布，而nuScenes更偏单模态分布。
- **Tags**: ['generalization', 'scoping']

## C8: 渐进式训练策略
- **Statement**: 三阶段训练策略逐步对齐vision、language与action空间，并在消融中优于直接进行规划相关训练。
- **Status**: supported
- **Falsification criteria**: 若取消早期空间对齐阶段后最终闭环结果不下降，或三阶段设置不再取得最佳闭环表现，则该主张不成立。
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: 论文把训练流程设计为先对齐视觉与语言，再对齐语言与动作，最后进行端到端联合微调。
- **Tags**: ['causal', 'improvement']
