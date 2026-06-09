# Concepts

## 截断扩散策略
- **Notation**: 训练阶段截断步数 $T_{\mathrm{trunc}} \ll T$；实际使用 50/1000 截断比例；推理阶段仅需 2 步去噪
- **Definition**: 一种改进的扩散策略，在训练与推理阶段均截断扩散时间步长，使模型从「锚定高斯分布」出发而非从标准高斯噪声出发进行去噪，以此将先验驾驶模式嵌入扩散过程。
- **Boundary conditions**: 该概念专指同时截断训练扩散时间表与推理去噪步数这一联合设计；单独截短推理步数（不截断训练时间表）属于不同方法；该策略依赖锚点质量，若锚点无法覆盖潜在动作空间（例如仅用一个外推轨迹锚点）则效果下降（论文 Table 8 验证）。
- **Related concepts**: ['锚定高斯分布', 'DDIM推理更新规则', '模式多样性分数']

## 锚定高斯分布
- **Notation**: $$\tau_k^i = \sqrt{\bar{\alpha}^i}\mathbf{a}_k + \sqrt{1-\bar{\alpha}^i}\epsilon,\quad \epsilon \sim \mathcal{N}(0,\mathbf{I})$$，其中 $i \in [1, T_{\mathrm{trunc}}]$，锚点集 $\{\mathbf{a}_k\}_{k=1}^{N_{\mathrm{anchor}}}$
- **Definition**: 以 K-Means 聚类训练集轨迹所得的先验锚点为中心、叠加少量高斯噪声后构成的多峰子高斯分布集合，用于替代标准高斯噪声作为扩散策略的初始采样分布。
- **Boundary conditions**: 锚定高斯分布在推理阶段可使用任意数量 $N_{\mathrm{infer}}$ 的噪声样本（与训练时 $N_{\mathrm{anchor}}$ 解耦），体现推理灵活性；它不同于 VADv2 等方法中的固定大词汇表离散锚点，前者通过扩散模型的连续生成能力覆盖词汇表外场景。
- **Related concepts**: ['截断扩散策略', 'K-Means锚点聚类', '推理灵活性']

## 模式多样性分数
- **Notation**: $$\mathcal{D} = 1 - \frac{1}{N}\sum_{i=1}^{N}\frac{\mathrm{Area}(\tau_i \cap \bigcup_{j=1}^{N}\tau_j)}{\mathrm{Area}(\tau_i \cup \bigcup_{j=1}^{N}\tau_j)}$$，其中 $\tau_i$ 为第 $i$ 条去噪轨迹，$N$ 为采样轨迹总数
- **Definition**: 一种基于均值交并比（mIoU）的定量指标，用于度量扩散策略生成的多条轨迹之间的多样性，数值越高表示轨迹越多样，越低表示轨迹趋于同质（即模式坍塌程度越高）。
- **Boundary conditions**: 该指标仅衡量轨迹的空间覆盖多样性，不直接衡量每条轨迹的可行性与安全性；高 $\mathcal{D}$ 分数是多模态能力的必要条件而非充分条件，需结合 PDMS 等规划质量指标综合评估。
- **Related concepts**: ['模式坍塌', '截断扩散策略', '多模态驾驶动作分布']

## 级联扩散解码器
- **Notation**: 解码器 $f_\theta$；输入 $\{\hat{\tau}_k\}_{k=1}^{N_{\mathrm{infer}}}$ 噪声轨迹与条件信息 $z$；输出分类置信分 $\{\hat{s}_k\}$ 与去噪坐标 $\{\hat{\tau}_k\}$；堆叠 2 个级联层；参数量 60M
- **Definition**: 一种基于 Transformer 的轻量级扩散解码器，通过稀疏可变形注意力与 BEV/视角特征进行空间交叉注意力，同时与感知模块的智能体/地图查询进行跨模态交互，并在每个去噪步骤内以级联方式迭代精炼轨迹预测。
- **Boundary conditions**: 该解码器专为驾驶场景设计，依赖感知模块提供的结构化查询（目标检测框/地图向量）；在 NAVSIM 设置中仅使用 BEV 特征与智能体查询，在 nuScenes 设置中额外使用地图查询与透视视图特征，两种设置的解码器结构保持一致但输入略有差异。
- **Related concepts**: ['截断扩散策略', '稀疏可变形注意力', '时间步调制层']

