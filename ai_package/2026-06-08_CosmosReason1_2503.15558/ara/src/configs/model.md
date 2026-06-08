## Cosmos-Reason1-7B 视觉编码器
- **Value**: ViT-676M，动态输入尺寸，patch 14×14，32 层，模型维度 1280，FFN 维度 3456
- **Rationale**: 沿用 Qwen2.5-VL 的视觉编码器以充分利用其预训练视觉表示
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3, Sec 3.1

## Cosmos-Reason1-56B 视觉编码器
- **Value**: InternViT-300M-V2.5，输入 448×448，patch 14×14，24 层，模型维度 1024，FFN 维度 4096
- **Rationale**: 轻量视觉编码器与大型混合 LLM 主干搭配以控制整体参数量与推理成本
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3, Sec 3.1

## Cosmos-Reason1-7B Projector
- **Value**: 2 层 MLP，空间降采样 2×2×2，输入维度 1280，隐层维度 5120，输出维度 3584
- **Rationale**: 通过 PixelShuffle 类降采样将视觉 token 数压缩，以减轻 LLM 输入序列长度
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3

## Cosmos-Reason1-56B Projector
- **Value**: 2 层 MLP，空间降采样 2×2×1（时序不压缩），输入维度 4096，隐层维度 32768，输出维度 8192
- **Rationale**: 与 56B LLM 主干维度对齐；视频帧时序维度不压缩
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3

## Cosmos-Reason1-7B LLM 主干
- **Value**: Dense Transformer，28 层，模型维度 3584，FFN 维度 18944，28 个注意力头
- **Rationale**: 基于 Qwen2.5-VL 预训练密集 Transformer，适合 7B 规模的统一多模态处理
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3, Sec 3.1

## Cosmos-Reason1-56B LLM 主干
- **Value**: Mamba-MLP-Transformer 混合架构（Nemotron-H），118 层，模型维度 8192，FFN 维度 32768，64 个注意力头
- **Rationale**: 混合架构兼顾长序列线性时间复杂度（Mamba SSM）与细节捕获能力（Transformer 自注意力），适合长视频推理
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Tab. 3, Sec 3.2

## 视频帧采样策略（56B）
- **Value**: 均匀采样最多 32 帧，最高采样率 2 fps，每帧缩放至 448×448
- **Rationale**: 平衡视频时序覆盖范围与推理计算成本
- **Search range**: 0–32 帧
- **Sensitivity**: 未报告
- **Source**: Sec 3.1

## 视觉 token 压缩（56B，每帧）
- **Value**: 视觉编码器输出 1024 tokens/帧，经 2×2 PixelShuffle 降采样至 256 tokens/帧
- **Rationale**: 将空间维度合并至通道维度以降低 LLM 输入序列长度，减少注意力计算开销
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 3.1

## 图像分块策略（56B）
- **Value**: 动态调整至预定义宽高比，分割为 1–12 个 448×448 的 tile，附加一张 thumbnail tile 保留全局上下文
- **Rationale**: 高分辨率图像保留局部细节的同时通过 thumbnail 维持全局理解
- **Search range**: 1–12 tiles
- **Sensitivity**: 未报告
- **Source**: Sec 3.1
