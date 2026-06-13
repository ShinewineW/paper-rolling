## Reasoner 预训练目标
- **Value**: next-token prediction，训练两个 epoch，最大序列 16k tokens，单样本限制为 2048 image tokens 与 8192 video tokens
- **Rationale**: Reasoner 先在大规模多模态语料上学习视觉理解与推理能力，并用序列长度限制服务低延迟 Physical AI 推理需求。
- **Search range**: 预训练阶段使用完整预训练混合数据；序列上限为 16k tokens。
- **Sensitivity**: 高；序列长度、长短样本损失权重和图像视频 token 限制会影响下游理解稳定性。
- **Source**: Sec 4.1.1

## Reasoner 预训练优化器
- **Value**: AdamW；LM 与 projector 峰值学习率 5e-5，ViT 峰值学习率 5e-6；10% linear warm-up 后 cosine decay 到 0.1×；betas 为 0.9 与 0.999；weight decay 0.05；global grad clip 1.0
- **Rationale**: 不同模块使用不同学习率，以保护 ViT 表征并稳定语言模型与投影层训练。
- **Search range**: 适用于 Reasoner pre-training。
- **Sensitivity**: 高；ViT 学习率、warm-up、weight decay 与梯度裁剪直接影响多模态对齐和稳定性。
- **Source**: Sec 4.1.1

## Reasoner SFT 采样与训练步数
- **Value**: importance-aware sampling；8200 iterations；global batch size 512
- **Rationale**: SFT 阶段按重要性、质量和规模分配固定采样预算，使优化集中在高价值 Physical AI 下游任务，同时保持能力覆盖。
- **Search range**: 适用于 curated high-quality multimodal mixture。
- **Sensitivity**: 中高；采样预算会改变任务域权重，可能影响 robotics、AV 与 smart infrastructure 的均衡。
- **Source**: Sec 4.1.2

## Reasoner SFT 优化器
- **Value**: AdamW；LM 与 projector 峰值学习率 1e-5，ViT 峰值学习率 1e-6；1000 steps linear warm-up 后 cosine decay 到 0.1×；betas 为 0.9 与 0.95；weight decay 0.1；global grad clip 1.0
- **Rationale**: SFT 使用更小学习率和更严格质量数据，适配下游任务同时降低遗忘风险。
- **Search range**: 适用于 Reasoner supervised fine-tuning。
- **Sensitivity**: 高；SFT 学习率和采样策略会影响下游任务适配与原有能力保持。
- **Source**: Sec 4.1.2

## Generator 训练目标
- **Value**: rectified flow matching；noisy latent 由 clean target 与 Gaussian noise 直线插值得到；denoiser 预测 constant velocity；条件 token 从 loss 中 gate out
- **Rationale**: 统一图像、视频、音频和 action 的生成训练目标，使不同模态共享扩散式去噪接口。
- **Search range**: 跨 images、videos、audio、action；每模态独立采样 noise level。
- **Sensitivity**: 高；噪声分布、shift reparameterization 和条件 token masking 会直接影响生成质量和条件一致性。
- **Source**: Sec 4.2

## Generator 预训练分辨率与上下文
- **Value**: 同时训练 256p、480p、720p；五种 aspect ratios；视频帧数 5-400 或 5-300；固定 74,000-token sequence packing；image-only、video-256p、video-480p、video-720p 比例为 1:1:2:1
- **Rationale**: 多分辨率和 token packing 在高保真、样本多样性和 GPU 利用率之间取得平衡。
- **Search range**: 256p 与 480p 最多 400 frames；720p 最多 300 frames；FPS 10-30。
- **Sensitivity**: 高；720p 帧数受上下文限制，分辨率混合会影响清晰度、动态和吞吐。
- **Source**: Sec 4.2.1, Table 5

## Generator 预训练任务比例
- **Value**: Text-to-Image 20%，Text-to-Video 56%，Image-to-Video 16%，Video-to-Video 8%；视频 batch 中 T2V、I2V、V2V 使用 clean-prefix/noisy-target 形式
- **Rationale**: 任务比例把主要容量投向文本到视频，同时保留图像生成、首帧条件生成和视频续写能力。
- **Search range**: 四种 generation modes 使用同一 structured JSON caption format。
- **Sensitivity**: 中高；比例变化会影响 T2V 主能力和条件视频任务之间的平衡。
- **Source**: Sec 4.2.1

