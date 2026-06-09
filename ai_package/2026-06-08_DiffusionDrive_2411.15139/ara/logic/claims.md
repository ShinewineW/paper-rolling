# Claims

## C1: 截断扩散策略将去噪步数减少10倍并消除模式崩塌
- **Statement**: 提出截断扩散策略，将去噪起点从纯高斯噪声改为锚定高斯分布，使去噪步数从20步缩减至2步（相比原始扩散策略减少10倍），同时将模式多样性得分D从11%提升至74%，FPS从7提升至45
- **Status**: verified
- **Falsification criteria**: 若在相同2步去噪配置下，截断扩散策略的模式多样性得分D与原始扩散策略相近（均约11%），或FPS未达到实时水平，则该主张不成立
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 截断扩散通过将扩散时间表截断至仅扩散50/1000步，使起点为「锚点+少量高斯噪声」，而非纯随机噪声，从而既压缩了需遍历的扩散步数，也赋予了多模式先验结构，两个问题同时得到解决
- **Tags**: ['improvement', 'causal']

## C2: DiffusionDrive在NAVSIM navtest上以88.1 PDMS创造新记录并以45 FPS实时运行
- **Statement**: 使用对齐的ResNet-34骨干网络，DiffusionDrive在NAVSIM navtest分割上达到88.1 PDMS，超越所有先前方法，且不依赖后处理，同时在NVIDIA 4090上以45 FPS运行
- **Status**: verified
- **Falsification criteria**: 若使用相同骨干且无后处理的其他方法在navtest分割上PDMS超过88.1，或NVIDIA 4090上FPS低于实时阈值，则该主张不成立
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: DiffusionDrive仅用20个锚点和2步去噪即超越了使用8192个锚点并附加后处理的Hydra-MDP-V8192-W-EP（86.5 PDMS），体现了扩散模型分布表达能力对大规模词汇表的替代优势
- **Tags**: ['improvement', 'descriptive']

## C3: 原始扩散策略直接适配驾驶场景时出现严重模式崩塌
- **Statement**: 将原始DDIM扩散策略（Transfuser_DP）应用于自动驾驶时，从不同高斯噪声采样的20条轨迹在去噪后高度重叠，模式多样性得分D仅为11%；同时20步去噪使FPS从60降至7，无法满足实时需求
- **Status**: verified
- **Falsification criteria**: 若Transfuser_DP的模式多样性得分D显著高于11%，或在NAVSIM场景中体现出与DiffusionDrive相当的轨迹多样性，则该问题描述不成立
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 驾驶场景的强场景条件约束（道路几何、交通规则）使多个随机噪声收敛至同一局部极值；与机器人操控高维动作空间不同，驾驶轨迹空间维度相对较低，导致模式崩塌更为突出
- **Tags**: ['descriptive', 'causal']

## C4: 级联扩散解码器以更少参数实现更优规划质量
- **Statement**: 提出的基于Transformer的扩散解码器，通过稀疏可变形空间交叉注意力（BEV/PV特征）、智能体/地图查询交叉注意力及级联精化机制，在减少39%参数（102M→60M）的同时将PDMS提升2.4分（85.7→88.1）
- **Status**: verified
- **Falsification criteria**: 若消融掉空间交叉注意力或级联机制后PDMS无明显下降，则各子模块贡献的主张不成立
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 消融实验（Table 3）表明：空间交叉注意力是关键组件（去掉后PDMS从87.1大幅跌至55.1），Agent/Map交叉注意力进一步提供结构化感知信息，级联机制在此基础上再提升0.7 PDMS
- **Tags**: ['improvement', 'causal']

## C5: DiffusionDrive在nuScenes开环评测上超越对比方法
- **Statement**: 在nuScenes数据集上，DiffusionDrive相比VAD实现20.8%更低平均L2误差（0.57 vs 0.72 m）和63.6%更低平均碰撞率（0.08 vs 0.22%），运行速度快1.8倍（8.2 vs 4.5 FPS）；相比SparseDrive进一步降低平均L2误差0.04 m
- **Status**: verified
- **Falsification criteria**: 若使用相同ResNet-50骨干且同等训练设置下VAD或SparseDrive达到或超过DiffusionDrive的L2和碰撞率，则该主张不成立
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 基于SparseDrive骨干的验证表明截断扩散策略对不同感知架构（稀疏PV特征）具有通用性；nuScenes场景相对简单，主要验证方法的跨数据集泛化能力
- **Tags**: ['improvement']

## C6: K-Means锚定高斯分布先验优于外推轨迹先验
- **Statement**: 使用K-Means聚类得到的多模式锚定高斯分布作为去噪起点，相比以当前车辆状态外推轨迹作为先验（单一锚点），PDMS高3.4分（88.1 vs 84.7），更好覆盖复杂场景（障碍物规避、转弯等）的潜在动作空间
- **Status**: verified
- **Falsification criteria**: 若外推轨迹先验在多模式多样性指标或复杂场景子集上与锚定高斯分布持平或更优，则多模式先验必要性的主张不成立
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: 外推轨迹仅表达单一直行/减速意图，无法覆盖转弯、变道等非平凡驾驶行为；K-Means锚点在训练集上自动捕获了真实驾驶行为的多模式结构，进而提供更具代表性的先验分布
- **Tags**: ['causal', 'improvement']

## C7: 推理阶段采样数量N_infer可灵活调整以适应不同算力需求
- **Statement**: 模型训练时使用固定锚点数量（20个），但推理时可动态调整采样噪声数量N_infer；较少采样（10个）即可获得合理规划质量，增加至20或40个可进一步提升质量
- **Status**: verified
- **Falsification criteria**: 若N_infer的变化对PDMS及子项无显著影响，则推理灵活性主张不成立
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 这一灵活性源于模型对锚定高斯分布的通用学习：任意数量的随机噪声均可被加入锚点并去噪，不受训练时锚点数量硬约束，允许在资源受限的部署场景中按需权衡质量与效率
- **Tags**: ['descriptive', 'scoping']
