# Claims

## C1: Drive-OccWorld提升4D占用与流预测
- **Statement**: 论文声称Drive-OccWorld在nuScenes、Lyft-Level5和nuScenes-Occupancy上的膨胀GMO、细粒度GMO以及GMO和GSO预测中优于既有方法。
- **Status**: supported
- **Falsification criteria**: 如果在相同数据集、输入帧、预测时长和指标协议下，Drive-OccWorld不再优于Cam4DOcc、PowerBEV-3D或OpenOccupancy-C，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 表格结果支持其在未来占用、当前占用和流关联质量上的整体优势，但表2的MD抽取存在排版粘连，细粒度类别拆分需按原表核对。
- **Tags**: ['improvement']

## C2: 动作条件支持可控生成
- **Statement**: 论文声称将轨迹、速度、转角或命令等动作条件注入世界模型，可以改善预测并带来可控生成能力。
- **Status**: supported
- **Falsification criteria**: 如果移除或替换动作条件后，预测质量不下降，或不同动作条件不能产生对应的未来占用变化，则该主张被削弱。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 表3显示任一动作条件相对基线均有提升，文字还区分低层条件更利于未来预测、高层命令更影响当前表现。
- **Tags**: ['causal', 'improvement']

## C3: 世界模型可改善端到端规划
- **Statement**: 论文声称将4D世界模型与占用代价规划器结合，可以提升开放环轨迹规划的L2误差和碰撞率表现。
- **Status**: supported
- **Falsification criteria**: 如果在相同nuScenes开放环协议下，Drive-OccWorldP的L2或碰撞率不优于UniAD、ST-P3、VAD-Base、Drive-WM或BEV-Planner等基线，则该主张被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 表5给出端到端规划比较，表8进一步显示占用代价因子和BEV refinement对安全规划有贡献。
- **Tags**: ['improvement']

## C4: 条件归一化和动作注入接口影响预测质量
- **Statement**: 论文声称语义、ego-motion和agent-motion条件归一化均有贡献，cross-attention与Fourier embedding是更有效的动作条件注入方式。
- **Status**: supported
- **Falsification criteria**: 如果在消融中加入这些模块不能改善mIoU或VPQ，或addition接口优于cross-attention，则该设计主张被削弱。
- **Proof**: [E4, E2]
- **Evidence basis**: ['E4', 'E2']
- **Interpretation**: 表6和表7将模块开关与预测指标关联，支持这些设计对未来状态建模有正向影响。
- **Tags**: ['causal', 'improvement']

## C5: 历史输入、记忆队列和语义损失提升模型效果
- **Statement**: 论文声称增加历史输入和记忆队列长度会提升预测表现，语义损失组合也会改善占用和流预测。
- **Status**: supported
- **Falsification criteria**: 如果在相同实验设置中增加历史帧、记忆队列或额外语义监督不能带来更好预测，则该主张被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 表9支持历史信息和记忆长度的效果，表10支持交叉熵、二值占用和Lovasz损失组合的效果。
- **Tags**: ['causal', 'improvement']