## Generator 预训练优化器
- **Value**: 仅更新 generation-specific parameters；reasoner tower frozen；FusedAdamW；learning rate 1e-4；betas 为 0.9 与 0.99；weight decay 0.05；grad clip norm 1.0；text-dropout rate 10%
- **Rationale**: 冻结 reasoner 保留理解能力，生成塔学习视觉、音频和 action 去噪；text dropout 支持 classifier-free guidance。
- **Search range**: 适用于 generator pre-training。
- **Sensitivity**: 高；冻结策略和 text dropout 会影响语言条件保持与 CFG 效果。
- **Source**: Sec 4.2.1

## Generator 中训练混合
- **Value**: Image 10%，Video 32%，Video + Audio 8%，Action 25%，General Transfer 20%，Driving Transfer 5%
- **Rationale**: 中训练在保留视觉生成能力的同时加入 action 与 transfer，使模型获得 Physical AI 控制和因果接口。
- **Search range**: Action 包含 forward dynamics、inverse dynamics、policy；transfer 包含 edge、blur、depth、segmentation 与 world-scenario-map controls。
- **Sensitivity**: 高；action 与 transfer 比例决定模型对控制、动作和视频保真的权衡。
- **Source**: Sec 4.2.2, Table 6

## Generator 中训练优化与 loss scale
- **Value**: FusedAdamW；learning rate 1e-4；weight decay 0.05；grad clip norm 1.0；loss scale 10；LambdaLinear schedule start factor 0.4，cycle length 100,000；action losses scaled by 10×
- **Rationale**: action 向量归一化后 per-element MSE 较小，因此提高 action loss 权重以避免被视觉 loss 淹没。
- **Search range**: 适用于 mid-training 的多模态 velocity MSE。
- **Sensitivity**: 高；action loss scale 和采样比例会影响 policy、FD、ID 与视觉质量之间的冲突。
- **Source**: Sec 4.2.2

## Text-to-Image post-training
- **Value**: Cosmos3-Super-Text2Image 两阶段 SFT：Stage 1 为 20k steps，45% general real image，40% synthetic image，15% text-rendering-only，base learning rate 1e-4，2k warmup；Stage 2 为 2k steps，470k ultra-high-quality image-caption pairs；context window 70k tokens；训练图像分辨率高于 720p
- **Rationale**: 先做广泛 T2I 专门化，再用高质量图文对做审美、文本渲染和偏好对齐细化。
- **Search range**: 仅用于 Cosmos3-Super-Text2Image。
- **Sensitivity**: 中高；高质量小数据和文本渲染比例会影响语义对齐、文字生成和过拟合风险。
- **Source**: Sec 4.2.3

## Image-to-Video post-training
- **Value**: Cosmos3-Super-Image2Video 训练 10k iterations，learning rate 1e-5，约 50B tokens；目标 480p，189 frames，约 8 seconds at 24fps；混合包含 1,000 manually curated videos、约 20k synthetic video clips，且 20% T2I image tokens 保留语义对齐
- **Rationale**: I2V 专门化强调物理规律、物体恒常性和场景几何，同时用 T2I token 抑制语义对齐退化。
- **Search range**: 仅用于 Cosmos3-Super-Image2Video。
- **Sensitivity**: 中高；目标时长、分辨率和 T2I 保留比例会影响速度、物理一致性和语义保持。
- **Source**: Sec 4.2.4

## Robot policy post-training
- **Value**: Cosmos3-Nano-Policy-DROID 从 mid-trained Cosmos3-Nano resume；fresh action encoder、action-decoding MLP、action embedding tokens；action-related parameters 使用 5× learning-rate multiplier；learning rate 2e-4；预测 32 future absolute joint-position actions，15Hz；输入为 proprioceptive state 与三视角视觉 canvas 540×640
- **Rationale**: 策略后训练把通用 omnimodal generator 适配为可执行闭环 robot policy，并用动作相关参数更快适配 DROID 接口。
- **Search range**: DROID platform 与 dataset；推理使用 4 diffusion steps、shift 5、guidance scale 3。
- **Sensitivity**: 高；动作编码初始化、学习率倍增和低步数采样直接影响闭环延迟与成功率。
- **Source**: Sec 4.2.5
