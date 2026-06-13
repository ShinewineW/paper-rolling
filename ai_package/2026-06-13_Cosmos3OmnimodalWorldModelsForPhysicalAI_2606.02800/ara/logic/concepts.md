# Concepts

## Cosmos 3
- **Notation**: 输入与输出被组织为统一多模态 token 序列，包含 AR subsequence 与 DM subsequence。
- **Definition**: Cosmos 3 是一组面向 Physical AI 的 omnimodal world models，联合建模 language、image、video、audio 和 action，并同时覆盖 understanding 与 generation。
- **Boundary conditions**: 论文强调的是同一架构可通过不同 input-output configuration 切换任务；不同后训练变体仍共享对应 mid-trained 模型的架构，不代表所有任务都用同一个权重完成。
- **Related concepts**: ['omnimodal world model', 'Physical AI', 'Mixture-of-Transformers', 'AR subsequence', 'DM subsequence', 'action token']

## omnimodal world model
- **Notation**: 模态集合可概括为 {language, vision, audio, action}，其中 vision 包含 image 与 video。
- **Definition**: omnimodal world model 指能够在统一框架内处理并生成 language、image、video、audio 和 action 序列的 world model。
- **Boundary conditions**: 该概念不等同于任意多模态模型；在本文语境中必须同时服务 Physical AI 的 perception、simulation 和 execution。
- **Related concepts**: ['Cosmos 3', 'Physical AI', 'understanding', 'generation', 'unified representation space']

## Physical AI
- **Notation**: 核心能力被表述为 understanding 与 generation 两个耦合支柱。
- **Definition**: Physical AI agents 感知、推理并采取行动来与真实世界交互；论文认为其训练需要安全、可扩展的 simulated worlds 来缓解真实世界训练慢、昂贵且可能危险的问题。
- **Boundary conditions**: 本文讨论的 Physical AI 不限于机器人，还包含 autonomous vehicles、camera motion、egocentric human motion 和 smart infrastructure 等数据域。
- **Related concepts**: ['Cosmos 3', 'understanding', 'generation', 'world model', 'action token']

## understanding
- **Notation**: 在 Cosmos 3 中主要由 AR subsequence 与 reasoner tower 承担。
- **Definition**: understanding 是从部分观测中推断 latent representations、semantics 和 dynamics 的能力。
- **Boundary conditions**: 本文中的 understanding 不只是静态图像问答，还包括 spatial grounding、temporal reasoning、action understanding 和 Physical AI 领域的监督微调能力。
- **Related concepts**: ['generation', 'AR subsequence', 'reasoner tower', 'Physical AI', 'VLM']

## generation
- **Notation**: 在 Cosmos 3 中非语言模态主要通过 DM subsequence 的 iterative denoising 生成，语言通过 next-token prediction 生成。
- **Definition**: generation 是预测并模拟 plausible futures 的能力，使 agent 能预期世界如何演化以及应如何响应。
- **Boundary conditions**: generation 的具体行为由 token arrangement 和 generation mode 决定；推理期语言生成与非语言模态生成机制不同。
- **Related concepts**: ['understanding', 'DM subsequence', 'generator tower', 'video generation', 'world-action model']

## action token
- **Notation**: 给定连续 video tokens，$a _ { t }$ 表示从前一状态 $v _ { t - 1 }$ 到当前状态 $v _ { t }$ 的 transition。
- **Definition**: action token 是 Cosmos 3 为 action 引入的专用 token 类别，用来连接 physical world、language-based reasoning 和 video-based world modeling，并关联到真实交互中的控制信号。
- **Boundary conditions**: 论文把 actions 定义为诱发 world state 变化的 causal variables；具体控制空间不会直接保留 PID 参数或低层执行接口，而是映射到统一动作接口。
- **Related concepts**: ['unified action representation', 'action tokenization', 'forward dynamics', 'inverse dynamics', 'policy mode', 'DM subsequence']

## unified action representation
- **Notation**: motion 使用相对位姿 $\Delta \mathbf { T } _ { t } = \mathbf { T } _ { t - 1 } ^ { - 1 } \mathbf { T } _ { t }$；action components 可包括 ego poses、effector poses 和 grasp states。
- **Definition**: unified action representation 将不同 embodiment 的控制信号映射为由共享几何组件构成的紧凑 action vectors，以支持跨域一致的多模态推理、生成和 policy learning。
- **Boundary conditions**: 不同数据域包含的组件不同：cameras 和 autonomous vehicles 仅用 ego poses；egocentric data 包含 head-camera pose deltas、wrist-pose deltas 和 fingertip positions；robotic data 包含 head-camera pose deltas、end-effector flange-pose deltas 和 continuous gripper open/close values。
- **Related concepts**: ['action token', 'action tokenization', 'domain-aware projection', 'Physical AI']

