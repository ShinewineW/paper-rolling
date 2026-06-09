## backbone
- **Value**: Wan2.2-5B
- **Rationale**: 预训练视频Diffusion Transformer骨干网络，包含视频DiT、T5文本编码器和视频VAE
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 4.1

## action_expert_hidden_dim
- **Value**: 1024
- **Rationale**: 动作专家DiT的隐藏维度da，与视频DiT共享架构但维度缩减以控制参数量
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 4.1

## action_expert_params
- **Value**: 1B
- **Rationale**: 动作专家分支的参数规模
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## total_model_params
- **Value**: 6B
- **Rationale**: Fast-WAM整体模型参数量（Wan2.2-5B骨干加1B动作专家）
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## architecture_type
- **Value**: Mixture-of-Transformer (MoT) with shared attention
- **Rationale**: 视频DiT与动作专家DiT通过共享注意力集成于统一框架，结构化注意力掩码控制信息流
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 3.2

## inference_denoising_steps
- **Value**: 10
- **Rationale**: 推理时动作去噪的迭代步数
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## cfg_scale
- **Value**: 1.0
- **Rationale**: 推理时classifier-free guidance比例
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1

## text_encoder
- **Value**: T5
- **Rationale**: Wan2.2内置T5文本编码器，通过cross-attention为所有token提供语言条件
- **Search range**: None
- **Sensitivity**: low
- **Source**: Sec 3.2

## attention_mask_type
- **Value**: 结构化注意力掩码（structured attention mask）
- **Rationale**: 控制干净第一帧token、噪声未来视频token与动作token之间的信息流方向，防止未来信息泄露到动作分支
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 3.2, Figure 2b

## inference_latency
- **Value**: 190 ms
- **Rationale**: Fast-WAM在单张NVIDIA RTX 5090D V2 32GB GPU上的实测推理延迟
- **Search range**: None
- **Sensitivity**: high
- **Source**: Sec 4.1, Sec 4.3.3

## multi_camera_input
- **Value**: 多路摄像头图像在送入VAE前拼接为单张图像
- **Rationale**: 通过图像拼接融合多视角观测，无需修改VAE输入接口
- **Search range**: None
- **Sensitivity**: medium
- **Source**: Sec 4.1
