## 总体架构
- **Value**: Genie 由 spatiotemporal video tokenizer、autoregressive dynamics model 和 latent action model 组成，总参数约 10.7B；摘要中称 11B parameters
- **Rationale**: 三个组件共同把视频压缩为 token、从相邻帧推断 latent actions，并在给定历史 token 与 action 时预测下一帧。
- **Search range**: 主 Genie 为 Platformers 模型；另有 Robotics 模型和 CoinRun 可复现实例
- **Sensitivity**: 三组件相互依赖；tokenizer 与 LAM 的设计选择会影响 fidelity 与 controllability。
- **Source**: Abstract；Sec 2.1；Sec 3.1

## ST-transformer
- **Value**: 所有模型组件都使用 ST-transformer，交替 spatial attention 与 temporal attention，并在 spatial 与 temporal 后只保留一个 FFW
- **Rationale**: 论文用它缓解视频 token 的 quadratic memory cost，并让主要计算随帧数线性增长。
- **Search range**: 应用于 video tokenizer、LAM、dynamics model 与 BC policy encoder
- **Sensitivity**: 省略 post-spatial FFW 被论文称为显著改善结果；ST-ViViT 消融优于 ViT 与 C-ViViT。
- **Source**: Sec 2 Methodology；Sec 2.1；Sec 3.4；Table 3

## video tokenizer
- **Value**: 200M parameters，patch size 4，codebook embedding size 32，1024 unique codes；Platformers tokenizer encoder 为 num_layers 12、d_model 512、num_heads 8，decoder 为 num_layers 20、d_model 1024、num_heads 16
- **Rationale**: tokenizer 将视频压缩为离散表示，降低维度并提升视频生成质量。
- **Search range**: Table 7 给出 Platformers 配置；Table 15 给出 CoinRun 小规模配置
- **Sensitivity**: tokenizer 架构敏感；ST-ViViT 在 FVD 与 controllability 方向上优于 spatial-only ViT 与 C-ViViT。
- **Source**: Sec 3 Training Details；Appendix C.2 Table 7；Appendix F.2 Table 15；Table 3

## latent action model
- **Value**: 300M parameters，patch size 16，codebook embedding size 32，8 unique codes；Platformers action model encoder num_layers 20、d_model 1024、num_heads 16，decoder num_layers 20、d_model 1024、num_heads 16
- **Rationale**: LAM 在无 action labels 的视频中学习离散 latent actions，并将 action vocabulary 限制为小集合以便 human playability 与 controllability。
- **Search range**: 主实验使用 |A| = 8；CoinRun case study action model 使用 num_codes 6
- **Sensitivity**: 论文指出增加 codes 有收益，但会降低 human 与 AI agents 的 playability；pixel-input 比 token-input controllability 更好。
- **Source**: Sec 2.1 Latent Action Model；Sec 3 Training Details；Appendix C.1 Table 5；Appendix F.3 Table 16；Table 2

## dynamics model
- **Value**: decoder-only MaskGIT transformer；最终 Genie dynamics 为 10.1B parameters，48 layers，36 heads，d_model 5120，kq size 128，FLOPs 为 6.6 × 10^22
- **Rationale**: dynamics model 给定历史 video tokens 与 stopgrad latent actions，预测下一帧 token。
- **Search range**: scaling models 从 41M 到 2.7B；batch scaling 使用 2.3B 架构；最终模型 10.1B dynamics
- **Sensitivity**: 模型规模增加带来训练 loss 方向上的一致改善；batch size 增加也带来有利增益。
- **Source**: Sec 2.1 Dynamics Model；Sec 3.1；Appendix C.3 Table 10；Table 11；Table 12

## latent action 注入方式
- **Value**: 将 latent actions 作为 additive embeddings 用于 latent action 和 dynamics models
- **Rationale**: 论文比较常见做法是把 action concat 到对应 frame，但报告 additive embeddings 有助于提高 controllability。
- **Search range**: 适用于 LAM 与 dynamics model
- **Sensitivity**: 这是 controllability 相关设计选择；论文没有给该选择的单独数字表。
- **Source**: Sec 2.1 Dynamics Model

## LAM 训练与推理差异
- **Value**: 训练时 LAM encoder 和 decoder 提供 VQ-VAE training signal；推理时除 VQ codebook 外丢弃整个 LAM，由 user actions 替代
- **Rationale**: decoder 只用于给 LAM 训练信号；交互生成时用户选择离散 latent action index。
- **Search range**: user action 取值为 [0, |A|)；主实验 |A| = 8
- **Sensitivity**: 训练期学习 action vocabulary，推理期控制依赖 codebook 与 dynamics model 对 action embedding 的响应。
- **Source**: Sec 2.1 Latent Action Model；Sec 2.2 Inference

## BC policy model
- **Value**: 使用 transformer policy，ST-ViViT encoder；encoder num_layers 12，d_model 512，patch_size 4；policy linear_layer 512
- **Rationale**: 用于验证 Genie LAM 的 latent actions 可迁移到 unseen CoinRun videos 的 imitation。
- **Search range**: oracle targets 为 real actions，Genie LAM targets 为 latent actions
- **Sensitivity**: policy 质量受 LAM 标注、latent-to-real mapping 和 expert labels 数量影响。
- **Source**: Appendix E.2；Table 14
