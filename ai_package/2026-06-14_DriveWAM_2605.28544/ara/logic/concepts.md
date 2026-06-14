# Concepts

## DriveWAM
- **Notation**: 以 pretrained flow-matching video diffusion transformer T _ { \omega } 为核心，围绕历史 H _ { k }、ego state e _ { k }、guidance g _ { k } 预测下一块 video-action chunk。
- **Definition**: DriveWAM 是一种面向自动驾驶的 semantically guided world-action model，把 pretrained video foundation model 改造成统一的未来世界演化与 ego-action 生成骨干，并由 frozen VLM 提供 scene-evolving driving semantics。
- **Boundary conditions**: 它不是 VLM-centric policy，也不是把视觉生成作为辅助分支的独立 planner；论文强调其 policy core 是 pretrained video generative backbone。
- **Related concepts**: ['autoregressive video-action generation', 'world-action flow', 'scene-evolving driving guidance', 'selective KV memory', 'joint flow-matching objective']

## autoregressive video-action generation
- **Notation**: 目标 chunk 为 ( x _ { k + 1 } , a _ { k + 1 } )；可用条件包括 H _ { k }、e _ { k }、g _ { k }。
- **Definition**: 把驾驶片段划分为连续 chunks，并把任务表述为在第 k 个决策步基于已观测历史生成下一段视频和对应 ego action。
- **Boundary conditions**: 它只使用 causally available context；目标 chunk 的观测不能泄漏到当前 guidance 或历史条件中。
- **Related concepts**: ['DriveWAM', 'unified temporal token sequence', 'world-action flow', 'full-clip training', 'autoregressive rollout']

## unified temporal token sequence
- **Notation**: $$z _ { k } = \mathrm { V A E } ( x _ { k } ) , \qquad u _ { k } = E _ { a } ( a _ { k } ) , \qquad H _ { k } = \{ ( z _ { i } , u _ { i } ) \} _ { i \leq k } .\tag{1}$$
- **Definition**: 用于联合建模视频与动作的时间 token 表示；视频 chunk 由 pretrained VAE 编码，ego-action chunk 由 MLP action encoder 嵌入，并按时间顺序组织。
- **Boundary conditions**: 动作表示限于论文所述 normalized ego-frame translation and yaw increments；视频 latent 仍来自 pretrained VAE，并非离散 VQ token。
- **Related concepts**: ['autoregressive video-action generation', 'H _ { k }', 'VAE', 'E _ { a }', 'selective KV memory']

## world-action flow
- **Notation**: 视频分支：$$\hat { v } _ { k + 1 , \tau } ^ { z } = T _ { \omega } ( z _ { k + 1 , \tau } ; H _ { k } , e _ { k } , g _ { k } , \tau ) .\tag{2}$$ 动作分支：$$\hat { v } _ { k + 1 , \tau } ^ { a } = D _ { a } ( T _ { \omega } ( u _ { k + 1 , \tau } ; \tilde { z } _ { k + 1 } , H _ { k } , e _ { k } , g _ { k } , \tau ) ) ,\tag{3}$$
- **Definition**: DriveWAM 将驾驶任务分解为 future world modeling 和 inverse-dynamics action generation，并使用同一个 pretrained flow-matching video diffusion transformer 预测未来视频 latent 与动作 velocity。
- **Boundary conditions**: 训练时 \tilde { z } _ { k + 1 } 是 clean future video latent；推理时是 generated latent。该差异由 noisy-history augmentation 缓解。
- **Related concepts**: ['future world modeling', 'inverse-dynamics action generation', 'joint flow-matching objective', 'T _ { \\omega }', 'D _ { a }']

## joint flow-matching objective
- **Notation**: $$\begin{array} { r } { \mathcal { L } = \mathbb { E } _ { k , \tau } \left[ \left. \hat { v } _ { k + 1 , \tau } ^ { z } - v _ { k + 1 , \tau } ^ { z } \right. _ { 2 } ^ { 2 } + \beta _ { a } \left. \hat { v } _ { k + 1 , \tau } ^ { a } - v _ { k + 1 , \tau } ^ { a } \right. _ { 2 } ^ { 2 } \right] , } \end{array}\tag{4}$$
- **Definition**: 同时训练视频分支和动作分支的 flow-matching 目标，用视频项保留 pretrained spatio-temporal generative prior，用动作项学习把该 prior 解码为 ego motion。
- **Boundary conditions**: 论文给出的训练目标只包含视频 velocity 误差与动作 velocity 误差；selective KV memory 的 retention score 属于推理期机制，不属于训练目标。
- **Related concepts**: ['world-action flow', 'future world modeling', 'action generation', '\\beta _ { a }']

