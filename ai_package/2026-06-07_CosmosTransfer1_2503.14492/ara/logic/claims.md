# Claims

## C1: 多模态控制相比单模态控制整体生成质量更高
- **Statement**: 在均匀权重设置下融合全部四种模态（Vis、Edge、Depth、Seg）的多模态控制模型，在整体生成质量（Quality Score）上优于所有单模态控制模型，并在深度对齐上取得最佳结果。
- **Status**: 支持
- **Falsification criteria**: 若存在单模态模型在TransferBench全指标上均优于多模态均匀融合模型，则该论断不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 各模态提供互补信息：密集结构模态（Vis/Edge）保障对齐，稀疏几何模态（Depth/Seg）提升多样性；融合后互补优势叠加，Quality Score超越任一单模态配置。
- **Tags**: ['improvement', 'causal']

## C2: 时空控制图实现逐区域模态权重细粒度控制
- **Statement**: 通过对前景/背景区域赋予不同模态权重，时空控制图可独立调节各区域的对齐度与多样性，且模态权重与对应区域对齐指标呈强相关（Pearson相关系数绝对值达0.92-0.93）。
- **Status**: 支持
- **Falsification criteria**: 若模态权重变化与对应区域对齐指标之间不存在显著相关性，则该论断不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文展示了前景Vis权重从0提升至0.5时前景Blur SSIM的提升，及背景Depth权重变化与背景Depth si-RSME强负相关，验证了时空权重对输出的因果作用。
- **Tags**: ['causal', 'descriptive']

## C3: 分支独立训练后推理时融合在内存效率与灵活性上更优
- **Statement**: 将各模态控制分支独立训练、推理时融合，相比同时训练所有分支，具有更低的显存需求、支持模态异构数据训练，并允许在推理时任意增减模态。
- **Status**: 描述性设计论断（论文未提供直接对比实验）
- **Falsification criteria**: 若联合训练所有分支的显存占用与分别训练相当，且灵活性不受影响，则内存效率优势论断不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该论断为论文设计动机的定性陈述，未提供联合训练的对比实验；（分析推断，论文未显式声明）实际优势来自大规模视频训练场景下的工程约束，每个分支仅需在训练时独占显存。
- **Tags**: ['causal', 'scoping']

## C4: 64块B200 GPU并行推理可实现实时视频生成
- **Statement**: 利用NVIDIA GB200 NVL72机架（64块B200 GPU），采用数据并行与注意力头并行策略，Cosmos-Transfer1-7B可在4.2秒内生成5秒的720p视频，从而达到实时生成吞吐量。
- **Status**: 支持
- **Falsification criteria**: 若在相同64块B200 GPU配置下端到端生成时间超过5秒，则实时论断不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 加速效果主要来自扩散步骤并行化（占总工作量99%以上），从1到64 GPU约实现40倍加速。端到端时间与纯扩散时间接近，说明非扩散部分开销极小。
- **Tags**: ['improvement', 'scoping']

## C5: 密集结构模态与稀疏几何模态在对齐度与多样性上存在系统性权衡
- **Statement**: 提供密集结构信息的Vis和Edge模态在排除时使多样性显著提升；Depth和Segmentation模态在排除时对多样性影响较小；密集模态约束生成自由度，稀疏模态留有更大创作空间。
- **Status**: 支持
- **Falsification criteria**: 若排除Vis/Edge与排除Depth/Seg对多样性指标的影响无系统性差异，则该权衡论断不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 基于TransferBench实验结果的归纳，论文明确分析了模态密度与多样性之间的关系，适用于指导实际应用中的模态选择策略。
- **Tags**: ['descriptive', 'generalization']

## C6: 机器人Sim2Real场景中时空控制图设置优于单模态模型
- **Statement**: 在机器人操作Sim2Real数据生成任务中，使用时空控制图的多模态设置（Setting1/Setting2）在前景机器人保留度（FG Mask mIoU）和整体质量（Quality Score）上均优于所有单模态基线。
- **Status**: 支持
- **Falsification criteria**: 若单模态模型在FG Mask mIoU和Quality Score上均优于时空控制图设置，则该论断不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Setting2（前景仅Edge、背景仅Seg）在Quality Score上取得所有配置最高分，Setting1和Setting2在FG Mask mIoU上均优于所有单模态模型，验证了时空控制图对前景保真的有效性。
- **Tags**: ['improvement', 'causal']

## C7: 自动驾驶场景中HDMap与LiDAR融合优于单独使用任一模态
- **Statement**: 在自动驾驶视频生成任务中，同时使用HDMap和LiDAR的多模态模型在车道线精度（Lane mIoU）上优于单独使用LiDAR，在三维一致性（重投影误差）上优于单独使用HDMap，实现更均衡的综合性能。
- **Status**: 支持
- **Falsification criteria**: 若单独使用HDMap或LiDAR在所有指标上均不劣于融合模型，则融合优势论断不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: HDMap提供精确车道信息但缺乏3D感知，LiDAR提供3D深度信息但缺乏车道语义；融合后互补，Lane mIoU超越两者中最优，重投影误差接近LiDAR最优。
- **Tags**: ['improvement', 'causal']
