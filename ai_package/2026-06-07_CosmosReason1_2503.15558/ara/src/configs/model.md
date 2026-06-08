## Cosmos-Reason1-7B 视觉编码器
- **Value**: ViT-676M，32 层，模型维度 1280，FFN 隐层维度 3456，patch 大小 14×14，输入动态分辨率
- **Rationale**: 继承 Qwen2.5-VL 的视觉编码器，复用其强大的图像与视频理解预训练能力
- **Search range**: 固定（继承预训练模型）
- **Sensitivity**: low
- **Source**: Tab. 3, Sec. 3.1

## Cosmos-Reason1-56B 视觉编码器
- **Value**: InternViT-300M-V2.5，24 层，模型维度 1024，FFN 隐层维度 4096，patch 大小 14×14，输入固定 448×448
- **Rationale**: 轻量级视觉编码器与大规模混合 LLM 主干搭配，控制总参数量与计算开销
- **Search range**: 固定（继承预训练模型）
- **Sensitivity**: low
- **Source**: Tab. 3, Sec. 3.1

## Cosmos-Reason1-7B 投影层（Projector）
- **Value**: 2 层 MLP，时空下采样因子 2×2×2，输入维度 1280，隐层维度 5120，输出维度 3584
- **Rationale**: 时空三维下采样将视频 token 数压缩至 1/8，同时对齐视觉特征至 LLM 嵌入空间维度
- **Search range**: 固定
- **Sensitivity**: medium
- **Source**: Tab. 3

## Cosmos-Reason1-56B 投影层（Projector）
- **Value**: 2 层 MLP，空间下采样因子 2×2×1（时间维不压缩），输入维度 4096，隐层维度 32768，输出维度 8192
- **Rationale**: 仅对空间维度下采样以对齐 56B LLM 主干的高维嵌入空间，保留时序连续性
- **Search range**: 固定
- **Sensitivity**: medium
- **Source**: Tab. 3

## Cosmos-Reason1-7B LLM 主干架构
- **Value**: 纯 Transformer，28 层，模型维度 3584，FFN 隐层维度 18944，注意力头数 28
- **Rationale**: 密集 Transformer 架构成熟稳定，在中等规模下推理能力突出，适合 7B 规模模型
- **Search range**: 固定（继承 Qwen2.5-VL LLM 主干）
- **Sensitivity**: low
- **Source**: Tab. 3, Sec. 3.1

## Cosmos-Reason1-56B LLM 主干架构
- **Value**: 混合 Mamba-MLP-Transformer（Nemotron-H），118 层，模型维度 8192，FFN 隐层维度 32768，注意力头数 64
- **Rationale**: Mamba 的线性序列建模降低长序列计算复杂度，少量 Transformer 层负责长距离上下文建模，两者互补
- **Search range**: 固定（继承 Nemotron-H 预训练模型）
- **Sensitivity**: medium
- **Source**: Tab. 3, Sec. 3.2

## 视频帧采样参数
- **Value**: 均匀采样，最多 32 帧，最高采样率 2fps，每帧缩放至 448×448 像素
- **Rationale**: 固定帧预算控制计算量；2fps 足以覆盖大多数 Physical AI 场景的时序动态变化
- **Search range**: 最多 32 帧
- **Sensitivity**: medium
- **Source**: Sec. 3.1

## 视频帧视觉 token 数量
- **Value**: 视觉编码器输出 1024 tokens/帧；经 PixelShuffle 2×2 下采样后压缩为 256 tokens/帧
- **Rationale**: PixelShuffle 将空间维度折叠至通道维度，以 4 倍压缩比减少 LLM 输入序列长度，降低注意力计算开销
- **Search range**: 固定
- **Sensitivity**: medium
- **Source**: Sec. 3.1

## 图像动态分块策略（56B）
- **Value**: 动态调整长宽比后切分为 1 至 12 个 448×448 分块，另附全图缩略图分块
- **Rationale**: 动态分块保留高分辨率细节，全图缩略图分块保留全局上下文，设计参考 NVLM-D
- **Search range**: 1 至 12 个分块
- **Sensitivity**: medium
- **Source**: Sec. 3.1

## 7B 模型训练并行策略
- **Value**: 张量并行 TP=4
- **Rationale**: 7B 规模通过张量并行切分，避免流水线并行引入的气泡开销
- **Search range**: 固定
- **Sensitivity**: low
- **Source**: Sec. 3.2

## 56B 模型训练并行策略
- **Value**: 张量并行 TP=8，流水线并行 PP=2
- **Rationale**: 56B 规模需结合张量并行与流水线并行以适配显存约束，策略训练节点另支持 CP 和 FSDP
- **Search range**: 固定
- **Sensitivity**: low
- **Source**: Sec. 3.2