## scene-evolving driving guidance
- **Notation**: $$g _ { k } = \Phi _ { \mathrm { V L M } } ( x _ { k } , a _ { k } , c _ { k } ) ,\tag{5}$$
- **Definition**: 由 frozen VLM 在每个决策步基于最新因果可用上下文生成 chunk-specific semantic intent，用于指导下一段 video-action generation。
- **Boundary conditions**: VLM 只接收 latest observation、recent ego trajectory 与 route command；不使用 target chunk 观测，因此不引入未来信息泄漏。
- **Related concepts**: ['Qwen3-VL-8B', 'temporally localized cross-attention', 'route command', 'g _ { k }', 'DriveWAM']

## temporally localized guidance injection
- **Notation**: chunk k + i 的 video-action tokens 只能 attend 到 g _ { k } 的 guidance tokens。
- **Definition**: 为每个决策步的 guidance 引入 block-diagonal text mask，使目标 chunk 的 video-action tokens 只能关注对应的 guidance tokens。
- **Boundary conditions**: 它约束的是 text guidance 的跨 chunk 可见性；不是改变视频与动作 token 的基本因果 teacher-forcing 结构。
- **Related concepts**: ['scene-evolving driving guidance', 'block-diagonal text mask', 'causal consistency', 'cross-attention']

## selective KV memory
- **Notation**: 相关性与冗余：$$\rho _ { j } ^ { m } = \frac { 1 } { \left| Q _ { k } ^ { m } \right| } \sum _ { \mathbf { q } \in Q _ { k } ^ { m } } \left[ \mathrm { s o f t m a x } _ { \ell \in H _ { k } ^ { m } } \left( \frac { \mathbf { q } ^ { \top } \mathbf { k } _ { \ell } ^ { m } } { \sqrt { d } } \right) \right] _ { j } , \qquad \eta _ { j } ^ { m } = \mathrm { m e a n } _ { \ell \neq j } \cos ( \mathbf { k } _ { j } ^ { m } , \mathbf { k } _ { \ell } ^ { m } ) ,\tag{6}$$ 保留分数：$$s _ { j } ^ { m } = \lambda \rho _ { j } ^ { m } - ( 1 - \lambda ) \eta _ { j } ^ { m } ,\tag{7}$$
- **Definition**: 一种仅在推理期使用的 training-free memory 机制，为长时域 autoregressive rollout 维护有界的 video 与 action KV memory pools，并通过 relevance-redundancy 规则选择保留 token。
- **Boundary conditions**: 该机制不改变训练 objective 或模型参数；它替代的是推理时 full KV cache 或 FIFO sliding-window cache 的历史保留策略。
- **Related concepts**: ['modality-aware memory pools', 'H _ { k } ^ { v }', 'H _ { k } ^ { a }', 'FlowCache', 'autoregressive rollout']

## modality-aware memory pools
- **Notation**: H _ { k } 被分解为 H _ { k } ^ { v } 与 H _ { k } ^ { a }，并满足 | H _ { k } ^ { v } | \le B ^ { v }、| H _ { k } ^ { a } | \le B ^ { a }。
- **Definition**: selective KV memory 将历史拆成 video memory pool 与 action memory pool，分别保留场景上下文与 ego-motion history，避免单一全局 cache 被视频 token 主导。
- **Boundary conditions**: 它不是单一 global cache；选择与驱逐在每个 modality pool 内进行。
- **Related concepts**: ['selective KV memory', 'video tokens', 'action tokens', 'B ^ { v }', 'B ^ { a }']

## route command
- **Notation**: command 集合为 {straight, left, right}；由 R _ { 0 } ^ { \top } R _ { 1 } 的相对 yaw 派生。
- **Definition**: 用于 scene-evolving guidance 的高层方向性意图，论文在附录中从每个 upcoming chunk 的 ego-yaw change 构造 coarse command。
- **Boundary conditions**: 该 command 只表达 directional intent，不包含 future positions、velocities、distances 或 trajectory coordinates。
- **Related concepts**: ['scene-evolving driving guidance', 'Qwen3-VL-8B', 'g _ { k }', 'causal guidance generation']