## action tokenization
- **Notation**: $$\mathbf { z } = \mathbf { W } _ { \mathrm { i n } } ^ { ( k ) } \mathbf { x } + \mathbf { b } _ { \mathrm { i n } } ^ { ( k ) }\tag{1}$$；$$\mathbf { x } = \mathbf { W } _ { \mathrm { o u t } } ^ { ( k ) } \mathbf { z } + \mathbf { b } _ { \mathrm { o u t } } ^ { ( k ) }\tag{2}$$
- **Definition**: action tokenization 使用 domain-aware input and output projection layers，把不同长度和结构的 native action vectors 映射到共享 latent action space，并能解码回原始动作空间。
- **Boundary conditions**: projection parameters 从头初始化并与 MoT backbone 联合优化；这不是把所有领域动作强行改成同一原始维度，而是在 latent token 层共享。
- **Related concepts**: ['action token', 'unified action representation', 'domain-aware projection', 'MoT backbone']

## AR subsequence
- **Notation**: 在多个生成模式中使用共享前缀 $\mathbf { S } _ { \mathrm { A R } } \triangleq [ l _ { 1 } , \ldots , l _ { n } , \langle \mathrm { E O S } \rangle , \langle \mathrm { B O G } \rangle ]$。
- **Definition**: AR subsequence 是输入 token sequence 的前半部分，负责 reasoning 和 understanding，包含 language tokens 以及由 ViT encoder 嵌入的 image 和 video tokens。
- **Boundary conditions**: AR tokens 被路由到 transformer decoder layers 中专门的参数集合；它们不会基于 DM tokens 更新，以保持 causal integrity。
- **Related concepts**: ['DM subsequence', 'reasoner tower', 'Mixture-of-Transformers', 'dual-stream joint attention']

## DM subsequence
- **Notation**: 统一排列规则是 AR tokens 在前；DM 内每个模态 clean conditioning tokens 在 noisy diffusion tokens 前；conditioning 与 diffusion 子段内按 vision、audio、action 排序。
- **Definition**: DM subsequence 跟随 AR subsequence，包含来自 VAE encoder 的 video 和 image tokens，以及 audio 和 action tokens；生成时通过 iterative denoising 得到 clean tokens。
- **Boundary conditions**: DM tokens 使用与 AR tokens 不同的参数集合，但在每个 transformer decoder layer 中仍可通过 joint attention 与 AR tokens 交互。
- **Related concepts**: ['AR subsequence', 'generator tower', 'iterative denoising', 'token arrangement', 'generation mode']

## Mixture-of-Transformers
- **Notation**: AR subsequence 路由到 reasoner tower，DM subsequence 路由到 generator tower；二者在 shared self-attention operator 中交互。
- **Definition**: Mixture-of-Transformers 是 Cosmos 3 的 backbone，处理来自不同模态的统一 token sequence；每个 transformer decoder layer 内有用于 reasoning tasks 的参数集合和用于 generation tasks 的参数集合。
- **Boundary conditions**: 论文指出该设计与其他 unified generation models 有相似 decoder-layer 结构，但差异在 training strategy、positional embeddings 和 overall capabilities。
- **Related concepts**: ['Cosmos 3', 'reasoner tower', 'generator tower', 'dual-stream joint attention', 'AR subsequence', 'DM subsequence']

## dual-stream joint attention
- **Notation**: $$\begin{array} { r } { { \bf O } _ { \mathrm { A R } } = \mathrm { A t t n } _ { \mathrm { c a u s a l } } \big ( { \bf Q } _ { \mathrm { A R } } ,       { \bf K } _ { \mathrm { A R } } , { \bf V } _ { \mathrm { A R } } \big ) . } \end{array}\tag{7}$$；$$\begin{array} { r } { \mathbf { O } _ { \mathrm { D M } } = \mathrm { A t t n } _ { \mathrm { f u l l } } \big ( \mathbf { Q } _ { \mathrm { D M } } , \mathbf { \Theta } [ \mathbf { K } _ { \mathrm { A R } } ; \mathbf { K } _ { \mathrm { D M } } ] , \mathbf { \Theta } [ \mathbf { V } _ { \mathrm { A R } } ; \mathbf { V } _ { \mathrm { D M } } ] \big ) , } \end{array}\tag{8}$$
- **Definition**: dual-stream joint attention 让 AR tokens 保持 causal self-attention，同时让 DM tokens 使用 full bidirectional attention，并以 AR 与 DM tokens 的并集作为 keys 和 values。
- **Boundary conditions**: AR tokens 只 attend AR subsequence 内的先前 token；DM tokens 才能双向 attend AR 与 DM 的组合上下文。
- **Related concepts**: ['Mixture-of-Transformers', 'AR subsequence', 'DM subsequence', 'reasoner tower', 'generator tower']

