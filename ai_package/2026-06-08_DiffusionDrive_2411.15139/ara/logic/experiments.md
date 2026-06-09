# Experiments

## E1: NAVSIM navtest分割闭环评测定量对比
- **Verifies**: C2
- **Setup**:
  - Model: DiffusionDrive（ResNet-34骨干，20个K-Means锚点，2步去噪，2层级联解码器）
  - Hardware: NVIDIA 4090（8卡训练）
  - Dataset: NAVSIM navtest分割（非响应式仿真闭环评测）
  - System: 从零训练100轮，AdamW优化器，总批量大小512，学习率6e-4，无测试时增强，无后处理
- **Procedure**:
  1. 以对齐的ResNet-34骨干网络训练DiffusionDrive，遵循Transfuser训练与推理配置
  2. 在navtest分割上进行闭环非响应式仿真评测，输出8航点4秒轨迹
  3. 与UniAD、PARA-Drive、LTF、Transfuser、DRAMA、VADv2-V8192、Hydra-MDP-V8192、Hydra-MDP-V8192-W-EP进行对比
  4. 记录NC、DAC、TTC、Comf.、EP和PDMS综合得分
- **Metrics**: ['NC（无责任碰撞）', 'DAC（可行驶区域合规性）', 'TTC（碰撞时间）', 'Comf.（舒适度）', 'EP（自车进度）', 'PDMS（综合规划得分）']
- **Expected outcome**: DiffusionDrive在PDMS及多数子项上高于所有基线方法，尤其超越使用更多锚点的词汇表方法
- **Baselines**: ['UniAD', 'PARA-Drive', 'LTF', 'Transfuser', 'DRAMA', 'VADv2-V8192', 'Hydra-MDP-V8192', 'Hydra-MDP-V8192-W-EP']
- **Dependencies**: []

## E2: 从Transfuser到DiffusionDrive的演进路线图实验
- **Verifies**: C1, C2, C3
- **Setup**:
  - Model: Transfuser（MLP头）、Transfuser_DP（原始DDIM扩散，20步）、Transfuser_TD（截断扩散，2步）、DiffusionDrive（截断扩散+级联解码器，2步）
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 各变体共享相同ResNet-34感知骨干，仅规划模块不同
- **Procedure**:
  1. 测量Transfuser基线（MLP规划，1步）的PDMS、FPS和模式多样性D
  2. 替换MLP为原始DDIM扩散UNet（20步）得到Transfuser_DP，测量各指标
  3. 在Transfuser_DP基础上应用截断扩散（2步）得到Transfuser_TD，重新评测
  4. 加入级联扩散解码器得到DiffusionDrive，完整评测
  5. 记录各方法的架构类型、单步推理时间、规划模块总时间、模式多样性D、参数量、FPS
- **Metrics**: ['PDMS', 'FPS', '模式多样性D（基于mIoU）', '单步推理时间（ms）', '规划模块总时间（ms）', '参数量（M）']
- **Expected outcome**: 随演进步骤PDMS和D分数逐步提升；截断扩散后FPS大幅恢复至实时水平；DiffusionDrive实现PDMS和多样性的综合最优
- **Baselines**: ['Transfuser（MLP）', 'Transfuser_DP（原始DDIM扩散）', 'Transfuser_TD（截断扩散）']
- **Dependencies**: []

## E3: 扩散解码器设计选择消融实验
- **Verifies**: C4
- **Setup**:
  - Model: 六种扩散解码器配置（ID-1至ID-6），参数量范围57M-102M
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 保持截断扩散策略不变，逐步添加或替换解码器子模块
- **Procedure**:
  1. ID-1：使用条件UNet解码器 + 自车查询交互（Transfuser_TD基线，102M）
  2. ID-2：轻量解码器 + 仅自车查询，无其他注意力（57M）
  3. ID-3：轻量解码器 + 自车查询 + 空间交叉注意力（58M）
  4. ID-4：轻量解码器 + 自车查询 + 智能体/地图交叉注意力（58M）
  5. ID-5：轻量解码器 + 自车查询 + 空间交叉注意力 + 智能体/地图交叉注意力（59M）
  6. ID-6：完整配置（ID-5 + 级联解码器，60M）
  7. 评测各配置的规划指标和参数量
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS', '参数量（M）']
- **Expected outcome**: 完整配置ID-6在PDMS上高于所有消融变体；空间交叉注意力是最重要的单一组件；级联机制在ID-5基础上进一步提升性能
- **Baselines**: ['ID-1 (Transfuser_TD UNet)', 'ID-2 (无空间注意力)', 'ID-3 (仅空间注意力)', 'ID-4 (仅Agent/Map注意力)', 'ID-5 (空间+Agent/Map，无级联)']
- **Dependencies**: ['E2']

