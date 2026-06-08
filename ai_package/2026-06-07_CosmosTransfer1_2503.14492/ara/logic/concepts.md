# Concepts

## 时空控制图（Spatiotemporal Control Map）
- **Notation**: $$\mathbf{w} \in \mathbb{R}^{N \times X \times Y \times T}$$，其中 N 为模态数量，X、Y 为视频宽高，T 为帧数。第 i 个模态在第 j 个控制块输出的加权激活为 $\mathbf{w}_i \cdot \mathbf{h}_i^j$（逐元素乘积）。当各模态权重之和超过 1 时，论文明确施加归一化使其总和为 1。
- **Definition**: 一个形状为 N×X×Y×T 的实值权重张量，在推理阶段对 N 路模态控制分支的激活输出按时空位置分别施加不同权重，实现细粒度、逐位置的多模态自适应条件控制。
- **Boundary conditions**: 时空控制图仅在推理阶段使用，不进入训练目标；训练阶段每个控制分支独立训练，并不使用该权重张量对输出进行加权融合（分析推断，论文未显式声明训练期权重融合细节）。
- **Related concepts**: ['DiT-based ControlNet', '多模态自适应控制', 'SalientObject 算法', 'Sim2Real 域迁移']

## DiT-based ControlNet（扩散变换器控制网络）
- **Notation**: 基础去噪器公式 $$\mathbf{n} = D(\mathbf{x}_\sigma, \sigma)$$（式1）；加入条件后 $$\mathbf{n} = D(\mathbf{x}_\sigma, \sigma, \mathbf{c})$$（式2），其中 c 为条件 tokens。控制分支线性层零初始化，训练时冻结基础模型权重。
- **Definition**: 将 UNet-based ControlNet 扩展至扩散变换器（DiT）架构的条件生成框架：在基础 DiT 扩散模型之外增加一组控制分支，控制分支包含若干与基础模型权重初始化一致的变换器块，输出经零初始化线性层后加回主分支对应激活，从而在不破坏基础模型初始输出的前提下引入条件控制。
- **Boundary conditions**: 3 个控制块的选择系经验决策，论文未提供不同块数量的量化对比；相比 UNet-based ControlNet，DiT 版本的核心差别在于激活形状与残差连接结构，而非算法逻辑。
- **Related concepts**: ['时空控制图', '多模态自适应控制', 'Cosmos-Predict1']

## 多模态自适应控制（Adaptive Multimodal Control）
- **Notation**: N 路条件输入 $\mathbf{c}_1, \mathbf{c}_2, \ldots, \mathbf{c}_N$；各控制分支独立训练，推理时通过 $\mathbf{w} = \{\mathbf{w}_1, \mathbf{w}_2, \ldots, \mathbf{w}_N\}$ 融合（见图 2）。
- **Definition**: 为每种输入模态（模糊视觉 Vis、Canny 边缘 Edge、深度图 Depth、语义分割 Seg，以及自动驾驶专用的 HDMap 与 LiDAR）分别独立训练一个 ControlNet 分支，推理时通过时空控制图将所有分支的激活加权融合，统一输入主生成分支的条件生成策略。
- **Boundary conditions**: 模态独立训练与联合训练效果的系统对比未在论文中给出；融合操作仅在推理期进行，训练目标中不包含跨模态融合项。
- **Related concepts**: ['时空控制图', 'DiT-based ControlNet', 'TransferBench 评测集', 'Sim2Real 域迁移']