## multimodal position embedding
- **Notation**: Cosmos 3 采用带 absolute temporal indexing 的 3D MRoPE；language tokens 使用 $t = h = w$，audio 和 action tokens 只使用 temporal coordinates 且 $h = w = 0$。
- **Definition**: multimodal position embedding 为 attention 注入时间与空间结构，使不同模态 token 能按语义和几何相关性对齐。
- **Boundary conditions**: AR subsequence 的位置分配保持与原始 3D MRoPE 兼容；DM subsequence 中 vision segment 的时空索引在 segment 内重置，并不简单等同于全局序列位置。
- **Related concepts**: ['3D MRoPE', 'absolute temporal modulation', 'AR subsequence', 'DM subsequence', 'video token', 'audio token', 'action token']

## absolute temporal modulation
- **Notation**: $$\delta t = \frac { \mathrm { T P S } _ { \mathrm { b a s e } } } { \mathrm { T P S } }.\tag{9}$$
- **Definition**: absolute temporal modulation 使用 TPS 将不同 temporal resolution 的 tokens 对齐到共享物理时间轴，使不同 FPS、audio hop 或 action sampling frequency 的时间步具备可比物理含义。
- **Boundary conditions**: TPS 的定义依赖模态：video tokens 由 frame rate 除以 temporal compression factor，audio tokens 由采样率和 hop size 计算，action tokens 等于 action data 的 sampling frequency。
- **Related concepts**: ['multimodal position embedding', '3D MRoPE', 'video token', 'audio token', 'action token']

## generation mode
- **Notation**: 示例包括 $\mathbf { S } _ { \mathrm { T 2 I } } = [ \mathbf { S } _ { \mathrm { A R } } , \ \tilde { v } _ { 1 } ]$、$\mathbf { S } _ { \mathrm { V 2 V } } = [ \mathbf { S } _ { \mathrm { A R } } , ~ v _ { 1 : P } , ~ { \tilde { v } } _ { P + 1 : N } ]$。
- **Definition**: generation mode 是 Cosmos 3 通过不同 token layout 支持的输入输出配置，包括 Language、Text-to-Image、Text-to-Video (+Audio)、Image-to-Video/Video-to-Video (+Audio)、Video transfer 和 Action。
- **Boundary conditions**: Language mode 只包含 AR subsequence，generation-specific diffusion parameters 不激活；非语言生成模式通常包含 noisy diffusion tokens。
- **Related concepts**: ['token arrangement', 'AR subsequence', 'DM subsequence', 'action mode', 'video transfer']

## forward dynamics
- **Notation**: 在 Figure 4 的配置中，clean action tokens 作为条件，vision tokens 被 denoise。
- **Definition**: forward dynamics 是 action generation modes 之一，给定 observed context 和 clean action tokens，预测 future visual states。
- **Boundary conditions**: 它不同于 inverse dynamics；forward dynamics 预测的是未来视觉状态，而不是解释视觉转移所需的动作。
- **Related concepts**: ['action token', 'inverse dynamics', 'policy mode', 'world-action model', 'DM subsequence']

## inverse dynamics
- **Notation**: 在 Figure 4 的配置中，clean vision tokens 作为条件，action tokens 被 denoise。
- **Definition**: inverse dynamics 是 action generation modes 之一，根据 observed visual transition 推断解释该转移的 action tokens。
- **Boundary conditions**: 它不直接生成未来视觉后果；视觉 token 是条件，动作 token 是被预测对象。
- **Related concepts**: ['action token', 'forward dynamics', 'policy mode', 'world-action model']

## policy mode
- **Notation**: 在 Figure 4 的配置中，vision tokens 与 action tokens 同时作为 noisy targets 被 denoise。
- **Definition**: policy mode 是 video-action prediction 模式，模型联合预测 action 和 video tokens，从而在同一 sequence model 中生成 intervention 及其 expected visual consequence。
- **Boundary conditions**: 论文中该模式是 action 支持的三种生成模式之一；它不是仅输出控制命令的传统 policy，而是联合建模动作和视频。
- **Related concepts**: ['action token', 'forward dynamics', 'inverse dynamics', 'world-action model', 'Cosmos3-Nano-Policy-DROID']
