## 总体范式
- **Value**: unified video-action world model
- **Rationale**: 在同一 shared latent generative process 中联合生成未来视频 latent 与轨迹 token，避免分阶段视频预测和动作生成之间的不匹配。
- **Search range**: 对比对象包括 cascaded 或 loosely coupled world-model-based planning。
- **Sensitivity**: 高；论文多处将闭环性能和零样本泛化归因于统一 video-action formulation。
- **Source**: Abstract; Sec 4.1; Sec 6

## 解码器
- **Value**: single DiT decoder
- **Rationale**: 用统一 DiT 同时预测 future video latents 和 action tokens，使两种模态在共享 latent space 中交互。
- **Search range**: Appendix E 对比 Bidirectional 与 Causal Mask。
- **Sensitivity**: 高；限制 future video tokens 访问 future action tokens 会削弱耦合并降低规划指标。
- **Source**: Sec 1; Fig. 2; Appendix E; Table 10

## 文本编码器
- **Value**: frozen text encoder from Wan2.2-TI2V-5B
- **Rationale**: 将 language instruction 和 high-level command 编码为固定长度 token，并通过 cross-attention 注入 backbone。
- **Search range**: 论文未报告解冻文本编码器或替代文本编码器。
- **Sensitivity**: 论文未给出文本编码器消融。
- **Source**: Sec 4.2

## 视频编码器
- **Value**: 3D-causal VAE encoder from Wan2.2-TI2V-5B
- **Rationale**: 将视频 clip 编码为时间下采样 latent sequence，并支持基于历史观测的 video continuation。
- **Search range**: 论文未报告替代 VAE。
- **Sensitivity**: 论文未给出 VAE 消融；其 causality 被用于单帧与历史缓冲条件。
- **Source**: Sec 4.2

## 条件信号
- **Value**: history latents, current ego state, text/command tokens
- **Rationale**: 模型在每个 timestep l 以历史视觉、当前 ego velocity components 和指令条件联合预测未来视频与动作。
- **Search range**: ego state 表示为 $v _ { x }$ and $v _ { y }$；文本为 command tokens。
- **Sensitivity**: 论文未分别消融各条件；整体设计用于匹配训练和推理。
- **Source**: Sec 4.1; Sec 4.3; Fig. 2

## 动作表示
- **Value**: each action is a 3-D vector encoding ego-vehicle $( x , y )$ position and yaw angle
- **Rationale**: 把未来 action chunk token 化后与视频 latent 一起生成，使轨迹成为同一 rollout 的 action grounding。
- **Search range**: 动作 chunk 长度记为 K；Table 6 说明 trajectory horizon fixed to K=8 (4s)。
- **Sensitivity**: 论文未给出动作维度消融。
- **Source**: Sec 4.1; Sec 4.3; Sec 5.7

## 生成目标
- **Value**: future video latents + future action tokens
- **Rationale**: 目标块在 flow matching 中作为联合生成对象，条件块保持固定。
- **Search range**: Action Only 变体只预测动作；Default 同时预测未来视频与动作。
- **Sensitivity**: 很高；Action Only 被论文描述为显著退化，说明联合预测是核心。
- **Source**: Sec 4.3; Appendix E; Table 10

## 交互掩码
- **Value**: Bidirectional interaction
- **Rationale**: self-attention 使 future video latents 与 action tokens 在 denoising 中相互作为条件。
- **Search range**: Causal Mask 只允许 future action tokens attend to future video tokens；Bidirectional 为默认。
- **Sensitivity**: 高；Causal Mask 使规划指标下降，表明视频不是被动上下文。
- **Source**: Appendix B; Appendix E; Table 10

## 长时域机制
- **Value**: progressive video continuation with sliding history buffer
- **Rationale**: 递归 rollout future video clips，同时更新预测轨迹，用短窗口续写维持 long-horizon temporal coherence。
- **Search range**: 消融包含有无 Video Continuation。
- **Sensitivity**: 高；移除 Video Continuation 会降低 long-horizon consistency 和闭环表现。
- **Source**: Sec 4.1; Fig. 2; Sec 5.7; Table 5

## 推理采样步数
- **Value**: 2 sampling steps for flow-based sampling
- **Rationale**: 论文称很少步数即可支持高效 recurrent decision making。
- **Search range**: Table 8 比较 1、2、3 steps。
- **Sensitivity**: 高；1 step 失败明显，2 steps 达到近最优，3 steps 没有进一步收益。
- **Source**: Sec 5.2; Sec 5.7; Table 8
