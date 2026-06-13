# Heuristics

## H1: 用多视角操作图像、任务指令与机器人状态共同构成观测条件，再让 action expert 预测动作块。
- **Rationale**: 原文把观测条件定义为三路图像、任务指令和机器人状态的组合，并说明 VLM 建立多模态条件，action expert 负责动作生成。
- **Sensitivity**: 若相机视角、状态输入或任务指令缺失，条件分布会少掉论文设定中的关键输入；这种影响是分析推断,论文未显式声明。
- **Bounds**: 动作块长度 T 在预训练阶段设为 50；观测图像按原文为三视角。
- **Code ref**: [O_t, A_t, action expert]
- **Source**: Sec. 4.1 Architecture, Eq. 1, Eq. 2

## H2: 用 blockwise causal attention 将图像/语言、状态、动作划分为功能块，块内双向注意力，块间按因果顺序可见。
- **Rationale**: 原文说明该配置让 action expert 利用全部观测知识，同时防止未来动作 token 泄漏到当前观测表示。
- **Sensitivity**: 如果块间 mask 放宽，未来动作信息可能进入观测表示；如果过度收紧，动作专家可用的观测条件会减少。
- **Bounds**: 功能块按原文为图像与任务指令块、状态块、动作块；块内 bidirectional attention，块间 causal mask。
- **Code ref**: [blockwise causal attention]
- **Source**: Sec. 4.1 Architecture

## H3: 用 learnable queries 对三视角图像提取的表示与 LingBot-Depth 的 depth tokens 做蒸馏对齐。
- **Rationale**: 原文说明该视觉蒸馏用于显式捕获空间感知，并通过投影层的 cross-attention 做维度对齐。
- **Sensitivity**: 深度 tokens 的质量和投影对齐会影响空间先验注入；这是分析推断,论文未显式声明。
- **Bounds**: queries 与 depth tokens 均对应三视角操作图像；损失按 Eq. 5 执行。
- **Code ref**: [Q_t, D_t, Proj, L_distill]
- **Source**: Sec. 4.1 Architecture, Eq. 5

## H4: 分布式训练采用 FSDP，并为 action expert modules 构造专属 shard groups。
- **Rationale**: 原文将该策略用于在显存占用与训练吞吐之间取得折中，并缓解过度参数分片带来的通信开销。
- **Sensitivity**: 分片粒度与 action expert 的模块边界会影响通信与吞吐；这是分析推断,论文未显式声明。
- **Bounds**: optimizer states、model parameters、gradients 被 FSDP 分片；action expert modules 使用专属 shard groups。
- **Code ref**: [FSDP, shard groups, action expert modules]
- **Source**: Sec. 4.2 Training Efficiency Optimization

## H5: 混合精度策略在 reductions 使用 torch.float32，在 storage and communication 使用 torch.bfloat16。
- **Rationale**: 原文说明 reductions 使用 torch.float32 是为了 numerical stability，storage and communication 使用 torch.bfloat16。
- **Sensitivity**: 若 reductions 精度降低，数值稳定性可能下降；若存储和通信不用低精度，效率收益可能减少。
- **Bounds**: reductions: torch.float32；storage and communication: torch.bfloat16。
- **Code ref**: [torch.float32, torch.bfloat16]
- **Source**: Sec. 4.2 Training Efficiency Optimization

## H6: 把视觉、语言与动作的 multimodal fusion 视作 sparse attention，并用 FlexAttention 与 torch.compile 优化。
- **Rationale**: 原文说明 FlexAttention 用于优化 sparse attention 计算，torch.compile 的 operator fusion 用于减少 kernel launch overhead 并最大化 memory bandwidth utilization。
- **Sensitivity**: 收益依赖注意力稀疏结构与算子融合覆盖范围；这是分析推断,论文未显式声明。
- **Bounds**: FlexAttention 用于 attention 计算优化；torch.compile 用于 operator fusion。
- **Code ref**: [FlexAttention, torch.compile]
- **Source**: Sec. 4.2 Training Efficiency Optimization