## E4: 推理去噪步数消融实验
- **Verifies**: C1
- **Setup**:
  - Model: DiffusionDrive（固定权重，60M），推理步数分别为1、2、3
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 模型权重固定，仅调整推理时去噪步数
- **Procedure**:
  1. 保持DiffusionDrive训练权重不变，分别以1步、2步、3步进行推理
  2. 评测各步数配置下的PDMS及子项分数
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 1步即可获得接近2步的规划质量，表明锚定高斯分布提供了合理起点；步数增加带来微小增益后趋于饱和
- **Baselines**: ['1步配置', '3步配置']
- **Dependencies**: ['E2']

## E5: 级联阶段数消融实验
- **Verifies**: C4
- **Setup**:
  - Model: DiffusionDrive，级联阶段数分别为1、2、4（参数量59M/60M/65M）
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 各配置独立训练
- **Procedure**:
  1. 分别训练级联阶段数为1、2、4的DiffusionDrive模型
  2. 评测各配置的规划指标和参数量
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS', '参数量（M）']
- **Expected outcome**: 阶段数增加提升规划质量；4阶段时性能趋于饱和，但参数量和推理时间持续增长
- **Baselines**: ['1阶段（59M）', '4阶段（65M）']
- **Dependencies**: ['E3']

## E6: 推理采样噪声数量N_infer消融实验
- **Verifies**: C7
- **Setup**:
  - Model: DiffusionDrive（固定权重，60M），N_infer分别为10、20、40
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 模型权重固定，仅调整推理阶段采样数量
- **Procedure**:
  1. 固定训练好的DiffusionDrive，分别以N_infer=10、20、40进行推理
  2. 评测不同采样数量下的规划指标
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 较少采样（10个）即可获得合理规划质量；更多采样带来持续但边际递减的提升
- **Baselines**: ['N_infer=10', 'N_infer=40']
- **Dependencies**: []

## E7: nuScenes数据集开环评测
- **Verifies**: C5
- **Setup**:
  - Model: DiffusionDrive（基于SparseDrive，ResNet-50骨干，18个K-Means锚点，2层级联解码器）
  - Hardware: NVIDIA 4090（单卡评测FPS）
  - Dataset: nuScenes数据集（开环评测，遵循ST-P3指标计算）
  - System: 两阶段训练：SparseDrive阶段1感知预训练权重初始化，阶段2在nuScenes训练10轮，替换规划模块为截断扩散解码器
- **Procedure**:
  1. 以SparseDrive官方阶段1预训练权重初始化，替换规划模块
  2. 在nuScenes数据集上训练阶段2模型10轮
  3. 与ST-P3、UniAD、OccNet、VAD、SparseDrive进行L2误差和碰撞率对比
  4. 按SparseDrive评测流程在单卡NVIDIA 4090上测量FPS
- **Metrics**: ['L2误差（1s/2s/3s/平均，单位m）', '碰撞率（1s/2s/3s/平均，单位%）', 'FPS']
- **Expected outcome**: DiffusionDrive在L2误差和碰撞率上低于或持平最强基线，同时保持较高FPS
- **Baselines**: ['ST-P3', 'UniAD', 'OccNet', 'VAD', 'SparseDrive']
- **Dependencies**: []

## E8: 驾驶先验对比：锚定高斯分布 vs 外推轨迹
- **Verifies**: C6
- **Setup**:
  - Model: 三种配置：Row-1（锚定分布训练+锚定分布推理，DiffusionDrive基线）、Row-2（锚定分布训练+外推轨迹推理）、Row-3（外推轨迹训练+外推轨迹推理）
  - Hardware: NVIDIA 4090
  - Dataset: NAVSIM navtest分割
  - System: 其他训练配置保持不变
- **Procedure**:
  1. Row-1：完整DiffusionDrive基线（多模式锚定高斯分布训练和推理）
  2. Row-2：使用DiffusionDrive基线模型，但推理时以基于当前状态的外推轨迹替换锚定采样
  3. Row-3：以单一锚点（外推轨迹）训练DiffusionDrive，推理时在外推轨迹周围采样
  4. 评测各配置的PDMS及子项指标
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 锚定高斯分布配置（Row-1）在PDMS上明显优于两种外推轨迹先验配置
- **Baselines**: ['外推轨迹推理（Row-2）', '外推轨迹训练+推理（Row-3）']
- **Dependencies**: ['E2']