## Sim2Real 仿真到真实域迁移（Sim-to-Real Transfer）
- **Notation**: 论文未给出显式域迁移公式；仿真端提供多模态条件输入（深度、分割等），Cosmos-Transfer1 输出光真实感视频。机器人场景中 Setting 1 权重为 $w_{\mathrm{Edge}}(FG)=1, w_{\mathrm{Vis}}(FG)=1, w_{\mathrm{Seg}}(BG)=1$；Setting 2 权重为 $w_{\mathrm{Edge}}(FG)=1, w_{\mathrm{Seg}}(BG)=1$。
- **Definition**: 利用 Cosmos-Transfer1 将 CG 仿真渲染输出（连同其附带的分割图、深度图等结构化模态信号）转换为光照、纹理和细节更加真实的视频，以弥合合成数据与真实世界之间的视觉域差距，从而提升物理 AI 系统（机器人、自动驾驶等）在仿真数据上训练后的真实世界泛化能力。
- **Boundary conditions**: 论文评估仅覆盖特定场景（厨房操作、城市驾驶），在更复杂动态场景中的泛化能力未做系统分析；对下游策略训练效果的端到端验证未在本文涵盖。
- **Related concepts**: ['多模态自适应控制', '时空控制图', 'TransferBench 评测集', '自动驾驶数据增强']

## TransferBench 评测集
- **Notation**: 600 个样本；三类各 200 例。评测指标包括 Blur SSIM（Vis 对齐，↑优）、Edge F1（边缘对齐，↑优）、Depth si-RMSE（深度对齐，↓优）、Mask mIoU（分割对齐，↑优）、Diversity-LPIPS（多样性，↑优）、Quality Score（DOVER 技术分，↑优）。
- **Definition**: NVIDIA 团队为评估 Cosmos-Transfer1 专门构建的基准数据集，共 600 个样本，均匀覆盖三类 Physical AI 场景：机器人手臂操作（200 例，来自 AgiBot World）、驾驶（200 例，来自 OpenDV）、以自我为中心的日常生活场景（200 例，来自 Ego-Exo-4D）。
- **Boundary conditions**: 该评测集由论文作者自行构建，非独立第三方标准化 benchmark，存在潜在评估偏差；评测场景以 Physical AI 为核心，不代表通用视频生成任务的评估。
- **Related concepts**: ['多模态自适应控制', 'Sim2Real 域迁移', 'SalientObject 算法']

## 推理并行化扩展策略（Inference Parallelism Scaling）
- **Notation**: 论文未给出显式公式。Cosmos-Transfer1-7B 单次推理生成 5 秒、1280×704p、24fps 视频，预测 56K tokens；32 个注意力头；正向/负向 CFG 分配到两组 GPU，共 64 GPU 分担注意力计算；64 GPU 时端到端生成耗时 4.2 秒，扩散阶段 3.5 秒，实现实时生成（论文原文数字）。
- **Definition**: 针对 NVIDIA GB200 NVL72 机架设计的混合并行推理方案：在非注意力层采用纯数据并行（每块 GPU 保存完整模型副本），在注意力层采用头并行（head parallelism），通过 all-to-all 集合通信使每块 GPU 对完整 56K token 序列中的单个注意力头执行完整计算，从而充分利用 B200 GPU 的 192GB HBM 和 Blackwell FMHA 核的并发能力。
- **Boundary conditions**: 该策略专为 GB200 NVL72 设计，对其他硬件架构的适用性需另行验证；CFG 正负向分组的两组 GPU 划分方式在论文中为工程实现选择，未提供理论最优分析。
- **Related concepts**: ['Cosmos-Transfer1-7B', '实时世界生成', 'DiT-based ControlNet']

## 提示上采样器（Prompt Upsampler）
- **Notation**: 论文未给出显式公式。训练数据：每种模态各 100 万配对视频；使用 Gemma-2-9B-it 生成多样短提示；以 FSDP2 在所有模态数据上联合训练一个 epoch。
- **Definition**: 基于 Pixtral-12B 微调的多模态提示增强模块，同时接受用户输入的短提示文本与对应的条件模态视频（如分割图视频或深度图视频），将其转换为结构与训练分布一致的详细长提示，以缓解用户查询分布与 Cosmos-Transfer1 训练时所用详细描述之间的偏移。
- **Boundary conditions**: 提示上采样器为可选辅助组件，非 Cosmos-Transfer1 核心生成架构；论文未定量消融其对最终生成质量的独立贡献；其性能依赖所用的 VLM（Pixtral-12B）的视觉理解能力。
- **Related concepts**: ['多模态自适应控制', 'Cosmos-Transfer1-7B']
