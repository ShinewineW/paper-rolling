# Related Work

## R1: Hu et al., VPP(Video Prediction Policy), 2024; arXiv:2412.14803
- **DOI**: 10.48550/arXiv.2412.14803
- **Type**: 相关方法
- **Delta**:
  - What changed: VPP从视频扩散模型提取预测性视觉表示作为策略条件信号;Fast-WAM通过联合视频协训练目标在训练期塑造视频骨干的世界表示,测试时直接单次前向编码,无需任何形式的未来帧特征提取
  - Why: VPP同样探索了利用视频建模辅助动作预测同时减少测试时显式视频合成的思路,与Fast-WAM的核心研究问题密切相关
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R2: Li et al., UVA(Unified Video Action model), 2025; arXiv:2503.00200
- **DOI**: 10.48550/arXiv.2503.00200
- **Type**: 相关方法
- **Delta**:
  - What changed: UVA联合建模视频和动作并在测试时跳过视频解码以加速推理;Fast-WAM进一步通过受控变体明确解耦训练期视频协训练与测试期未来想象各自的贡献
  - Why: UVA是最接近Fast-WAM的相关工作之一,同样联合建模视频和动作并在测试时规避完整视频生成
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: []

## R3: Li et al., LingBot-VA(Causal World Modeling), 2026; arXiv:2601.21998
- **DOI**: 10.48550/arXiv.2601.21998
- **Type**: 基线方法/imagine-then-execute WAM代表(video-then-action范式)
- **Delta**:
  - What changed: Fast-WAM提出不依赖具身预训练即可达到与LingBot-VA相近的性能;受控变体Fast-WAM-IDM直接实现了LingBot-VA的video-then-action推理范式用于受控对比
  - Why: LingBot-VA是采用因果世界建模(先生成视频再预测动作)的代表性WAM方法,提供了直接对比基线并启发了Fast-WAM-IDM变体的设计
- **Claims affected**: ['C1', 'C2', 'C4']
- **Adopted elements**: ['video-then-action推理结构(在Fast-WAM-IDM变体中实现)', 'noise augmentation(p=0.5)用于视频token']

## R4: Ye et al., WAM(World Action Models are Zero-Shot Policies), 2026; arXiv:2602.15922
- **DOI**: 10.48550/arXiv.2602.15922
- **Type**: 概念框架/基线方法(联合去噪范式)
- **Delta**:
  - What changed: Fast-WAM沿用WAM的「视频协训练+动作生成」框架概念,但解耦了训练期视频建模与测试期未来想象,而原WAM在测试时仍执行显式联合视频-动作去噪
  - Why: 该工作提出了「World Action Models」术语,将WAM定义为利用世界建模支持下游动作预测的具身策略系统,并提供了联合去噪范式作为Fast-WAM-Joint变体的参考
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['WAM概念框架', '联合视频动作去噪训练范式(作为Fast-WAM-Joint变体的参考设计)']

## R5: Bi et al., Motus, 2025; arXiv:2512.13030
- **DOI**: 10.48550/arXiv.2512.13030
- **Type**: 基线方法(潜在动作世界模型)
- **Delta**:
  - What changed: Fast-WAM在无具身预训练情况下实现超越有具身预训练的Motus的性能
  - Why: Motus是采用统一潜在动作世界模型的WAM方法,是最强的有预训练基线之一,提供了关键的上界对比
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R6: Team Wan et al., Wan2.2-5B, 2025; arXiv:2503.20314
- **DOI**: 10.48550/arXiv.2503.20314
- **Type**: 预训练骨干组件
- **Delta**:
  - What changed: Fast-WAM将Wan2.2-5B的视频DiT重新用于单次前向编码作为世界编码器,并添加动作专家DiT分支,而非按原始用途执行迭代视频生成
  - Why: Wan2.2-5B提供了在大规模视频数据上预训练的视频生成DiT骨干及配套T5文本编码器和视频VAE,是Fast-WAM视频世界建模能力的基础
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['Wan2.2-5B视频DiT骨干', 'T5文本编码器(通过cross-attention供所有token使用)', '视频VAE(将视觉观测映射为潜在视频token)', 'logit-normal噪声调度']
