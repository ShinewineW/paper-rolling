## World Model 主干
- **Value**: 1.2B-parameter Diffusion Transformer
- **Rationale**: 作为核心生成模型，学习 denoise 和预测 future latent frames。
- **Search range**: 论文未给出模型规模搜索范围。
- **Sensitivity**: 规模影响生成能力和计算成本；该判断为分析推断,论文未显式声明。
- **Source**: Abstract, Sec 3.3.2

## DCAE 参数量
- **Value**: 340M-parameter
- **Rationale**: 用于学习 high-ratio state compression，把视觉帧和 pose keypoints 压缩到 latent tensor。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 编码器和解码器容量不足可能降低 latent 表征质量；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.1, Sec 4.1

## Distilled decoder 参数量
- **Value**: 44M-parameter
- **Rationale**: 通过减少 upsampling block count 形成轻量 decoder，用于 real-time rendering。
- **Search range**: 从 340M 减到 44M；论文未给出更多候选。
- **Sensitivity**: 更小 decoder 提升速度但可能损失重建质量；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.1, Sec 4.1

## latent tensor shape
- **Value**: 128 × 23 × 11
- **Rationale**: DCAE 将原始 frame 和 pose 压缩为紧凑 latent representation，供 DiT 在 latent space 中建模。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: latent 尺寸决定压缩率、细节保留和后续 DiT token 规模；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.1, Sec 4.1

## DiT layers
- **Value**: 16 layers
- **Rationale**: 构成 autoregressive Diffusion Transformer 的深度。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 层数影响时空关系建模能力与延迟；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Sec 4.1

## attention heads
- **Value**: 16 attention heads
- **Rationale**: 用于 DiT self-attention 建模复杂 spatiotemporal relationships。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: head 数影响注意力表示能力与计算开销；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Sec 4.1

## model dimension
- **Value**: d_model = 2048
- **Rationale**: 作为 DiT backbone 的 hidden dimension。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 维度影响模型容量与显存需求；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Sec 4.1

## conditioning injection
- **Value**: AdaLNZero in each block
- **Rationale**: 将 Player 1 action history 与 diffusion timestep 形成的 conditioning vector 注入每个 DiT block。
- **Search range**: 论文未给出替代注入方式搜索范围。
- **Sensitivity**: 条件注入方式直接影响动作控制和生成结果对 Player 1 输入的响应；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.1, Sec 3.3.2

## tokenization
- **Value**: linear projection layers for spatio-temporal rasterization
- **Rationale**: 论文说明该设计绕过 conventional patch-based embeddings。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: tokenization 会影响 latent 序列组织与计算模式；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2

## local attention window
- **Value**: 16 frames
- **Rationale**: 大多数层使用 frame-causal attention mask 与 local sliding window，以捕捉短期 temporal dependency。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 窗口过短可能缺少动作上下文，窗口过长会增加计算成本；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Sec 4.1

## global attention context
- **Value**: 128 frames
- **Rationale**: 每第四个 DiT block 使用跨整个 128-frame context 的 global attention，以补充长期依赖。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 全局注意力频率影响长期战术建模与计算开销；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Sec 4.1

## global attention frequency
- **Value**: every fourth layer
- **Rationale**: 在 hybrid local-global attention pattern 中定期引入全局上下文。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 频率越低可能削弱长程依赖，频率越高可能增加计算成本；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2, Fig 2

## position encoding
- **Value**: RoPE across spatial and temporal axes
- **Rationale**: 用于同时编码空间和时间轴位置关系。
- **Search range**: 论文未给出替代位置编码搜索范围。
- **Sensitivity**: 位置编码影响动作、角色位置和时间顺序的一致建模；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2

## attention implementation
- **Value**: FlexAttention
- **Rationale**: 用于 efficient block-sparse masking implementation。
- **Search range**: 论文未给出替代实现搜索范围。
- **Sensitivity**: 实现选择主要影响长序列注意力的效率；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.3.2

## inference sampler
- **Value**: 4-step distilled model
- **Rationale**: 采用 CausVid DMD 将 fully trained model 蒸馏为 few-step sampler 以实现 interactive frame rates。
- **Search range**: 论文未给出其他 step 数搜索范围。
- **Sensitivity**: 步数越少通常速度越高但可能带来质量折中；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.4, Sec 4.1

## KV cache
- **Value**: static key-value caching
- **Rationale**: 复用 generation steps 中先前计算的 attention states 以进一步提升速度。
- **Search range**: 论文未给出替代 cache 策略。
- **Sensitivity**: 缓存策略影响实时推理延迟和长序列计算效率；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.4
