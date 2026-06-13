# Problem Specification

## Observations

### O1: 现有 future-aware 或 world-model-based plan
- **Statement**: 现有 future-aware 或 world-model-based planner 已能预测未来场景演化，但 future prediction alone does not guarantee better planning。
- **Evidence**: 摘要和引言明确指出，许多方法仍只预测 future scene states，而没有显式解码 state transitions 中隐藏的 motion implications。
- **Implication**: 未来状态本身可能有描述价值，但未必能直接生成可执行、动态一致的轨迹更新。

### O2: 关键缺失信号不只在 predicted future states 中，更在相邻
- **Statement**: 关键缺失信号不只在 predicted future states 中，更在相邻未来状态的 transitions 中。
- **Evidence**: 引言写明 missing signal lies not only in the predicted future states themselves, but more importantly in the transitions between them。
- **Implication**: 规划模块需要读取状态变化所暗示的运动语义，而不是把未来 BEV 特征当作静态上下文。

### O3: IDM 的 spatial 与 global 两类 dynamics cue 分
- **Statement**: IDM 的 spatial 与 global 两类 dynamics cue 分别承担局部运动证据和整体校准。
- **Evidence**: 方法部分说明 S_k 保留 position-wise motion variations，g_k 总结 overall transition，并通过 spatial cross-attention 与 MLN 融合到 ego query。
- **Implication**: 规划反馈既能关注哪里发生了关键变化，也能获得轨迹级的整体运动条件。

## Gaps

### G1: 预测未来与修正当前轨迹之间缺少显式、可解释的桥。
- **Statement**: 预测未来与修正当前轨迹之间缺少显式、可解释的桥。
- **Caused by**: 现有方法常把 future latent states 作为上下文、评估对象或 reward-guided selection 的依据，而较少学习 adjacent predicted states 到 action-relevant motion 的映射。
- **Existing attempts**: ['WoTE 预测 future BEV states 来评估 candidate trajectories', 'SeerDrive 通过 iterative bidirectional refinement 耦合 future scene evolution 与 trajectory planning', 'DriveLaW 在 shared latent driving world 中让 generator latents 支持 closed-loop planning']
- **Why they fail**: planner may know what could happen next，却缺少 principled mechanism 来判断当前轨迹应如何被修正。

### G2: 仅使用 pooled inverse dynamics feature 过于粗糙
- **Statement**: 仅使用 pooled inverse dynamics feature 过于粗糙。
- **Caused by**: 全局池化会弱化位置相关的 transition evidence。
- **Existing attempts**: ['保留 spatial dynamics map', '同时聚合 global dynamics feature', '用 dual-branch fusion 更新 ego query']
- **Why they fail**: 论文指出 only a subset of spatial changes are truly relevant to the current trajectory hypothesis。

## Key Insight
- **Insight**: 将相邻 imagined BEV latent states 视作可反推运动调整的线索，用 inverse dynamics 从 transition 中提取 motion-aware cue，再把 cue 注入 anchor-conditioned planning query。
- **Derived from**: 由引言中对 predicted futures actionability gap 的分析，以及方法中 IDM 对 adjacent latent imagined BEV states 的建模得到。
- **Enables**: 让 future reasoning 从静态场景上下文转为 trajectory optimization 的显式反馈，并支持 closed-loop refinement 改善长时一致性。

## Assumptions
- 相邻 imagined BEV latent states 的差异包含可恢复的 motion semantics。
- BEV world model 产生的 latent futures 足够可靠，能为 IDM 提供有用 transition cue。
- anchor-conditioned ego query 能代表候选轨迹假设，并可通过 inverse-dynamics feedback 被有效修正。
- spatial dynamics 与 global dynamics 的组合比单一全局表示更适合规划 refinement。
