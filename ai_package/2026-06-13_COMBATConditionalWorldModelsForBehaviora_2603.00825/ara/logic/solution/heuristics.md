# Heuristics

## H1: 只以 Player 1 action history 作为控制条件，不把 Player 2 action labels 输入 world model。
- **Rationale**: 论文把 Player 2 policy 的学习定义为从时序一致的多智能体交互生成中自然涌现，借此避免传统 imitation learning 对所有 agent 完整 action supervision 的依赖。
- **Sensitivity**: 如果训练数据中 Player 1 与 Player 2 的交互关系不清晰，或 Player 1 条件与画面后果对应弱，Player 2 的反应性可能退化为视觉共现模式。
- **Bounds**: 适用于论文中的 partially observed multi-agent trajectories；Player 2 actions remain unobserved。
- **Code ref**: [condition_on_p1_actions_only]
- **Source**: Problem Formulation 与 Key Innovation

## H2: 使用 joint RGB-pose latent representation 作为一个模型变体，并与 RGB-only latent 变体对照。
- **Rationale**: 论文称 joint RGB-pose representation 用于强化 character movement 的结构一致性，实验中 pose-augmented COMBAT 在视觉质量指标上优于 RGB-only variant。
- **Sensitivity**: 依赖 pose keypoints 的质量与同步；pose 注释噪声会影响 latent space 中的结构信号。
- **Bounds**: 论文只说明 RGB-only VAE 与 pose-augmented VAE 两种 world model，没有扩展到其他模态。
- **Code ref**: [rgb_pose_vae_variant]
- **Source**: Model Architecture、Multi-Modal Latent Encoding 与 Results

## H3: DiT attention 采用 frame-causal local sliding window，并让每 fourth layer 使用 global attention。
- **Rationale**: 局部窗口降低长序列计算成本，周期性 global attention 捕获 long-term temporal dependencies。
- **Sensitivity**: local window 过短会损失动作连招和战术上下文，global attention 过少会削弱长程一致性，过多则增加计算量。
- **Bounds**: 论文设定为 local 16 frames 与 global 128-frame context，且用于 128-frame sequences。
- **Code ref**: [hybrid_local_global_attention]
- **Source**: Diffusion Transformer Backbone 与 Implementation Details

## H4: 先蒸馏 decoder，再用 CausVid DMD 将 world model 蒸馏为 few-step sampler，并在推理时使用 static key-value caching。
- **Rationale**: decoder distillation 降低渲染成本，step distillation 减少扩散采样步数，KV caching 复用 attention states，三者共同支持 real-time generation。
- **Sensitivity**: 论文指出 DMD step distillation 会降低 agent responsiveness 和 attack frequency，因此速度提升会牺牲部分行为保真。
- **Bounds**: 应用于 RGB-only 与 pose-augmented world models；论文给出 4-step variant 与 single NVIDIA A100 GPU 上 85 FPS。
- **Code ref**: [causvid_dmd_static_kv_cache]
- **Source**: Accelerated Inference、Stage 3 与 Future Work

## H5: 用 TAA 与 ARC 评估 emergent Player 2 offensive behavior，而不是只依赖 FVD、FID、LPIPS。
- **Rationale**: 论文认为传统视频指标评估 visual fidelity，RL 指标假设有 actions 或 rewards；TAA 衡量动作总量，ARC 衡量 punch-to-kick style balance。
- **Sensitivity**: 依赖 human annotations 的一致性，且只覆盖 observable offensive actions，不能完整度量防守、策略与胜率。
- **Bounds**: 定义在 ground-truth 与 generated gameplay sequences 的 offensive punch/kick annotations 上。
- **Code ref**: [taa_arc_behavior_metrics]
- **Source**: Human Evaluation of Emergent Behavior
