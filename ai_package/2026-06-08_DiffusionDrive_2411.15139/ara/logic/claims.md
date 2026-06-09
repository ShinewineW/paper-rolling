# Claims

## C1: 截断扩散策略解决模态崩溃并将去噪步数减少至2步
- **Statement**: 通过引入基于K-Means聚类锚点构建的锚定高斯分布并截断扩散时间表,截断扩散策略将去噪起点从纯高斯噪声替换为多模式锚定分布,从而解决原始扩散策略的模态崩溃问题,并将推理所需去噪步数从20步压缩至2步
- **Status**: supported
- **Falsification criteria**: 若截断扩散策略与原始DDIM扩散策略在模态多样性得分D和推理速度上无显著差异,则主张不成立
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: Table 2通过Transfuser→Transfuser_DP→Transfuser_TD的演进路线图,定量展示截断扩散策略将去噪步数从20减至2,FPS从7提升至27,同时模态多样性得分D从11%提升至70%
- **Tags**: ['improvement', 'causal']

## C2: DiffusionDrive在NAVSIM上以最少锚点数创造新PDMS记录
- **Statement**: DiffusionDrive在NAVSIM navtest split上以相同ResNet-34主干网络仅用20个锚点实现88.1 PDMS,超越所有先前方法(包括使用8192个锚点和额外监督及后处理的强力竞争者),同时在NVIDIA 4090上以45 FPS实时速度运行
- **Status**: supported
- **Falsification criteria**: 若存在同等主干、无后处理条件下取得更高PDMS的方法,或若增大N_infer对性能无改善,则主张不成立
- **Proof**: [E1, E6]
- **Evidence basis**: ['E1', 'E6']
- **Interpretation**: Table 1展示DiffusionDrive以最少锚点数在所有子指标上领先;Table 6进一步说明推理时动态调整采样数量N_infer可灵活权衡性能与计算开销
- **Tags**: ['improvement', 'descriptive']

## C3: 级联扩散解码器通过分层交互提升规划质量并减少参数
- **Statement**: 所提出的级联扩散解码器通过稀疏可变形空间交叉注意力与BEV/PV特征交互、与智能体/地图查询的交叉注意力以及级联迭代精化机制,在参数量少于基于UNet方案的条件下显著提升规划质量
- **Status**: supported
- **Falsification criteria**: 若消融实验中去掉空间交叉注意力或级联机制后PDMS不下降,则主张不成立
- **Proof**: [E3, E5]
- **Evidence basis**: ['E3', 'E5']
- **Interpretation**: Table 3中ID-2到ID-6的逐步消融验证了每个组件对规划质量的贡献,完整解码器(ID-6)比UNet基准(ID-1)减少39%参数并提升2.4 PDMS;Table 5验证级联阶段数的递进影响
- **Tags**: ['improvement', 'causal']

## C4: DiffusionDrive在nuScenes开环评估上达到最低L2误差和碰撞率
- **Statement**: DiffusionDrive在nuScenes数据集上以ResNet-50主干网络取得所有对比方法中最低的平均L2误差和最低(或持平最低)的平均碰撞率,同时运行速度快于VAD
- **Status**: supported
- **Falsification criteria**: 若VAD或SparseDrive在相同指标协议下取得更低平均L2误差,则主张不成立
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: Table 7展示DiffusionDrive平均L2为0.57m,平均碰撞率为0.08%,与SparseDrive持平或更优,且运行速度(8.2 FPS)快于VAD(4.5 FPS)
- **Tags**: ['improvement', 'descriptive']

## C5: 锚定高斯分布先验优于基于当前状态的外推轨迹先验
- **Statement**: 基于K-Means聚类多模式锚点的锚定高斯分布在覆盖潜在动作空间方面优于基于当前行驶状态外推的单一轨迹先验,在挑战性场景(如避障和转弯)中表现出更强的规划能力
- **Status**: supported
- **Falsification criteria**: 若使用外推轨迹先验(Row-3)能与锚定高斯分布(Row-1)达到相近PDMS,则主张不成立
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: Table 8中Row-1(88.1 PDMS)显著优于Row-2(81.3)和Row-3(84.7),证明多模式锚点覆盖能力是性能关键因素
- **Tags**: ['causal', 'improvement']

## C6: 锚点高斯分布具备跨数据集泛化能力
- **Statement**: 以NAVSIM数据集聚类的锚点训练的DiffusionDrive在完全不同的CARLA Longest6基准上仍显著优于基准方法,证明锚点高斯分布是覆盖多模式驾驶动作空间的通用先验,而非训练集信息的泄漏
- **Status**: supported
- **Falsification criteria**: 若使用NAVSIM锚点在CARLA上训练的性能与Transfuser基准相当或更低,则泛化性主张不成立
- **Proof**: [E9]
- **Evidence basis**: ['E9']
- **Interpretation**: Table 9显示跨域锚点训练的DiffusionDrive在CARLA Longest6上驾驶得分DS从47.30提升至64.27,验证了锚点设计的跨域泛化能力
- **Tags**: ['generalization']
