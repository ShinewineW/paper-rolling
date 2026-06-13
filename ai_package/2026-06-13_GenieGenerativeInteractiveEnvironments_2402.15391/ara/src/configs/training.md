## 训练数据
- **Value**: Platformers 使用经过筛选的 6.8M 个 16s video clips，约 30k hours；原始候选来自 55M clips，约 244k hours；帧率为 10FPS，分辨率为 160x90
- **Rationale**: 论文将大规模公开 Internet 2D Platformer 视频作为主训练数据，并强调筛选后的高质量数据优于未筛选数据。
- **Search range**: 原始 55M videos 到筛选后 6.8M videos；主结果除特别说明外使用 Platformers
- **Sensitivity**: 数据质量敏感；论文报告 curated dataset 相比 original dataset 在 FVD 方向上更优。
- **Source**: Sec 3 Datasets；Appendix B.1；Table 4

## 训练阶段
- **Value**: 先训练 video tokenizer，再联合训练 latent action model 与 dynamics model
- **Rationale**: tokenizer 先把视频压缩为离散 token，后续 dynamics model 使用这些 token；LAM 直接从 pixels 学 latent actions。
- **Search range**: 两阶段流程；tokenizer 独立训练，LAM 与 dynamics model co-train
- **Sensitivity**: 阶段顺序对后续 token 预测和 latent action 学习是结构性依赖。
- **Source**: Sec 2.1 Model Components

## video tokenizer 优化器
- **Value**: AdamW，cosine decay，300k steps；max_lr 3e-4，min_lr 3e-4，β1 0.9，β2 0.9，weight_decay 1e-4，warmup_steps 10k
- **Rationale**: 论文在 Appendix C.2 给出 tokenizer 的优化器配置。
- **Search range**: 论文仅列出该配置；batch size scaling 比较 64 与 384
- **Sensitivity**: batch size 增大带来 marginal gain；decoder scaling 比 encoder scaling 更有效。
- **Source**: Appendix C.2；Table 6；Table 8

## dynamics model 优化器
- **Value**: max_lr 3e-5，min_lr 3e-6，β1 0.9，β2 0.9，weight_decay 1e-4，warmup_steps 5k
- **Rationale**: 论文在 Appendix C.3 的 Table 9 给出 dynamics model optimizer hyperparameters。
- **Search range**: 用于 scaling experiments 与 CoinRun 小规模复现实例中的 dynamics 加 LAM 训练
- **Sensitivity**: 论文未逐项消融优化器超参；但大规模训练同时使用 bfloat16 与 QK norm 来稳定。
- **Source**: Appendix C.3；Table 9；Sec 3 Training Details

## dynamics scaling 训练步数与 batch
- **Value**: 模型规模 scaling 使用 batch size 256，训练 200k steps，每次 run 约 750B training tokens；最终 Genie dynamics 使用 batch size 512，训练 125k steps，总计 942B tokens
- **Rationale**: 论文通过模型规模与 batch size scaling 决定最终 Genie 训练配置。
- **Search range**: 模型规模从 41M 到 2.7B 做 scaling；最终 dynamics 为 10.1B
- **Sensitivity**: 论文明确说增加模型规模与 batch size 都改善模型表现。
- **Source**: Sec 3.1；Appendix C.3；Table 10；Table 12

## 随机 masking
- **Value**: train time 对 input tokens z2:T-1 随机 masking，masking rate 从 0.5 到 1 的均匀分布采样
- **Rationale**: dynamics model 采用 decoder-only MaskGIT 训练，并对输入 token 做随机 mask。
- **Search range**: masking rate sampled uniformly between 0.5 and 1
- **Sensitivity**: 该设置直接影响 MaskGIT 式 next frame token prediction；论文未给单独消融。
- **Source**: Sec 2.1 Dynamics Model

## 推理采样配置
- **Value**: 每帧采样使用 25 MaskGIT steps，temperature 2，random sampling
- **Rationale**: 论文在 Training Details 中给出 inference time 的采样流程。
- **Search range**: 主 Genie 使用 temperature 2；CoinRun case study 的 dynamics sampling temperature 为 1.0，maskgit_steps 为 25
- **Sensitivity**: 这是推理期配置，不是训练目标；会影响生成轨迹的采样行为。
- **Source**: Sec 3 Training Details；Appendix F.3 Table 17

## 行为克隆配置
- **Value**: BC policy 使用 sequence length 4，batch size 16；oracle 与 Genie LAM 均用 cross-entropy loss 训练；评估在 5 seeds 上平均
- **Rationale**: 论文用 frozen Genie LAM 标注 unseen videos，再训练 policy 预测 latent action。
- **Search range**: 使用少量 expert labels 做 latent-to-real action mapping；主文提到 as few as 200 expert samples
- **Sensitivity**: latent-to-real mapping 的 expert labels 数量影响适配；oracle agent 在 inference 时随机采样 actions 10% 表现更好。
- **Source**: Sec 3.3；Appendix E.1；Appendix E.2；Figure 15；Table 13
