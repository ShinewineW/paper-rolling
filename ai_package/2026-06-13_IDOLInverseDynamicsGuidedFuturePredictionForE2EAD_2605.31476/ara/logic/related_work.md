# Related Work

## R1: TransFuser [7]
- **DOI**: 
- **Type**: end-to-end autonomous driving baseline
- **Delta**:
  - What changed: TransFuser 建立了 transformer-based sensor-fusion baseline；IDOL 采用 ResNet34-based TransFuser backbone 进行 multi-modal fusion，并在其上加入 latent future simulation、IDM feedback 与 candidate selection。
  - Why: 这样让比较保留常见端到端感知融合骨干，同时把创新集中在未来转移到规划更新的显式连接上。
- **Claims affected**: ['C5']
- **Adopted elements**: ['multi-modal fusion backbone', 'anchor-conditioned planning setting']

## R2: WoTE [38]
- **DOI**: 
- **Type**: world-model-based planning baseline
- **Delta**:
  - What changed: WoTE 使用 future BEV states 评价 candidate trajectories；IDOL 不只评价或选择候选轨迹，而是对相邻 imagined BEV states 施加 IDM，生成 transition-aware query updates。
  - Why: 论文认为现有 world-model 方法通常停留在 latent future forecasting、trajectory evaluation 或 reward-guided selection，缺少 adjacent predicted states 上的显式 transition-to-action mapping。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['reward model based candidate ranking', 'world-model future reasoning comparison']

## R3: SeerDrive [77]
- **DOI**: 
- **Type**: future-aware end-to-end driving
- **Delta**:
  - What changed: SeerDrive 显式耦合 future scene evolution 与 trajectory planning through iterative bidirectional refinement；IDOL 进一步把相邻 latent BEV futures 解码为 inverse-dynamics-derived spatial and global dynamics cues。
  - Why: 该差异用于支撑论文对更可解释、可行动 future-to-planning bridge 的定位。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['future-aware refinement motivation']

## R4: DriveLaW [68]
- **DOI**: 
- **Type**: latent driving world model
- **Delta**:
  - What changed: DriveLaW 将 video generation 与 motion planning 统一在 latent driving world 中；IDOL 同样在 latent space 中使用 world-model reasoning，但将重点放在 adjacent future transitions 的 inverse dynamics decoding。
  - Why: 论文借此说明 latent world 支持 closed-loop planning 后，关键问题转向如何让 predicted futures 以 motion-consistent 方式塑造规划。
- **Claims affected**: ['C1']
- **Adopted elements**: ['latent world-model planning motivation']

## R5: ReSim [71]
- **DOI**: 
- **Type**: inverse dynamics in autonomous driving
- **Delta**:
  - What changed: ReSim 使用 inverse dynamics model 将 predicted videos 转换为 executable trajectories 并评估 controllability；IDOL 将 inverse dynamics 放到 predicted future latent BEV states 之上，用于 planner query refinement。
  - Why: 这为 inverse dynamics 作为 future state 与 action 之间桥梁提供先例，但 IDOL 的作用位置和表示空间不同。
- **Claims affected**: ['C1']
- **Adopted elements**: ['inverse dynamics as controllability bridge']

## R6: FutureSightDrive [76]
- **DOI**: 
- **Type**: inverse-dynamics-related planning
- **Delta**:
  - What changed: FutureSightDrive 将 planning 表述为从 current observations 与 imagined future scenes 中恢复 actions；IDOL 在相邻 imagined BEV states 上学习 transition-to-motion mapping，并把结果注入轨迹优化。
  - Why: 论文用它说明 inverse dynamics 在 driving 中仍较少被探索，而 IDOL 将该思想系统化到 latent BEV world-model planning。
- **Claims affected**: ['C1']
- **Adopted elements**: ['recovering actions from imagined future scenes motivation']
