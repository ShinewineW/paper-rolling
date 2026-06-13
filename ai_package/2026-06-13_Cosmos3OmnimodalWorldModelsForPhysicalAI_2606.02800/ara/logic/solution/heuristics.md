# Heuristics

## H1: AR 子序列固定放在 DM 子序列之前；DM 内每种模态先放 clean conditioning tokens，再放 noisy diffusion tokens；conditioning 与 diffusion 子序列内部均按 vision、audio、action 排序。
- **Rationale**: 统一 token layout 让 T2I、T2V、I2V、V2V、transfer、forward dynamics、inverse dynamics、policy 共享同一模型入口，避免为不同任务改架构。
- **Sensitivity**: 若顺序不一致，DM token 看到的条件上下文和掩码语义会漂移，生成模式间共享会变弱；clean/noisy 边界错误还会把条件 token 错计入 denoising loss。
- **Bounds**: 适用于论文列出的 language、vision、audio、action 组合；新模态扩展需要保持 clean-before-noisy 与统一时序坐标原则。
- **Code ref**: [pack_sequence_ar_dm]
- **Source**: Sec. 2.2.1 Token Arrangement

## H2: AR token 只做 causal attention；DM token 对 AR+DM 做 full bidirectional attention，且 AR 永不被 DM 更新。
- **Rationale**: 这样 diffusion 可以使用文本提示和全部条件 token，同时保留 VLM 继承来的自回归语言生成与因果完整性。
- **Sensitivity**: 若 AR 允许看 DM，会破坏 autoregressive conditioning pathway；若 DM 只能看局部或因果上下文，会削弱空间、时间一致性与多模态条件利用。
- **Bounds**: 该规则绑定 MoT 双塔结构：AR 走 reasoner tower，DM 走 generator tower，二者在 attention 层交互但参数路径独立。
- **Code ref**: [dual_stream_joint_attention]
- **Source**: Sec. 2.3.2 Dual-Stream Joint Attention

## H3: 在 AR 与 DM temporal indices 之间插入 fixed temporal gap，论文所有模型使用 gap 15000。
- **Rationale**: 论文报告直接让 DM 从最后一个 AR token 的 temporal offset 开始会导致初始视频帧 over-saturation 与 checkerboard artifacts，尤其 Super 更明显；gap 提供更清晰的 text-to-vision transition signal。
- **Sensitivity**: gap 太小可能继续产生位置嵌入过近的问题；gap 过大可能改变 temporal embedding 分布并影响跨模态对齐，论文未给出系统扫参。
- **Bounds**: 论文明确值为 15000，作用于所有后续 vision、audio、action diffusion tokens 的 temporal indices。
- **Code ref**: [ar_dm_temporal_gap]
- **Source**: Sec. 2.4.1 Autoregressive and diffusion token margin

## H4: 用 absolute temporal modulation 将视频、音频、动作不同采样率映射到共享物理时间轴；base TPS 取 24 FPS 经视频 VAE temporal compression 后的值。
- **Rationale**: 视频、音频、动作 token 的物理时间间隔不同，按 token index 对齐会混淆同步关系；按 TPS 调制 temporal increment 能让相同真实时长占据一致位置范围。
- **Sensitivity**: FPS 或 action sampling frequency 元数据错误会直接造成跨模态时序错位；base rate 改变会影响模型已学到的位置尺度。
- **Bounds**: 视频 TPS 为 frame rate 除以 temporal compression factor；音频 TPS 来自 48 kHz 与 1920 hop size；动作 TPS 等于动作数据 sampling frequency。
- **Code ref**: [absolute_temporal_modulation]
- **Source**: Sec. 2.4.2 Absolute Temporal Modulation

## H5: Generator pre-training 使用 multi-resolution training，覆盖 256p、480p、720p，并用 fixed 74000-token context window 做 token packing。
- **Rationale**: 多分辨率暴露高保真内容并鼓励 resolution-agnostic representations；token packing 最大化 GPU 利用率且避免 padding。
- **Sensitivity**: 高分辨率与长视频会推高序列长度；若没有 token budget 与 packing，训练会出现 padding 浪费、重编译开销或显存压力。
- **Bounds**: 论文中 720p 限制更短帧数以满足 sequence length constraints；pre-training 中 resolution-adaptive shift 随分辨率变化。
- **Code ref**: [multi_resolution_token_packing]
- **Source**: Sec. 4.2.1 Multi-resolution training

## H6: Robot policy 推理使用少步 diffusion、shifted noise schedule、CFG parallelism，并跳过 video-latent decoding。
- **Rationale**: policy 部署需要低延迟闭环控制，论文用这些采样与服务优化减少推理开销，同时保留动作输出。
- **Sensitivity**: 步数过少可能损害动作质量；guidance scale 或 noise shift 不匹配会影响 policy 稳定性；跳过视频解码适合控制输出但不适合需要可视化 rollout 的场景。
- **Bounds**: 该策略属于 inference-time 优化，不属于训练目标；论文将其用于 Cosmos3-Nano-Policy-DROID。
- **Code ref**: [policy_fast_diffusion_inference]
- **Source**: Sec. 4.2.5 Robot Policy Post-Training
