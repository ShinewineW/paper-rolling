# Heuristics

## H1: 按 depth queries、video queries、action queries 的顺序组织 query，并施加 depth→video→action 的因果注意力。
- **Rationale**: 论文称 video queries 可以消费 depth context，action queries 可以消费 depth 和 video context，这让几何先支撑视频想象，再让视频和几何共同支撑规划。
- **Sensitivity**: 若取消或反转该顺序，video/action 可能失去上游几何与想象上下文；这是分析推断，论文未显式声明具体失败幅度。
- **Bounds**: 同一 time step 内固定 depth queries→video queries→action queries；规划模式可只启用 action expert，但 query 语义接口仍按该顺序定义。
- **Code ref**: [build_depth_video_action_causal_mask]
- **Source**: Embeddings Generation；Introduction 中的 structured causal attention mask across query groups in a depth→video→action manner

## H2: 使用固定大小 query bottleneck 连接 LLM 与三个 generative experts。
- **Rationale**: 论文强调 fixed-size query interface 能控制实际计算量，并让下游 heads 从对应 query embeddings 读出深度、未来视频和未来动作。
- **Sensitivity**: query 数量越少，上下文容量越低；论文的 query ablation 表述为更多 query tokens 提供更高容量并提升生成与规划。
- **Bounds**: 默认 query 配置为 64 depth-query tokens、64 video-query tokens、8 action-query tokens；较小预算为 32 depth + 32 video + 4 action query tokens。
- **Code ref**: [FixedSizeQueryInterface]
- **Source**: Input Processing；Implementation Details；Ablations on Number of Queries

## H3: 深度生成在 pixel-space 中完成，并在训练前对 depth 做 log transform 与 per-map percentile normalization 到 [-0.5, 0.5]。
- **Rationale**: 论文认为 depth 维度低于 RGB video，pixel-space 可保留边界细节且不需要额外 learned codec；归一化用于稳定训练。
- **Sensitivity**: 归一化或像素空间设计改变会影响深度边界保真与数值稳定性；这是分析推断，论文未给出替代设置的量化敏感性。
- **Bounds**: 训练前执行 log transform 与 per-map percentile normalization；推理时 invert transform 以恢复 metric 或 relative depth。
- **Code ref**: [normalize_depth_log_percentile]
- **Source**: Depth Generator；Depth Normalization

## H4: video denoiser 不使用标准 text embedding 条件，而使用 LLM world video embeddings，并额外拼接 CLIP 当前帧视觉条件。
- **Rationale**: world video embeddings 汇总语言意图、多视角感知、action context，并外部吸收 depth query 的几何线索；CLIP 条件用于保留 appearance、identity 和 camera content。
- **Sensitivity**: 去掉 depth joint learning 或当前帧视觉条件会削弱未来视频一致性；论文对 depth learning 做了 ablation，但未单独量化 CLIP 条件移除。
- **Bounds**: 当前 RGB 先经 VAE 得到 latent，目标 horizon 初始化 noisy video latents；video denoiser 每个 transformer block 通过 cross-attention 访问 world embeddings。
- **Code ref**: [VideoGeneratorWithWorldAndClipCondition]
- **Source**: Video Generator；Ablations on Depth Learning for Video Generation

## H5: action trajectory state 使用连续的 position and heading 表示，即 $( x , y ,$ cos ??, sin ??)。
- **Rationale**: 论文称该表示避免 angular wrap-around，并鼓励 smooth turn dynamics。
- **Sensitivity**: 若直接回归角度，可能重新引入角度环绕问题；这是分析推断，论文未给出替代表达的实验。
- **Bounds**: 每个 trajectory state 按位置与 heading 的连续表示参数化。
- **Code ref**: [ContinuousTrajectoryState]
- **Source**: Action Generator 后的 trajectory state parameterization
