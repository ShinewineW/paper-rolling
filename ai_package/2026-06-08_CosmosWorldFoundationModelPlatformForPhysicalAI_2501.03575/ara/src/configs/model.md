## 扩散 WFM 7B 层数 / 模型维度 / FFN 维度
- **Value**: 28 层，dim=4,096，FFN=16,384
- **Rationale**: DiT 架构适配视频生成，28 层对应 7B 参数规模
- **Search range**: 层数 24~36；维度 2048~8192
- **Sensitivity**: 高：直接决定模型容量
- **Source**: ['Tab. 11']

## 扩散 WFM 14B 层数 / 模型维度 / FFN 维度
- **Value**: 36 层，dim=5,120，FFN=20,480
- **Rationale**: 更多层与更大维度支持 14B 参数规模
- **Search range**: 层数 28~48；维度 4096~8192
- **Sensitivity**: 高
- **Source**: ['Tab. 11']

## AdaLN-LoRA 低秩维度
- **Value**: 256
- **Rationale**: 低秩分解 AdaLN 层，使 7B 模型从 11B 参数量降至 7B（减少 36%）同时保持性能
- **Search range**: 64 ~ 512
- **Sensitivity**: 中：维度影响 AdaLN 近似质量与参数节省量
- **Source**: ['Sec. 5.1.2', 'Tab. 11']

## 3D Patchify 尺寸
- **Value**: p_t=1, p_h=2, p_w=2
- **Rationale**: 时序维度不压缩以保留帧级信息，空间维度 2×2 patch 控制 token 序列长度
- **Search range**: 固定配置
- **Sensitivity**: 高：直接影响序列长度与计算量
- **Source**: ['Sec. 5.1.2']

## 文本编码器及 T5 序列长度
- **Value**: T5-XXL，zero-padding 至固定长度 512
- **Rationale**: T5-XXL 提供高质量语言表示；固定长度保证批次计算效率
- **Search range**: 固定配置
- **Sensitivity**: 高：文本编码器质量直接影响文本对齐效果
- **Source**: ['Sec. 5.1.3']

## 扩散 WFM 注意力头数（7B/14B）
- **Value**: 7B: 32，14B: 40
- **Rationale**: 多头注意力捕获不同子空间特征，头数随模型规模增大
- **Search range**: 16 ~ 64
- **Sensitivity**: 中
- **Source**: ['Tab. 11']

## 自回归 WFM 4B 层数 / 模型维度
- **Value**: 16 层，dim=4,096
- **Rationale**: Llama3 风格 GPT，16 层对应 4B 参数规模
- **Search range**: 8 ~ 32 层
- **Sensitivity**: 高
- **Source**: ['Tab. 14']

## 自回归 WFM 12B 层数 / 模型维度
- **Value**: 40 层，dim=5,120
- **Rationale**: 40 层大型模型对应 12B 参数规模，生成质量优于 4B
- **Search range**: 28 ~ 48 层
- **Sensitivity**: 高
- **Source**: ['Tab. 14']

## 自回归 WFM FFN 隐藏维度
- **Value**: 14,336
- **Rationale**: SwiGLU 激活配合 14,336 隐藏维度（约模型维度 3.5×）
- **Search range**: 8192 ~ 20480
- **Sensitivity**: 中
- **Source**: ['Tab. 14']

## 自回归 WFM Key/Value 注意力头数
- **Value**: 8
- **Rationale**: GQA 设计减少 KV cache 内存开销，与 LLM 主流实践一致
- **Search range**: 4 ~ 32
- **Sensitivity**: 中
- **Source**: ['Tab. 14']

## RoPE 时序频率缩放基 θ
- **Value**: 500,000
- **Rationale**: 支持更长上下文的 RoPE 基频，自回归 WFM 需外推更长时序
- **Search range**: 10,000 ~ 1,000,000
- **Sensitivity**: 高：影响长序列位置编码外推能力
- **Source**: ['Tab. 14']

## 视频分词器词表大小
- **Value**: 64,000
- **Rationale**: FSQ 量化 (8,8,8,5,5,5) 对应 8×8×8×5×5×5=64,000，足够表示丰富视觉内容
- **Search range**: 32000 ~ 131072
- **Sensitivity**: 高：词表影响自回归训练难度与信息保真度
- **Source**: ['Sec. 4.1', 'Sec. 5.2.1']

## 离散分词器 FSQ 量化层级
- **Value**: (8,8,8,5,5,5)
- **Rationale**: 6 维 FSQ 无需 commitment loss，避免 VQ 的码本崩溃风险，训练更稳定
- **Search range**: 固定配置
- **Sensitivity**: 高：量化层级决定信息保留量与词表大小
- **Source**: ['Sec. 4.1']

## 连续分词器潜空间维度
- **Value**: 16
- **Rationale**: 16 维连续向量在压缩率与信息保真度之间平衡
- **Search range**: 8 ~ 32
- **Sensitivity**: 中
- **Source**: ['Sec. 4.1']

## 视频连续分词器时空压缩率（CV，用于扩散 WFM）
- **Value**: 8×8×8 (T×H×W)
- **Rationale**: 为扩散 WFM 提供压缩适中的连续潜表示，平衡画质与计算量
- **Search range**: 4×8×8 ~ 8×16×16
- **Sensitivity**: 高：压缩率影响 token 数量与重建质量权衡
- **Source**: ['Tab. 10', 'Sec. 5.1']

## 视频离散分词器时空压缩率（DV，用于自回归 WFM）
- **Value**: 8×16×16 (T×H×W)
- **Rationale**: 激进压缩减少自回归 token 数，但需扩散解码器弥补画质损失
- **Search range**: 4×8×8 ~ 8×16×16
- **Sensitivity**: 高：过高压缩引入模糊，需配合扩散解码器
- **Source**: ['Tab. 10', 'Sec. 5.2.5']

## Medusa 头数（最优）
- **Value**: 9
- **Rationale**: 实验表明 9 个 Medusa 头在 token 吞吐量与前向传播次数之间取得最优平衡；更多头会降低整体吞吐量
- **Search range**: 3 ~ 12
- **Sensitivity**: 中：头数过多反而降低吞吐量
- **Source**: ['Sec. 5.2.4', 'Tab. 15']

## FSDP 分片因子（扩散 WFM）
- **Value**: 7B: 32，14B: 64
- **Rationale**: 更大模型需更高分片因子以适配 H100 80GB 内存限制
- **Search range**: 16 ~ 128
- **Sensitivity**: 高：直接影响每 GPU 内存用量
- **Source**: ['Sec. 5.1.4']

## Context Parallelism (CP) 大小（高分辨率阶段）
- **Value**: 8
- **Rationale**: CP_SIZE=8 将激活显存从约 310 GB 分摊到 40 GB/GPU，适配长上下文（56,320 tokens）
- **Search range**: 2 ~ 16
- **Sensitivity**: 高：影响激活内存与通信开销
- **Source**: ['Sec. 5.1.4', 'Tab. 12']
