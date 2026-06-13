# Concepts

## DriveVA
- **Notation**: 以条件 \(\mathbf { C } _ { l } : = ( \mathcal { O } _ { l } , \mathcal { T } , \mathbf { q } _ { l } )\) 为输入，联合建模 \(\mathcal { F } _ { l + 1 : l + N }\) 与 \(\mathcal { A } _ { l + 1 : l + K }\)。
- **Definition**: DriveVA 是面向自动驾驶的统一视频-动作世界模型，在同一潜在生成过程中联合预测未来视觉想象与未来动作序列。它基于预训练视频生成模型的时空先验，并把规划动作作为同一 rollout 的动作 grounding。
- **Boundary conditions**: DriveVA 不是只做视觉预测的世界模型，也不是只输出轨迹的 VLA；论文强调其区别在于联合解码未来视频 latents 与 action tokens。
- **Related concepts**: ['共享潜在生成过程', '视频-轨迹一致性', 'DiT decoder', 'IDM-style action grounding', 'video continuation']

## 共享潜在生成过程
- **Notation**: 生成目标块记作 \(\mathbf { Y } _ { 0 } ^ { ( l ) }\)，条件块记作 \(\mathbf { X } _ { \mathrm { c o n d } } ^ { ( l ) }\)。
- **Definition**: 共享潜在生成过程指未来视频 latents 与 action tokens 被放入同一个生成目标块中，由统一模型在共享 latent space 内一起去噪和解码。
- **Boundary conditions**: 不要把它理解为两个独立模型之间的特征传递；论文明确说 future video latents 与 action tokens 不是 cascaded manner 解码。
- **Related concepts**: ['DriveVA', 'DiT decoder', 'action tokens', 'future video latents', 'flow matching']

## 视频-轨迹一致性
- **Notation**: 论文用 DPVO 从 ground-truth future videos 与 generated future videos 重建 camera trajectories，并与对应参考轨迹做对齐后比较。
- **Definition**: 视频-轨迹一致性表示模型预测的未来轨迹应与生成视频中隐含的自车运动和场景演化相匹配。
- **Boundary conditions**: 它不是单纯的视频清晰度指标，也不是只比较轨迹与 ground truth；论文还关注 predicted video reconstruction 与 Pred Future 之间的几何一致。
- **Related concepts**: ['DriveVA', 'DPVO reconstruction', 'shared latent generative process', 'IDM-style action grounding']

## action chunk
- **Notation**: \(\mathscr { A } _ { l + 1 : l + K }\)，其中每个 \(\mathbf { a } _ { l + i }\) 编码 ego-vehicle 的位置与 yaw angle。
- **Definition**: action chunk 是在当前 timestep 预测的一段未来动作序列，用于按顺序执行车辆后续运动。
- **Boundary conditions**: 它不是单步控制命令；论文把它描述为 K future actions to be executed sequentially。
- **Related concepts**: ['action tokens', 'IDM-style action grounding', 'rolling-horizon setup', 'future video clip']

## future video clip
- **Notation**: \(\mathcal { F } _ { l + 1 : l + N } = \{ F _ { l + j } \} _ { j = 1 } ^ { N }\)。实践中预测的是 latent representations，而不是直接预测 raw frames。
- **Definition**: future video clip 是模型预测的未来视觉演化片段，用来表示执行未来动作后可能看到的场景变化。
- **Boundary conditions**: 不要把它等同于最终像素级视频输出；论文方法部分说明实际预测的是未来帧的 latent representations。
- **Related concepts**: ['future video latents', 'video continuation', 'action chunk', 'Video Causal VAE']

## video continuation
- **Notation**: 历史观测缓冲为 \(\mathcal { O } _ { l } = \{ \mathbf { F } _ { l - m + 1 } , \ldots , \mathbf { F } _ { l } \}\)，执行 \(\mathscr { A } _ { l + 1 : l + K }\) 后用滑动窗口更新。
- **Definition**: video continuation 是把长期 rollout 分解为连续短片段生成的策略，通过历史观测条件递归生成未来视频片段并更新轨迹。
- **Boundary conditions**: 它不是只依赖当前单帧的条件生成；论文强调扩展到 history observation buffer。
- **Related concepts**: ['rolling-horizon setup', 'future video clip', 'Video Causal VAE', 'DriveVA']

## DiT decoder
- **Notation**: 给定 \(\mathbf { X } _ { \mathrm { c o n d } } ^ { ( l ) }\) 与 text tokens \(T\)，\(f _ { \theta }\) 预测 generative targets 的 conditional velocity field。
- **Definition**: DiT decoder 是 DriveVA 用来联合预测未来视频 latents 与 action tokens 的统一 Diffusion Transformer 解码器。
- **Boundary conditions**: 它不是只服务于视频生成的解码器，也不是独立的下游 planner。
- **Related concepts**: ['shared latent generative process', 'flow matching', 'future video latents', 'action tokens']

## IDM-style action grounding
- **Notation**: \(\pi _ { \theta } ( \mathcal { F } _ { l + 1 : l + N } , \mathcal { A } _ { l + 1 : l + K } \mid \mathbf { C } _ { l } ) = \pi _ { \theta } ( \mathcal { F } _ { l + 1 : l + N } \mid \mathbf { C } _ { l } ) \pi _ { \theta } ( \mathcal { A } _ { l + 1 : l + K } \mid \mathbf { C } _ { l } , \mathcal { F } _ { l + 1 : l + N } )\)。
- **Definition**: IDM-style action grounding 指在给定未来视觉演化和相同条件上下文时，预测与该想象未来最兼容的 action chunk。
- **Boundary conditions**: 不要把该概念误解为单独训练的 inverse dynamics model；论文明确说 DriveVA 优化单一端到端模型。
- **Related concepts**: ['DriveVA', 'future video clip', 'action chunk', 'video-trajectory consistency']

## flow matching
- **Notation**: \(\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { s , \epsilon , x _ { \mathrm { d a t a } } } \left[ \left\| v _ { \boldsymbol { \theta } } \left( \boldsymbol { x } ^ { ( s ) } , { s } \right) - \dot { \boldsymbol { x } } ^ { ( s ) } \right\| _ { 2 } ^ { 2 } \right]\)。
- **Definition**: flow matching 是论文用于生成建模的训练框架，把噪声样本连续变换到目标数据分布，并训练模型回归速度场。
- **Boundary conditions**: 该概念来自论文 Preliminary；不要把它替换成论文未给出的其他扩散损失或自行构造的训练目标。
- **Related concepts**: ['DiT decoder', 'shared latent generative process', 'conditional flow matching']

## zero-shot transfer
- **Notation**: 论文描述为 trained on NAVSIM and evaluated on nuScenes 或 Bench2Drive without any fine-tuning。
- **Definition**: zero-shot transfer 指模型在一个数据域训练后，不对目标数据集 fine-tuning，直接在 unseen datasets 或 cross domain 场景中评估。
- **Boundary conditions**: 它不是目标域 fine-tuning 后的性能比较；论文在 Table 2 中强调 all methods are trained on NAVSIM and directly evaluated on target datasets。
- **Related concepts**: ['DriveVA', 'cross-domain generalization', 'video-trajectory consistency', 'NAVSIM', 'nuScenes', 'Bench2Drive']
