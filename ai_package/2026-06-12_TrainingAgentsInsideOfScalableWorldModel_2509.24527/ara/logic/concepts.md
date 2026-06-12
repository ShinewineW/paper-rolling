# Concepts

## Dreamer 4
- **Notation**: 无单一符号；模型内部使用视频表示 z、动作 a、任务 q、奖励 r、价值 ν。
- **Definition**: Dreamer 4 是一个可扩展智能体，通过在快速且准确的 world model 内进行 imagination training 来学习控制任务。论文将它描述为由 causal tokenizer、interactive dynamics model、任务条件化的策略与奖励头，以及后续的想象强化学习组成。
- **Boundary conditions**: Dreamer 4 不是真实 Minecraft 引擎的完整复制品；论文明确指出其长期一致性、短记忆和库存预测仍有限。
- **Related concepts**: ['world model', 'imagination training', 'causal tokenizer', 'interactive dynamics model', 'agent tokens', 'PMPO']

## world model
- **Notation**: 输入包括动作序列 a、信号水平 τ、步长 d、被扰动表示 \tilde{z}；输出为干净表示 z_1 或其预测 \hat{z}_1。
- **Definition**: world model 学习从智能体视角预测潜在动作的未来结果，并可用来在想象中规划或做强化学习。本文中的 world model 由 tokenizer 和 dynamics model 组成，用于从视频、动作和噪声条件中预测未来表示。
- **Boundary conditions**: 它只基于冻结 tokenizer 的表示空间进行动态预测；论文没有声称它完全还原所有游戏状态，也没有声称可无误追踪长程库存或超出上下文的记忆。
- **Related concepts**: ['Dreamer 4', 'interactive dynamics model', 'shortcut forcing', 'causal tokenizer', 'unlabeled videos']

## causal tokenizer
- **Notation**: 视频帧 x 被编码为表示 z；每个时间步包含图像 patch tokens 和 learned latent tokens，latent 经线性投影和 tanh 得到低维表示。
- **Definition**: causal tokenizer 将原始视频帧压缩成供 dynamics model 消费和生成的连续表示。它包含 encoder、bottleneck 和 decoder，并在时间上使用因果结构，以支持时间压缩和逐帧解码。
- **Boundary conditions**: tokenizer 本身不是策略，也不直接决定动作；它主要承担视频压缩与重建，dynamics model 才负责动作条件下的未来表示预测。
- **Related concepts**: ['world model', 'masked autoencoding', 'efficient transformer architecture', 'interactive inference']

## interactive dynamics model
- **Notation**: 模型接收 a={a_t}、τ={τ_t}、d={d_t}、\tilde{z}={z_t^(τ_t)}，预测 z_1={z_t^1}。
- **Definition**: interactive dynamics model 在冻结 tokenizer 产生的表示和交错动作序列上运行，使用 shortcut forcing objective 训练，以支持低延迟、逐帧的交互式生成。
- **Boundary conditions**: 它预测的是 tokenizer 表示而非直接预测真实游戏状态；训练无动作视频时动作位置只使用 learned embedding，因此动作条件能力依赖有动作数据的对齐学习。
- **Related concepts**: ['shortcut forcing', 'x-prediction', 'register tokens', 'agent tokens', 'world model']

## shortcut forcing
- **Notation**: 信号水平为 τ，步长为 d；模型预测 \hat{z}_1=f_θ(\tilde{z},τ,d,a)，并用 x-space 的 flow 和 bootstrap 损失训练。
- **Definition**: shortcut forcing 是本文用于 dynamics model 的训练目标，结合 diffusion forcing 和 shortcut models，让模型在序列中按不同信号水平去噪，同时学习按指定步长完成采样步骤。
- **Boundary conditions**: shortcut forcing 是 dynamics model 的目标，不等同于 agent 的强化学习目标；论文还明确区分了预训练动态预测、行为克隆、奖励建模和想象强化学习阶段。
- **Related concepts**: ['diffusion forcing', 'shortcut models', 'x-prediction', 'ramp loss weight', 'interactive dynamics model']

## x-prediction
- **Notation**: 预测目标为 \hat{z}_1，而不是速度 υ=x_1-x_0；bootstrap 项中先把网络输出转换到 v-space 再把损失缩回 x-space。
- **Definition**: x-prediction 指 dynamics model 直接预测干净表示，而不是预测从噪声到数据的速度。论文称这种参数化在逐帧生成长视频时比 v-prediction 更有利于高质量 rollout。
- **Boundary conditions**: 这是作者基于实验与假设的设计选择；论文没有把它表述为所有扩散或流模型的通用最优参数化。
- **Related concepts**: ['shortcut forcing', 'interactive dynamics model', 'ramp loss weight', 'v-prediction']

## ramp loss weight
- **Notation**: 论文给出显式公式 $$
{ w ( \tau ) = 0 . 9 \tau + 0 . 1 }\tag{8}
$$
- **Definition**: ramp loss weight 是随信号水平增加的损失权重，用来把模型容量更多分配给学习信号更强的时间步与噪声水平。
- **Boundary conditions**: 该权重作用于 world model 的动态预测训练；它不是策略奖励，也不是推理时的动作选择准则。
- **Related concepts**: ['shortcut forcing', 'signal level', 'x-prediction', 'flow matching']

## imagination training
- **Notation**: rollout 中采样表示 z={z_t} 和动作 a={a_t}，用 reward head 标注 r={r_t}，用 value head 标注 ν={ν_t}。
- **Definition**: imagination training 是在 world model 生成的轨迹中训练策略和价值头的过程。本文先用数据集训练任务条件策略和奖励模型，再在模型 rollout 上用强化学习改进策略。
- **Boundary conditions**: 训练期间没有真实环境交互；因此改进依赖 world model 和 reward model 的准确性，论文没有声称想象轨迹等价于真实环境轨迹。
- **Related concepts**: ['Dreamer 4', 'PMPO', 'reward model', 'value head', 'behavioral prior']

## agent tokens
- **Notation**: 任务 q 输入到 agent tokens；其输出嵌入 h_t 供 MLP heads 预测动作、奖励和价值。
- **Definition**: agent tokens 是在 agent finetuning 阶段插入 dynamics transformer 的额外模态，用于接收任务嵌入并预测 policy、reward 和 value。
- **Boundary conditions**: 论文强调其他模态不能反向注意到 agent tokens，以避免 world model 的未来预测被当前任务直接影响；因此 agent tokens 不是用来改写环境动态的通道。
- **Related concepts**: ['task embeddings', 'policy head', 'reward model', 'value head', 'causal confusion']

## PMPO
- **Notation**: advantage 写作 A_t=R_t^λ-ν_t；状态按 A_t≥0 与 A_t<0 分入正集合和负集合。
- **Definition**: PMPO 是本文用于策略头的强化学习目标，依据 advantage 的符号而非幅度组织正负反馈，并结合 behavioral cloning prior 约束策略。
- **Boundary conditions**: PMPO 只用于想象强化学习阶段的 policy head；transformer 在该阶段被冻结，论文没有把 PMPO 用作 world model 预训练目标。
- **Related concepts**: ['imagination training', 'behavioral prior', 'value head', 'policy head']
