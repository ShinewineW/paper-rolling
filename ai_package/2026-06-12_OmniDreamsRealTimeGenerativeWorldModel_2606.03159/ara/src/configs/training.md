## 基础训练来源
- **Value**: 从 Cosmos-Predict 2.5 出发，先在 RDS 上 mid-train，再用 RDS-HQ-1M 做 finetuning 与 post-training
- **Rationale**: 先注入 AV 场景能力，再用高质量世界场景标注数据加强控制与后训练。
- **Search range**: RDS 为 16,600 h、3M 20s clips；RDS-HQ-1M 为 4,944 h、1,142,285 clips。
- **Sensitivity**: 高；数据域、标注质量和长尾覆盖直接影响闭环仿真与可控生成。
- **Source**: Sec. 2.1, Sec. 2.4, Sec. 4

## 相机视角训练配置
- **Value**: 原始数据含 7 synchronized cameras；训练表中标注为 7 in total, 4 in training
- **Rationale**: 多视角模型重点覆盖 front-wide、cross-left、cross-right、front-telescope，以服务闭环策略常用视角。
- **Search range**: 最多支持 up to 7 synchronized views；核心 MV 训练和实时演示使用 4 views。
- **Sensitivity**: 中到高；视角数量提升一致性需求和推理计算量。
- **Source**: Sec. 2.1, Tab. 1, Sec. 3.2, Sec. 4.1

## 文本提示生成
- **Value**: 使用 Qwen2.5-VL-7B 对 10s-long temporal windows 独立 caption 7 cameras，并生成 short、medium、long 三种长度
- **Rationale**: 让模型学习天气、光照、时间和交通外观的文本控制。
- **Search range**: short ≈40 words、medium ≈80 words、long ≈200 words；采样概率 0.1/0.2/0.7。
- **Sensitivity**: 中；prompt 长度鲁棒性和环境可控性依赖该配置。
- **Source**: Sec. 2.2

## 世界场景标注处理
- **Value**: 3D detection and tracking 以 10 FPS 运行并插值到 30 FPS 匹配视频帧率
- **Rationale**: 将动态对象轨迹与视频帧对齐，提供可用于 world-scenario map 的结构控制。
- **Search range**: HD map 标签来自 pre-constructed city-level map；动态对象包括 vehicles、pedestrians 和 other vulnerable road users。
- **Sensitivity**: 高；标注不可靠会直接污染控制信号。
- **Source**: Sec. 2.2

## 数据过滤与去重
- **Value**: 移除 unreliable sensor data、unreliable annotations、prediction disagreements、VLM 检测到的 visual artifacts，并按 ego-trajectory 和 visual features 去重
- **Rationale**: 减少时序不一致和视觉瑕疵，支持 artifact-free rollouts。
- **Search range**: 覆盖传感器、自动标注、视觉质量和重复片段多个阶段。
- **Sensitivity**: 高；过滤不足会影响生成稳定性，过度过滤会削弱场景多样性。
- **Source**: Sec. 2.3

## 评估留出集
- **Value**: 从训练集中 hold out 5,000 clips，另取 300 个 60 s 版本用于长时一致性评估
- **Rationale**: 评估集按 road users、large vehicles、weather and lighting、rare infrastructure 平衡，而非按训练分布比例抽样。
- **Search range**: Sec. 9.1 中定量质量评估使用其中 1,000 clips。
- **Sensitivity**: 中；留出集构成影响长尾和长时评估结论。
- **Source**: Sec. 2.4, Sec. 9.1

## 多视角适配训练
- **Value**: 启用 learnable view embeddings，先在 front-wide、cross-left、cross-right、front-telescope 的 uniform mix 上训练，再加入 cross-view attention layers 训练 multi-view videos
- **Rationale**: 让模型学习特殊相机内参、运动模式以及跨视角一致性。
- **Search range**: view embeddings 和 cross-view attention output projection weights 均 zero-initialized。
- **Sensitivity**: 高；初始化和训练顺序影响收敛稳定性。
- **Source**: Sec. 4.1

## 文本到视频与图像到视频混合
- **Value**: 训练使用 1:1 mixture of text-to-video and image-to-video tasks
- **Rationale**: 同时支持 first-frame conditioning 并保持生成新内容的能力。
- **Search range**: 论文仅给出 1:1 混合比例，未列出其他比例实验。
- **Sensitivity**: 中；比例变化可能改变首帧保真与开放生成之间的平衡。
- **Source**: Sec. 4.1

## world-scenario control 训练长度
- **Value**: 先训练 93-frame clips 至收敛，再扩展到 189-frame clips
- **Rationale**: 先提升训练效率，再学习更长时程一致性。
- **Search range**: 适用于向预训练或多视角适配权重追加 world-scenario control branch 的阶段。
- **Sensitivity**: 高；短片段不足会削弱长时一致性，长片段成本更高。
- **Source**: Sec. 4.1

## 因果化训练
- **Value**: 使用 causal masking 与 Diffusion Forcing 将 bidirectional models 转为 autoregressive causal models
- **Rationale**: 闭环仿真要求每步只依赖过去观察和当前条件。
- **Search range**: 先从无 world-scenario control 权重在 RDS 上训练，再添加 control branch 并用 RDS-HQ-1M 继续 Diffusion Forcing。
- **Sensitivity**: 高；该阶段决定自回归生成与闭环响应能力。
- **Source**: Sec. 4.2

## Self Forcing DMD 蒸馏
- **Value**: 采用 Self Forcing self-rollout 与 DMD 的 video-level distribution matching objective
- **Rationale**: 减少 teacher forcing 与推理时自生成上下文之间的 exposure bias，并支持 few-step generation。
- **Search range**: 实现中使用 ??=2，timestep schedule 为 [1000, 450]；每次迭代只对单个随机 denoising step 反传。
- **Sensitivity**: 高；决定实时少步生成和长 rollout 误差累积。
- **Source**: Sec. 4.3

## 渐进长上下文教师
- **Value**: 先用 short-context teacher 蒸馏，再用 long-context bidirectional teacher 继续 finetuning
- **Rationale**: 缓解 rolling KV cache 超出训练上下文窗口后的 shifting artifacts。
- **Search range**: 用于长自回归 rollout 稳定性提升。
- **Sensitivity**: 高；论文明确称该策略对高质量 long rollout 成功关键。
- **Source**: Sec. 4.3, Sec. 9.2

## 动态 cuboid dropout 后训练
- **Value**: 另一个 OmniDreams 变体在 post-training 中随机移除 dynamic cuboids，同时保留 parked vehicles 等 static cuboids
- **Rationale**: 避免模型完全依赖动态 cuboid，让未显式标注轨迹的 OOD 物体可从首帧和视觉历史中延续。
- **Search range**: 面向 out-of-distribution object modeling。
- **Sensitivity**: 中；提升 OOD 灵活性，但可能改变结构控制依赖方式。
- **Source**: Sec. 9.3.2
