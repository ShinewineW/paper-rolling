# Heuristics

## H1: 固定条件块与生成目标块分离:历史视频 latent、ego state 与文本作为 condition block,未来视频 latent 和 action tokens 作为 target block。
- **Rationale**: 论文强调 condition block 在训练和推理都保持 fixed,从而匹配训练/推理形式,让短窗口 continuation 可递归串联。
- **Sensitivity**: 若条件与目标混杂或训练/推理窗口不一致,长时域 rollout 容易失去一致性。
- **Bounds**: 条件来自固定长度 history buffer；目标包含未来 latent steps 和 K 个 future action tokens。
- **Code ref**: [X_cond / Y_target / condition_block / target_block]
- **Source**: Sec. 4.3 Fixed Condition and Generative Targets

## H2: 用 frozen text encoder 编码 language instruction,并通过 cross-attention 注入 backbone,不直接拼接到视觉/动作 token 流。
- **Rationale**: 论文说明这样保持 spatiotemporal token sequence compact,并 decouple text length 以提高控制灵活性。
- **Sensitivity**: 若把文本直接拼接进主 token 序列,token 长度与控制上下文耦合会增加序列负担。
- **Bounds**: 文本 token 来自 Wan2.2-TI2V-5B 的 frozen text encoder。
- **Code ref**: [text_encoder / cross_attention / text_tokens]
- **Source**: Sec. 4.2 Text Instruction Encoding

## H3: 历史观测 buffer 用 3D-causal VAE 编码为 history latents,推理时只编码历史观测并生成未来 latents。
- **Rationale**: 论文利用 WAN 的 causal VAE 使单帧/历史帧可作为合法条件 latent,并把单帧条件扩展为 video-continuation 条件以增强长时域一致性。
- **Sensitivity**: 历史 buffer 太短会削弱 long-range visual priors；训练和推理条件不匹配会影响 continuation。
- **Bounds**: 训练样本使用 4 history frames 和 8 future frames at 2 FPS。
- **Code ref**: [video_vae / history_latents / future_latents]
- **Source**: Sec. 4.2 Video Causal VAE with Wan2.2-TI2V-5B and Sec. 5.2 Training Details

## H4: 默认使用视频与动作 token 的 bidirectional interaction,不采用只让 action 看 video 的 causal mask。
- **Rationale**: 附录消融说明 causal mask 限制 future video tokens 访问 future action tokens 会削弱场景演化与 ego behavior 的耦合。
- **Sensitivity**: causal mask 会使 video prediction 退化为被动上下文,降低 video-trajectory consistency。
- **Bounds**: future action tokens 可以 attend future video tokens,默认还允许 future video tokens attend future action tokens。
- **Code ref**: [bidirectional_attention / causal_mask]
- **Source**: Appendix E Causal Masking Strategy

## H5: 推理阶段采用少量 flow sampling steps,正文训练细节指定使用 2 sampling steps。
- **Rationale**: 论文消融指出 2 steps 已达到近最优闭环表现,用于高效 recurrent decision making。
- **Sensitivity**: 单步采样在消融中失败明显；继续增加 step 没有带来收益。
- **Bounds**: 推理使用 2 sampling steps for flow-based sampling。
- **Code ref**: [num_sampling_steps / flow_sample]
- **Source**: Sec. 5.2 Training Details and Sec. 5.7 Sampling steps

## H6: future video rollout 长度与 action chunk 对齐,论文默认用 8 future frames 对应 K=8 的 action horizon。
- **Rationale**: 消融解释短 rollout 会 under-cover trajectory,长 rollout 会积累 drift,都会削弱 video grounding。
- **Sensitivity**: 未来帧过短或过长都会破坏视频-轨迹一致性。
- **Bounds**: 训练细节为 8 future frames at 2 FPS；消融中 trajectory horizon fixed to K=8。
- **Code ref**: [future_frames / action_horizon_K]
- **Source**: Sec. 5.2 Training Details and Sec. 5.7 Prediction time horizon