## 模式坍塌
- **Notation**: 用模式多样性分数 $\mathcal{D}$ 量化；Transfuser$_{\mathrm{DP}}$（香草扩散策略）的 $\mathcal{D}$ 为 11%
- **Definition**: 将标准扩散策略直接应用于端到端自动驾驶时出现的现象：从不同随机高斯噪声出发经去噪后，生成的多条轨迹高度重叠、缺乏多样性，无法覆盖真实驾驶中的多种行为模式（如直行、换道、转弯）。
- **Boundary conditions**: 模式坍塌与重计算开销是原始扩散策略在驾驶场景面临的两个独立问题；截断扩散策略通过锚定高斯分布同时缓解两者，但两者的根源不同——模式坍塌源于初始分布无先验结构，重计算开销源于去噪步数过多。
- **Related concepts**: ['模式多样性分数', '锚定高斯分布', '截断扩散策略']

## 条件扩散模型（前向与反向过程）
- **Notation**: 前向：$$q(\tau^i|\tau^0) = \mathcal{N}(\tau^i;\sqrt{\bar{\alpha}^i}\tau^0,(1-\bar{\alpha}^i)\mathbf{I})$$；反向：$$p_\theta(\tau^0|z) = \int p(\tau^T)\prod_{i=1}^{T}p_\theta(\tau^{i-1}|\tau^i,z)\mathrm{d}\tau^{1:T}$$；其中 $\bar{\alpha}^i = \prod_{s=1}^{i}(1-\beta^s)$，$\beta^s$ 为噪声时间表
- **Definition**: 扩散模型的基础框架：前向过程逐步向干净数据样本添加高斯噪声，反向过程以场景条件信息为引导，通过可学习模型逐步去噪还原干净样本。
- **Boundary conditions**: 论文给出了前向加噪公式（公式 1）和反向生成的积分形式（公式 2）作为预备知识，这些是 DDPM/DDIM 的标准框架，并非 DiffusionDrive 的创新点；DiffusionDrive 的创新在于对该框架的截断改造（公式 4）及训练目标（公式 6）。
- **Related concepts**: ['截断扩散策略', 'DDIM推理更新规则', '训练目标']

## 推理灵活性
- **Notation**: 训练时 $N_{\mathrm{anchor}} = 20$；推理时 $N_{\mathrm{infer}}$ 可选 10、20、40 等任意值
- **Definition**: 截断扩散策略的一项关键特性：模型在训练阶段固定使用 $N_{\mathrm{anchor}}$ 条噪声轨迹，但在推理阶段可动态调整采样噪声轨迹数量 $N_{\mathrm{infer}}$，使其独立于训练配置，可按计算资源或应用需求灵活选择。
- **Boundary conditions**: 推理灵活性指的是采样数量 $N_{\mathrm{infer}}$ 的可调性，而非去噪步数的灵活性；去噪步数在论文主要设置中固定为 2 步，Table 4 验证了 1~3 步的性能差异但这属于另一维度的调节。
- **Related concepts**: ['锚定高斯分布', '截断扩散策略', '级联扩散解码器']

## PDM分数（PDMS）
- **Notation**: PDMS 由以下子分数加权合成：无责任碰撞分数（NC）、可行驶区域合规分数（DAC）、碰撞时间分数（TTC）、舒适度分数（Comf.）、自车进度分数（EP）
- **Definition**: NAVSIM 数据集采用的规划导向评估指标，是多个子分数的加权组合，全面衡量自动驾驶规划的安全性、舒适性与进度效率。
- **Boundary conditions**: PDMS 基于 top-1 置信分最高的轨迹计算，不衡量多模态生成质量；因此论文额外引入模式多样性分数 $\mathcal{D}$ 作为补充指标。PDMS 仅适用于 NAVSIM 数据集，nuScenes 数据集使用 L2 误差与碰撞率等开环指标。
- **Related concepts**: ['NAVSIM数据集', '模式多样性分数', '端到端自动驾驶规划']
