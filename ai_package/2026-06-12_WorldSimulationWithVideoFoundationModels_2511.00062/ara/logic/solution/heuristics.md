# Heuristics

## H1: 训练 timestep 从 logit-normal 分布采样，并随分辨率提升使用 progressive timestep shift，使样本更多覆盖高噪声区域。
- **Rationale**: 论文指出高分辨率内容存在邻近像素相关性，噪声过小时模型难以打破相关性；偏向高噪声能帮助模型学习在相关性被破坏时重建信号。
- **Sensitivity**: 过低会导致高噪声区域暴露不足并出现突兀、不自然的帧间转场；过高可能让训练过度偏向强噪声样本，论文未系统给出上界。
- **Bounds**: 按论文中 shifted logit-normal 和 resolution-dependent shift 的设定执行；最高噪声尾部额外采样比例按论文原设置，不在此处外推。
- **Code ref**: [Sec. 3.1 Flow Matching; Sec. 4.1 Pre-training]
- **Source**: 论文明确陈述 shifted logit-normal、progressive timestep shift 和最高噪声尾部定向采样。

## H2: Image2World 和 Video2World 使用 frame-replacement，把生成序列初始 frames 持续替换为条件 frames。
- **Rationale**: 论文称该策略既允许按任务调整条件 frames 数量，也能让早期 frames 忠实于输入，从而增强时间一致性。
- **Sensitivity**: 条件 frames 太少会降低输入视觉线索传播；条件 frames 太多会压缩自由生成区间，论文未给出通用最优点。
- **Bounds**: 仅用于 Image2World 和 Video2World；Text2World 没有 reference image 或 video frames。
- **Code ref**: [Sec. 3.2 Network Architecture]
- **Source**: 论文明确描述 frame-replacement strategy 的两个目的。

## H3: 预训练按任务和分辨率渐进：先 Text2Image，再联合 Image2World 和 Video2World，最后加入 Text2World。
- **Rationale**: 论文解释先学单帧质量，再引入运动和时间一致性，随后提升分辨率和任务多样性。
- **Sensitivity**: 过早加入复杂视频任务可能影响单帧质量基础；过慢推进会降低多任务统一训练效率，论文以收敛和视觉质量平台作为切换信号。
- **Bounds**: 阶段切换以模型收敛和 visual quality plateau 为准；denoising loss 只作用于指定 frames。
- **Code ref**: [Sec. 4.1 Pre-training]
- **Source**: 论文明确给出 progressive pretraining procedure 和 masking scheme。

## H4: domain-specific SFT 先分别训练专域模型，再通过 model merging 统一优势。
- **Rationale**: 论文称专域 SFT 能充分利用专域数据且避免混合数据比例平衡问题；轻微 general-domain degradation 可由 merging 缓解。
- **Sensitivity**: 单一 joint SFT 需要调 mixture ratios；基于单个 fine-tuned model win rate 的启发式选择不如 grid search，论文选择 model soup 作为最终 post-trained model。
- **Bounds**: 候选 merging 方法限定为论文实验的 model soup、TIES、DARE-Linear 和 DARE-TIES；最终选择来自人工质量评估和更大评估集 human preference voting。
- **Code ref**: [Sec. 4.2.1 Supervised Fine-tuning]
- **Source**: 论文明确比较 merging 方法并说明最终选择 model soup。

## H5: RL post-training 对每个条件生成一组 rollout，用 VideoAlign 计算 reward，并在组内归一化 advantage。
- **Rationale**: 论文将条件视作 states、denoising trajectories 视作 actions，用 reward model 对 text alignment、motion quality 和 visual quality 对齐。
- **Sensitivity**: reward hacking 是主要风险；论文用 fine-tuning dataset 上的 diffusion loss regularization 缓解。
- **Bounds**: 论文由于 GPU memory constraint 将 trajectory probability 分解为每步 conditional probabilities，并分段累积梯度。
- **Code ref**: [Sec. 4.2.2 Reinforcement Learning]
- **Source**: 论文明确描述 VideoAlign、GRPO 风格 advantage、trajectory probability decomposition 和 diffusion loss regularization。

## H6: Cosmos-Transfer2.5 将 control blocks 更均匀地插入主干，而不是集中放在开头。
- **Rationale**: 论文称这样在保持 control blocks 总量的同时，让 conditioning information 更渐进地贯穿网络。
- **Sensitivity**: 控制注入太集中可能只在早期影响主干；过度分散或改变 blocks 数量的效果论文未报告。
- **Bounds**: 适用于 Cosmos-Transfer2.5-2B 相对 Cosmos-Transfer1-7B 的 control-net style 修改。
- **Code ref**: [Sec. 6.1 Cosmos-Transfer2.5]
- **Source**: 论文明确对比 control blocks sequential insertion 与 evenly distributed insertion。

## H7: action-conditioned 版本把 action embedder MLP 输出加到 DiT timestamp embeddings，而不是直接作为 cross-attention 或 channel concatenation。
- **Rationale**: 论文的消融表明 TimeEmbedding 方案方向上优于 CrossAtten 和 ChannelConcat。
- **Sensitivity**: 动作是预训练中不存在的新模态，注入位置影响动作条件和视频生成的耦合方式；论文只比较这三种路径。
- **Bounds**: 适用于 Cosmos-Predict2.5-2B/robot/action-cond 的 robot action sequence conditioning。
- **Code ref**: [Sec. 6.6 Action-Conditioned World Generation]
- **Source**: 论文明确描述 action embedder MLP 和三种动作注入方式的消融。
