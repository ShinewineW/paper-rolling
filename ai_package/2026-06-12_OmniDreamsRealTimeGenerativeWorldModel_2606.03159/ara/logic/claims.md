# Claims

## C1: OmniDreams 可以实时生成闭环传感器视频
- **Statement**: OmniDreams 通过自回归视频扩散、流式 KV cache、轻量编解码与多 GPU 并行，在闭环仿真中达到实时交互渲染。
- **Status**: supported
- **Falsification criteria**: 若相同分辨率与推理配置下的端到端分块延迟不能支持实时帧率，或 KV-cache 更新成为热路径瓶颈，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 论文把实时性定义为闭环可交互的视频分块生成，并用单视角与多视角推理计时表支持该点。
- **Tags**: ['improvement', 'descriptive']

## C2: Self Forcing 蒸馏改善仿真质量并保持因果生成
- **Statement**: 从双向模型到因果 Diffusion Forcing 再到 Self Forcing 蒸馏后，OmniDreams-SV 在生成质量、结构条件保真与车道线指标上整体优于未蒸馏因果阶段，同时保留可实时因果生成能力。
- **Status**: supported
- **Falsification criteria**: 若在同一评测集和相同检测器下，Self Forcing 阶段不能优于因果 Diffusion Forcing 阶段，或改进只来自评测设置变化，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该结论来自训练阶段消融；论文明确说明最终蒸馏模型取得最佳 FVD 和最强条件信号保真。
- **Tags**: ['improvement', 'causal']

## C3: 长上下文教师提升长时程 rollout 稳定性
- **Statement**: 继续使用长上下文双向教师进行 Self Forcing 能降低长 rollout 的时间漂移与累积伪影，使后段窗口相对短上下文教师更稳定。
- **Status**: supported
- **Falsification criteria**: 若按相同分段 FVD 协议评测时，长上下文教师不能降低后段窗口退化或均值退化，则该主张被反驳。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 论文将长时程 rollout 拆成多个时间窗，并说明长上下文教师是高质量长 rollout 成功的关键。
- **Tags**: ['improvement', 'causal']

## C4: OmniDreams 可作为闭环策略评估代理
- **Statement**: 在同一 AlpaSim 闭环栈中替换传感器仿真器时，OmniDreams 保持了 NuRec 下不同策略的相对排名，因此可作为闭环策略比较的真实世界代理。
- **Status**: supported
- **Falsification criteria**: 若切换到 OmniDreams 后策略相对排序发生系统性改变，或差异主要由非传感器模块变化导致，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 论文强调固定编排器、交通和物理服务以及初始状态，仅替换传感器仿真器来隔离其影响。
- **Tags**: ['generalization', 'descriptive']

## C5: OmniDreams 的表示可迁移为 World-Action Model 策略
- **Statement**: 将 OmniDreams-SV 后训练为 WAM 后，在 Physical AI Autonomous Vehicles NuRec 数据集闭环协议中，相比 Alpamayo 1.5 获得更低碰撞相关事件，同时使用更少参数。
- **Status**: supported
- **Falsification criteria**: 若按相同闭环协议评测时 WAM 不再优于 Alpamayo 1.5，或训练集重叠导致结果泄漏，则该主张被削弱。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 该主张来自 Sec. 7 的策略后训练评测，论文把它解释为世界模型内部表示对驾驶任务有用。
- **Tags**: ['improvement', 'generalization']
