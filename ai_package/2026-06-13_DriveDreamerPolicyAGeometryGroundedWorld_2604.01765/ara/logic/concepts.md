# Concepts

## DriveDreamer-Policy
- **Notation**: 输入由 natural-language instruction、synchronized multi-view RGB observations、current action 与 learnable query tokens 组成；输出经 depth generator、video generator、action generator 分别产生 depth maps、future videos、future actions。
- **Definition**: 一种统一的驾驶 world-action model，将 large language model 与轻量级 generative experts 结合，在同一框架内支持 depth generation、future video generation 和 motion planning。
- **Boundary conditions**: 它不是只做 VLA 轨迹预测的 planner，也不是只生成未来视频的 world model；论文强调其统一生成和规划，但没有把它描述为端到端单一解码头结构。
- **Related concepts**: ['world-action model', 'large language model', 'generative experts', 'depth generator', 'video generator', 'action generator']

## geometry-aware world representation
- **Notation**: depth-query world embedding 作为 cross-attention 的 keys/values 条件 depth denoiser，并作为上游几何特征被后续 video queries 和 action queries 访问。
- **Definition**: 由 depth learning 与 world embeddings 形成的几何感知世界表征，用显式 depth 作为场景 3D scaffold，为 future video imagination 和 action planning 提供几何约束。
- **Boundary conditions**: 论文将 depth 作为显式几何脚手架，但没有声称完整恢复 3D occupancy 或 HD map；其 depth label 来自 DA3，而非额外采集的真值深度传感器。
- **Related concepts**: ['depth generator', 'depth queries', 'world embeddings', '3D scaffold', 'causal ordering']

## fixed-size query bottleneck
- **Notation**: query groups 的顺序为 depth queries、video queries、action queries；downstream heads 读取对应 query embeddings 生成 depth、video 和 action。
- **Definition**: 一种稳定紧凑的接口设计，将 depth queries、video queries 和 action queries 作为 learnable query token groups 追加到输入 token 后，由 LLM 产生对应的 world embeddings 与 action embeddings。
- **Boundary conditions**: 这是接口与容量控制机制，不等同于论文中的某个具体生成损失；query 数量会影响容量，但概念本身不限定某个固定预算。
- **Related concepts**: ['depth queries', 'video queries', 'action queries', 'LLM', 'cross-attention']

## causal 3D→2D→1D conditioning pathway
- **Notation**: 同一决策步内 attention pattern 满足 depth queries→video queries→action queries。
- **Definition**: 一种跨 query groups 的结构化因果注意力顺序：depth queries 先形成几何上下文，video queries 可关注 depth context，action queries 可关注 depth 和 video context。
- **Boundary conditions**: 论文称其避免额外同步或跨分支迭代细化；因此不要把它解释成多轮闭环搜索、MPC 或推理时反复优化过程。
- **Related concepts**: ['causal ordering', 'depth queries', 'video queries', 'action queries', 'planning']

## Depth Generator
- **Notation**: 训练时采样 continuous flow time，将 ground-truth depth 加噪；denoiser 输入 noisy depth 与对应 RGB image 的拼接，并预测 denoising update。
- **Definition**: 用于生成 monocular depth map 的 pixel-space diffusion transformer，以 flow-matching objective 训练，并通过 LLM world depth embeddings 进行 cross-attention 条件化。
- **Boundary conditions**: 它生成的是 monocular depth map，不是 RGB video；论文强调 pixel-space 对 depth 可行，因为 depth 维度低于 RGB video，并不需要额外 learned codec。
- **Related concepts**: ['pixel-space diffusion transformer', 'flow matching', 'depth-query world embedding', 'DA3', 'PPD']

## Video Generator
- **Notation**: current RGB images 先经 VAE 编码成 compact latent representation，再初始化 target horizon 的 noisy video latents；video denoiser 在每个 transformer block 通过 cross-attention 关注 world embeddings。
- **Definition**: 用于 future video generation 的 text-image-to-video diffusion transformer，接收当前 RGB 图像的 latent 初始化，并以 LLM world video embeddings 和视觉条件作为生成条件。
- **Boundary conditions**: 论文说明 video generator 替代标准 text-to-video 中的 text embedding 条件，但没有把它描述为直接由文字单独驱动的开放域视频生成器。
- **Related concepts**: ['future video generation', 'VAE', 'world video embeddings', 'CLIP', 'action-aware video generation']

## Action Generator
- **Notation**: trajectory state 使用连续表示 $( x , y ,$ cos ??, sin ??)，以避免 angular wrap-around 并鼓励平滑转向动态。
- **Definition**: 一个独立的 diffusion transformer，将 noise trajectory 映射为 feasible future action sequence，并通过 action query tokens 产生的 action embedding 进行 cross-attention 条件化。
- **Boundary conditions**: 它不依赖显式运行 depth 和 video generation 才能规划；但论文也没有声称动作生成完全脱离 LLM 表征或上游 query 信息。
- **Related concepts**: ['action embeddings', 'motion planning', 'diffusion transformer', 'future action sequence', 'trajectory state']

## Flow Matching
- **Notation**: 显式公式为 $$
x _ { t } = \left( 1 - t \right) x _ { 0 } + t x _ { 1 } , \quad t \sim \mathcal { U } ( 0 , 1 ) ,\tag{1}
$$ 与 $$
\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { x _ { 0 } , x _ { 1 } , t } \left[ \left. v _ { \theta } ( x _ { t } , t \vert c ) - ( x _ { 1 } - x _ { 0 } ) \right. _ { 2 } ^ { 2 } \right] .\tag{2}
$$
- **Definition**: 论文用于连续目标生成专家训练的条件生成原则，学习 time-dependent velocity field，将简单噪声分布沿预定义路径运输到数据分布。
- **Boundary conditions**: 这是生成专家的训练原则；论文另给出 joint multi-task loss，但没有为每个子损失进一步展开新的显式公式。
- **Related concepts**: ['conditional flow matching', 'velocity field', 'diffusion transformer', 'depth generator', 'action generator']

## joint multi-task loss
- **Notation**: 论文显式给出 $$
\mathcal { L } = \lambda _ { d } \mathcal { L } _ { d } + \lambda _ { v } \mathcal { L } _ { v } + \lambda _ { a } \mathcal { L } _ { a } ,\tag{3}
$$ 其中 $\mathcal { L } _ { d }$、$\mathcal { L } _ { v }$、$\mathcal { L } _ { a }$ 分别对应 depth、video 和 trajectory。
- **Definition**: 单阶段训练中联合优化 depth prediction、video prediction 和 trajectory prediction 的总损失。
- **Boundary conditions**: 不要把只在推理或模块条件化中使用的注意力信息流误写成额外训练目标；论文没有给出更细的每项损失展开。
- **Related concepts**: ['Training Objective and Optimization', 'Depth Generator', 'Video Generator', 'Action Generator', 'single-stage training']
