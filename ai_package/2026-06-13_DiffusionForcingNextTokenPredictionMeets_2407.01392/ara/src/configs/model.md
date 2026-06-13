## causal_diffusion_forcing_backbone
- **Value**: 主实验采用 RNN；正文称 minimal implementation 使用 vanilla Recurrent Neural Network。
- **Rationale**: CDF 需要 future tokens 只依赖 past noisy tokens，RNN 提供因果架构并适合 online decision-making。
- **Search range**: RNN 或 masked transformer；transformer 扩展在 Appendix B.1 讨论但不是主实现。
- **Sensitivity**: 论文称 transformer 可能提升部分结果，但 RNN 更适合在线决策的灵活性和效率。
- **Source**: Sec 3.2; Appendix B.1; Appendix D.2

## video_dynamics_model
- **Value**: transition model 使用 typical diffusion U-net，U-net 输出送入 GRU，z_t-1 作为 GRU hidden state。
- **Rationale**: video diffusion 中 x 与 z 都是 channel、width、height 形式的 2D tensor，U-net 负责扩散去噪，GRU 维护递归 latent。
- **Search range**: 视频实现使用 U-net 加 GRU；论文未列出 U-net 层数。
- **Sensitivity**: 作者认为 causal transformer 可能获得更好结果，但为效率与训练时长保留 RNN 实现。
- **Source**: Appendix D.2

## video_observation_model
- **Value**: observation model 使用 1-layer resnet 后接 conv layer。
- **Rationale**: 该 observation model 将 GRU 输出的 latent 转换为 x_hat。
- **Search range**: 论文只给出 1-layer resnet 加 conv layer。
- **Sensitivity**: 论文未报告 observation model 结构消融。
- **Source**: Appendix D.2

## latent_channels
- **Value**: DMLab 的 z channel 为 16；Minecraft 的 z channel 为 32。
- **Rationale**: 视频任务中 z 与 x 共享 width 和 height，并通过不同 channel 数控制 latent 容量。
- **Search range**: DMLab 16；Minecraft 32。
- **Sensitivity**: 作者说更多参数可能改善 Minecraft，但为保持训练时长合理而留给 future works。
- **Source**: Appendix D.2

## parameter_count
- **Value**: Minecraft model 为 36 million parameters；DMLab model 为 24 million parameters；maze planning 为 4.33 million parameters。
- **Rationale**: 参数量反映不同任务模型容量。
- **Search range**: 4.33 million 到 36 million parameters。
- **Sensitivity**: 作者提到更大的 Minecraft 模型可能更好，但未实验。
- **Source**: Appendix D.2

## non_video_backbone
- **Value**: 非视频非图像的 x 使用 residue MLPs 作为 dynamics model backbone；输出送入 GRU，另一个 ResMLP 作为 observation model。
- **Rationale**: 非空间数据不使用 U-net，而用 MLP 版本的 ResNet 结构处理低维 token。
- **Search range**: residue MLP 加 GRU 加 ResMLP observation model。
- **Sensitivity**: 论文未给出非视频 backbone 消融。
- **Source**: Appendix D.2

## time_series_architecture
- **Value**: 1 mlp and 4 grus。
- **Rationale**: 时间序列回归沿用 pytorch-ts 实现，并使用同一架构和 batch size。
- **Search range**: 论文只列出 1 mlp and 4 grus。
- **Sensitivity**: 论文称所有 time series datasets and experiments 使用 exact same architecture and hyperparameters。
- **Source**: Sec E.1; Appendix D.9

## transformer_extension
- **Value**: 可将 transformer-based sequence diffusion model 修改为跨 token 独立噪声级别训练；严格 causal DF 可使用 causal attention mask。
- **Rationale**: Appendix B.1 说明 Diffusion Forcing 可扩展到 transformers，也可通过控制未来 token 噪声实现不同程度因果性。
- **Search range**: causal attention mask、future full white noise、future noise-free、future noisy 等设定。
- **Sensitivity**: 这些扩展超出论文范围，但作者称已验证有效性并作为 future works 直觉。
- **Source**: Appendix B.1
