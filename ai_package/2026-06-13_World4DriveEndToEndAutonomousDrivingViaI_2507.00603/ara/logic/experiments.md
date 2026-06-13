# Experiments

## E1: nuScenes 开放环主结果对比
- **Verifies**: C1
- **Setup**:
  - Model: World4Drive
  - Hardware: NVIDIA GPU
  - Dataset: nuScenes
  - System: 开放环端到端规划，输入为多视角 camera，按 VAD-Tiny 配置使用 ResNet-50 backbone
- **Procedure**:
  1. 在 nuScenes benchmark 上训练 World4Drive。
  2. 按既有端到端规划方法的评测协议预测未来轨迹。
  3. 与需要感知标注和不需要感知标注的方法进行表格对比。
- **Metrics**: ['L2', 'Collision Rate']
- **Expected outcome**: World4Drive 相比感知标注-free 强基线应呈现更低规划误差和更低碰撞率。
- **Baselines**: ['ST-P3 [12]', 'OccNet [36]', 'UniAD [13]', 'VAD [16]', 'PPAD [4]', 'GenAD [47]', 'LAW* [18] (Perception-based)', 'BEV-Planner [21]', 'LAW* [18] (Perception-free)']
- **Dependencies**: ['nuScenes [2]', 'ResNet-50 [8]', 'LAW [18]']

## E2: NavSim 闭环主结果对比
- **Verifies**: C2
- **Setup**:
  - Model: World4Drive
  - Hardware: NVIDIA GPU
  - Dataset: NavSim
  - System: 闭环规划评测，输入为拼接 camera 图像，使用 ResNet-34 提取图像特征
- **Procedure**:
  1. 在 NavSim benchmark 设定下训练闭环模型。
  2. 将预测轨迹用 LQR controller 插值。
  3. 按官方闭环 PDM 指标与多个方法比较。
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: World4Drive 相比 LAW (Perception-free) 应获得更好的闭环综合表现，并接近若干感知标注方法。
- **Baselines**: ['UniAD [13]', 'PARA-Drive [33]', 'LTF [30]', 'Transfuser [30]', 'VADv2 [3]', 'Hydra-MDP [19]', 'DiffusionDrive [23]', 'Ego-MLP', 'LAW (Perception-free) [18]']
- **Dependencies**: ['NavSim [14]', 'OpenScene [5]', 'ResNet-34 [8]', 'LAW [18]']

## E3: 核心组件消融实验
- **Verifies**: C3
- **Setup**:
  - Model: World4Drive 及组件变体
  - Hardware: 未在该消融小节单独指定
  - Dataset: nuScenes
  - System: 在相同 nuScenes 平均规划指标下比较 Physical Latent Encoder 与 Intention-aware WM 的不同组合
- **Procedure**:
  1. 构造仅包含单模态世界模型的基线。
  2. 逐步加入 vehicle intention、depth、semantic 和 world model 相关组件。
  3. 比较各行平均 L2 与 Collision 的方向变化。
- **Metrics**: ['L2', 'Collision']
- **Expected outcome**: 完整组件组合应取得更好的规划误差与碰撞表现；缺少世界模型时，即使有意图信息也应退化。
- **Baselines**: ['LAW', '组件移除变体']
- **Dependencies**: ['nuScenes [2]', 'LAW [18]', 'Metric3D v2 [11]', 'Grounded-SAM [31]']

## E4: 不同驾驶条件与机动下的鲁棒性实验
- **Verifies**: C4
- **Setup**:
  - Model: World4Drive
  - Hardware: 未在该实验小节单独指定
  - Dataset: nuScenes
  - System: 按官方 scene descriptions 划分 weather、illumination 和 driving maneuvers 后评估
- **Procedure**:
  1. 按 day、night、sunny、rainy 等条件划分 nuScenes 场景。
  2. 按 left、straight driving、right 等机动类型划分规划样本。
  3. 分别比较 World4Drive 与 LAW 的 L2 和 Collision。
- **Metrics**: ['L2', 'Collision']
- **Expected outcome**: World4Drive 在多数环境条件与驾驶机动下应比 LAW 更稳健，碰撞表现更好。
- **Baselines**: ['LAW [18]']
- **Dependencies**: ['nuScenes [2]', 'LAW [18]']

## E5: Backbone 与 hidden dimension 扩展性消融
- **Verifies**: C5
- **Setup**:
  - Model: World4Drive
  - Hardware: 未在该实验小节单独指定
  - Dataset: nuScenes
  - System: 改变 image backbone 和 hidden dimension 后评估平均规划表现
- **Procedure**:
  1. 固定部分设置并改变 image backbone。
  2. 固定部分设置并改变 hidden dimension。
  3. 比较不同规模设置下的 L2 与 Collision 方向变化。
- **Metrics**: ['L2', 'Collision']
- **Expected outcome**: 扩大 backbone 或 hidden dimension 应整体带来更好的规划指标方向。
- **Baselines**: ['不同 backbone 变体', '不同 hidden dimension 变体']
- **Dependencies**: ['nuScenes [2]', 'ResNet-34', 'ResNet-50', 'ResNet-101']
