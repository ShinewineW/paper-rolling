# Environment
- **Python**: 论文未明确说明
- **Framework**: DeepSpeed ZeRO-2（分布式训练策略，含activation checkpointing）；FlashAttention v2（世界模型注意力加速）；余弦β噪声调度（视频解码器）；v-parameterization扩散目标（视频解码器）；DDIM采样器（推理）
- **Hardware**: 图像tokenizer：32块A100 80GB GPU，训练约4天；世界模型：64块A100 80GB GPU，训练约15天；视频解码器：32块A100 80GB GPU，训练约15天
- **Key dependencies**: AdamW优化器, FlashAttention v2, DeepSpeed ZeRO-2, T5-large（预训练文本编码器）, DINO（预训练自监督视觉模型，用于语义蒸馏）, DDIM采样器, 余弦β噪声调度, v-parameterization扩散训练目标, 指数移动平均（EMA）
- **Random seeds**: 论文未明确报告随机种子
