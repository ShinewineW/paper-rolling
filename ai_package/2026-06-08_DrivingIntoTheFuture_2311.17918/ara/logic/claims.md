# Claims

## C1: Drive-WM 首次实现高质量多视角视频世界模型
- **Statement**: Drive-WM 是首个兼容现有端到端规划模型的驾驶世界模型，通过联合时空建模与视图分解，在自动驾驶场景下生成高质量、多视角一致且可控的多视角视频
- **Status**: supported
- **Falsification criteria**: 若存在早于 Drive-WM 且同样能生成多视角视频的驾驶世界模型，则「首个」主张被证伪；若其 FID/FVD 不优于单视角基线，则「高质量」主张不成立
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: 通过在预训练图像扩散模型基础上引入时序层与多视角层，Drive-WM 在 nuScenes 数据集上超越同期多视角图像生成和单视角视频生成基线，验证了多视角视频世界模型的可行性
- **Tags**: ['improvement', 'scoping']

## C2: 视图分解式生成显著提升多视角一致性
- **Statement**: 将联合多视角建模分解为参考视角生成与条件化拼接视角生成两阶段，可使 KPM 多视角一致性指标大幅提升，同时维持视频质量
- **Status**: supported
- **Falsification criteria**: 若分解式生成与联合建模在 KPM 指标上无显著差异，则该主张不成立
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 分解生成令拼接视角能感知相邻参考视角的具体内容，从而严格约束重叠区域的像素一致性；而联合建模仅施加风格层面约束，无法保证重叠区域内容严格匹配
- **Tags**: ['improvement', 'causal']

## C3: 统一条件接口有效整合多种异构驾驶条件
- **Statement**: 将初始帧图像、文本描述、自车动作、3D 框与 BEV 地图统一投影至 d 维特征空间后拼接，单一接口即可灵活驱动多种异构条件下的可控生成，无需为每类条件设计专用模块
- **Status**: supported
- **Falsification criteria**: 若消融布局条件或时序嵌入后生成质量无明显下降，则统一条件接口设计对可控性的作用不成立
- **Proof**: [E2, E3]
- **Evidence basis**: ['E2', 'E3']
- **Interpretation**: 消融实验显示布局条件对 FID/FVD 与 KPM 均有显著正向影响；可控性评估中 Drive-WM 在 mAPobj 与 mIoUbg 等多项指标上达到最优，印证了统一接口的有效性
- **Tags**: ['improvement', 'descriptive']

## C4: 基于世界模型的树状规划与图像奖励提升端到端规划质量
- **Statement**: 利用世界模型对多条候选轨迹生成未来多视角视频，并以融合地图奖励与目标奖励的图像奖励函数选择最优轨迹，可使规划性能明显优于随机指令基线并接近真值指令上界
- **Status**: supported
- **Falsification criteria**: 若树状规划的 L2 距离和碰撞率不优于随机指令基线，则该主张不成立
- **Proof**: [E4, E5]
- **Evidence basis**: ['E4', 'E5']
- **Interpretation**: 通过在三种驾驶指令候选下展开规划树，图像奖励函数结合感知模型的检测结果为每条预测轨迹打分，地图奖励与目标奖励的乘积形式联合考虑行驶区域合理性与避碰安全性
- **Tags**: ['improvement', 'causal']

## C5: 世界模型生成 OOD 数据可提升规划器域外鲁棒性
- **Statement**: 利用 Drive-WM 在像素空间模拟自车横向偏离车道中心的域外场景并生成监督数据，微调后的规划器可在 OOD 场景下显著降低碰撞率并缩小 L2 偏差
- **Status**: supported
- **Falsification criteria**: 若经世界模型数据微调后的规划器在 OOD 场景的性能与未微调版本无显著差异，则该主张不成立
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 行为克隆训练的端到端规划器存在「缺乏探索」问题，未见过偏离车道中心的场景；Drive-WM 在像素空间合成此类 OOD 样本并提供恢复至车道的轨迹监督，弥补了训练分布的缺口
- **Tags**: ['improvement', 'causal']
