## 总体架构
- **Value**: 统一 autoregressive architecture，交替生成 visual tokens 和 action tokens
- **Rationale**: 通过逐步反馈把 future frame prediction 与 trajectory planning 紧密耦合。
- **Search range**: 论文对比 parallel predict-and-plan、sequential predict-then-plan 与 interleaved modeling and planning。
- **Sensitivity**: 高；生成方案消融显示时序组织直接影响规划质量。
- **Source**: Sec 1 Introduction; Sec 3 Overview; Sec 4.3 Table 4

## 语言骨干
- **Value**: Phi-1.5-based multimodal LLM，遵循 Show-o 设计
- **Rationale**: Show-o 将多模态数据表示为共享离散 token 空间，Phi-1.5 提供语言骨干。
- **Search range**: 论文未报告替代 LLM 骨干。
- **Sensitivity**: 未知；论文未做骨干模型消融。
- **Source**: Sec 3 Overview; Appendix A

## 文本 tokenizer 词表
- **Value**: Phi-1.5 discrete tokenizer vocabulary size 50,295
- **Rationale**: 原始 text-only LLM 不能直接处理多模态输入，需要扩展视觉 tokens。
- **Search range**: 原始词表加额外 visual tokens。
- **Sensitivity**: 低到中；词表扩展是统一离散 token 建模的结构前提，但论文未做词表大小消融。
- **Source**: Appendix A

## 视觉 tokenizer
- **Value**: dual-branch tokenizer，high-resolution contextual branch 与 low-resolution dynamic branch，均 built upon MagVIT-v2，each with an 8192-entry codebook
- **Rationale**: 将图像压缩为上下文语义 token 与动态运动 token，供 LLM 序列建模。
- **Search range**: contextual branch 与 dynamic branch；论文未报告单 codebook 替代。
- **Sensitivity**: 高；历史信息消融显示 Context Only、Dynamic Only 与二者组合表现不同。
- **Source**: Sec 4.1 Implementation details; Appendix A; Sec 4.3 Table 5

## contextual branch
- **Value**: frozen high-resolution branch processes 256 × 448 images and produces 448 contextual tokens per frame
- **Rationale**: 提供高分辨率场景语义与结构信息。
- **Search range**: 256 × 448；448 contextual tokens per frame。
- **Sensitivity**: 中到高；Context Only 保持较强规划表现，说明空间语义重要。
- **Source**: Sec 4.1 Implementation details; Sec 4.3 Table 5

## dynamic branch
- **Value**: pretrained low-resolution branch processes 128 × 224 images and generates 28 dynamic tokens per frame
- **Rationale**: 用较短 token 序列捕获短期运动和动态变化。
- **Search range**: 128 × 224；28 dynamic tokens per frame。
- **Sensitivity**: 高；Dynamic Only 在历史信息消融中显著变差，说明单独动态 token 不足。
- **Source**: Sec 4.1 Implementation details; Sec 4.3 Table 5

## 深度估计与融合
- **Value**: Depth Anything 3 提取 monocular depth maps，深度图 resized 为 256×448 和 128×224，经 CDE 与 DDE，通过 cross-attention 与视觉 token embeddings 融合
- **Rationale**: 引入几何线索以提升长时域未来帧预测和规划上下文。
- **Search range**: 有 depth fusion 或无 depth fusion。
- **Sensitivity**: 高；深度消融显示加入 depth 后视频质量改善，规划综合指标也提升。
- **Source**: Sec 3 Depth integration; Sec 4.3 Table 3; Fig 5

## 深度编码器初始化
- **Value**: depth encoders initialized using MagVIT-v2 weights
- **Rationale**: 复用视觉 tokenizer 相关权重以初始化 CDE 和 DDE。
- **Search range**: 论文未报告其他初始化方式。
- **Sensitivity**: 未知；论文未做初始化消融。
- **Source**: Sec 4.1 Implementation details

## 动作解码头
- **Value**: hidden states corresponding to action tokens are fed into an MLP head to regress ego positions
- **Rationale**: 把 LLM 中的 action token 表征映射为未来 ego positions，从而形成 planned trajectory。
- **Search range**: 论文未报告其他动作头。
- **Sensitivity**: 未知；论文未做动作头消融。
- **Source**: Sec 3 Training objectives; Sec 3 Decoding and output

## 注意力掩码
- **Value**: future frame tokens 可关注所有 previous tokens 和 current frame 内所有 tokens，同时跨时间保持 causal masking
- **Rationale**: 同时捕获帧内空间依赖与跨时间依赖，提升相邻视觉区域一致性。
- **Search range**: 训练和推理使用一致的 attention masking scheme。
- **Sensitivity**: 中；论文给出机制但未做掩码消融。
- **Source**: Sec 3 Training objectives; Sec 3 Inference; Fig 3

## 推理缓存
- **Value**: KV-cache reuse
- **Rationale**: 保存前序 key 与 value 表征，新增 token 只计算新增部分，提高自回归推理效率。
- **Search range**: 使用或不使用 KV-cache；论文未报告速度对比。
- **Sensitivity**: 低到中；主要影响效率，论文未说明影响精度。
- **Source**: Sec 3 Inference

## 特殊 tokens
- **Value**: <|soi|>, <|eoi|>, <|sod|>, <|eod|>, <|t2i|>, <|mmu|>, <|t2d|>, <|act|>, <|sot|>, <|eot|> and so on
- **Rationale**: 标记任务类型、contextual image tokens、dynamic image tokens、user prompt 与 action segment 边界。
- **Search range**: 论文列出这些 special tokens，未报告替代集合。
- **Sensitivity**: 中；它们定义统一序列格式，但论文未做 token 设计消融。
- **Source**: Appendix A
