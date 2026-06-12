## true_world_model_subsystems
- **Value**: Generative Heart、Interactive Loop、Memory System 三个子系统的合成
- **Rationale**: 论文把 true world model 定义为这些必要子系统的集成，并用它们支撑 generation、interaction、real-time adaptation 与 memory。
- **Search range**: 从 Stage II 的统一模型到 Stage V 的 true world model
- **Sensitivity**: 高；缺少 interactive loop 或 explicit memory system 的 unified model 只能作为前驱，而非 true world model。
- **Source**: Sec 2.2

## generative_heart
- **Value**: state transitions、observations、rewards、terminations 的生成过程
- **Rationale**: 论文将 Generative Heart 形式化为 world dynamics 与 appearance 的学习模型，负责预测未来状态、观测与任务相关结果。
- **Search range**: Dynamics Model、Observation Model、Outcome Model
- **Sensitivity**: 高；这是 world model 的 generative foundation，但单独存在不足以产生持久可交互世界。
- **Source**: Sec 2.2, Appendix A

## interactive_loop
- **Value**: inference filter、policy、value function
- **Rationale**: 论文说明为了超过 passive movie generator，模型需要 closed interactive loop，使 agent 能实时解释观测并行动。
- **Search range**: partially observable worlds 与 action-conditioned evolution
- **Sensitivity**: 高；没有该回路，模型会停留在 static predictor 或 one-shot generator。
- **Source**: Sec 2.2, Appendix A

## memory_system
- **Value**: recurrent state h_t 与 memory update model
- **Rationale**: 论文把 Memory System 定义为让过去事件影响未来的机制，用于支撑长时程一致性。
- **Search range**: history representation、state update、long-horizon coherence
- **Sensitivity**: 高；论文反复指出没有 dedicated memory and state management 就无法 sustain persistent worlds。
- **Source**: Sec 2.2, Sec 5.3, Appendix A

## unified_model_backbone
- **Value**: shared backbone 与 same paradigm 跨模态处理和生成
- **Rationale**: 论文将 Stage II 的 unified model 定义为用共享骨干和同一范式处理、生成不同模态的系统。
- **Search range**: language-prior、visual-prior、industrial-scale unified systems
- **Sensitivity**: 中；它减少碎片化并促进 cross-modal transfer，但仍缺少连续实时闭环交互。
- **Source**: Sec 4

## single_paradigm_filter
- **Value**: 排除不同模态拼接不同范式的 simple glue models
- **Rationale**: 论文在代表性统一模型筛选中明确排除 text 用 autoregression、image 用 diffusion 这类不同范式拼接系统。
- **Search range**: Stage II representative works 的纳入边界
- **Sensitivity**: 中；该选择让 roadmap 更强调统一范式，而不是工程拼接。
- **Source**: Sec 4.1

## implicit_vs_explicit_world_representation
- **Value**: implicit 2D video frames 与 explicit 3D scenes
- **Rationale**: 论文在一致性部分把世界表示划分为两类，并指出它们面对的记忆与漂移问题不同。
- **Search range**: autoregressive video models、NeRFs、Gaussian Splatting、World Labs、VMem 等
- **Sensitivity**: 高；implicit 表示灵活但易丢上下文和 hallucinating objects，explicit 3D 空间一致性强但动态对象状态更难。
- **Source**: Sec 5.3, Sec 6.3

## memory_governance_policy
- **Value**: 决定 what to write、what to retrieve、how to update、when to forget
- **Rationale**: 论文总结 longer context alone is insufficient，一致性来自对记忆操作的 explicit policies。
- **Search range**: externalized memory、architectural persistence、consistency policies
- **Sensitivity**: 高；它直接对应长时程漂移与遗忘控制。
- **Source**: Sec 6.3
