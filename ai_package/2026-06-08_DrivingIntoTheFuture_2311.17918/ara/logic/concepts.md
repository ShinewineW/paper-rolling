# Concepts

## 驾驶世界模型(Driving World Model)
- **Notation**: 去噪模型 $$\mathbf{f}_{\theta,\phi,\psi}$$ ,其中 $\theta$ 为空间参数，$\phi$ 为时序参数，$\psi$ 为多视角参数；输入多视角视频张量 $$\mathbf{x} \in \mathbb{R}^{T \times K \times 3 \times H \times W}$$
- **Definition**: 一种能够在像素空间中根据当前多视角观测与自车动作预测未来场景状态的生成模型。与向量化状态空间世界模型不同，Drive-WM 直接在高分辨率像素空间建模，无需额外的向量标注，并兼容现有端到端规划器。
- **Boundary conditions**: 世界模型仅在像素空间运作，推理时需要显式条件输入（动作、布局或文本）；不具备主动感知能力，视频质量受扩散步数与条件精度影响；训练数据为 nuScenes，分布外极端动作（如掉头）需额外数据增强才能保证质量。
- **Related concepts**: ['多视角联合建模', '视图分解生成', '基于图像的奖励函数', '端到端自动驾驶规划']

## 多视角联合时序建模(Joint Multiview Temporal Modeling)
- **Notation**: 编码后隐变量 $$\mathbf{z} \in \mathbb{R}^{T \cdot K \times C \times \hat{H} \times \hat{W}}$$；时序维度重排 $(TK)CHW \rightarrow KCTHW$；视角维度重排 $(KHW)TC \rightarrow (THW)KC$；训练目标(去噪得分匹配): $$\mathbb{E}_{\mathbf{z}\sim p_{\mathrm{data}},\tau\sim p_\tau,\epsilon\sim\mathcal{N}(\mathbf{0},I)}[\lVert \mathbf{y} - \mathbf{f}_{\theta,\phi,\psi}(\mathbf{z}_\tau;\mathbf{c},\tau)\rVert_2^2]$$
- **Definition**: 在预训练图像扩散模型基础上引入时序层（temporal encoding layers）和多视角层（multiview encoding layers），使模型能够同时对 T 帧 × K 视角的视频在时间与空间维度统一去噪。时序层通过 3D 卷积与多头自注意力强化帧间依赖；多视角层将隐变量按视角维度排列后施加自注意力，使各视角具备相似风格与整体结构一致性。
- **Boundary conditions**: 联合建模本身（不加分解）对重叠区域一致性保证有限，消融实验显示 KPM 仅为 45.8%；视频帧长 T=8 在训练阶段固定，长视频依赖滑窗续帧；分辨率训练时为 384×192，Waymo 推理可扩展至 768×512 但依赖相同超参数。
- **Related concepts**: ['驾驶世界模型', '视图分解生成', '统一条件接口', '潜在视频扩散模型']

## 视图分解生成(Factorized Multiview Generation)
- **Notation**: 参考视角 $\mathbf{x}_r$，拼接视角 $\mathbf{x}_s$，含时序条件帧 $\mathbf{x}_{pre}$ 的分解公式: $$p(\mathbf{x}) = p(\mathbf{x}_r|\mathbf{x}_{pre})\,p(\mathbf{x}_s|\mathbf{x}_r,\mathbf{x}_{pre})$$；nuScenes 参考视角选取 {F, BL, BR}，拼接视角为 {FL, B, FR}
- **Definition**: 将多视角联合分布 $p(\mathbf{x}_{1,\ldots,K})$ 分解为「参考视角」(reference views)和「拼接视角」(stitched views)两类：先用联合模型生成不重叠的参考视角视频，再以参考视角为额外图像条件生成与之有重叠的拼接视角视频，从而在保持生成效率的同时大幅提升视角间像素一致性。
- **Boundary conditions**: 分解方案预设视角拓扑关系（相邻视角有重叠），不适用于任意摄像头布局；拼接视角数量受参考视角数量约束；推理时需先完成所有参考视角生成后才能启动拼接视角生成，存在串行等待时延。
- **Related concepts**: ['多视角联合时序建模', '统一条件接口', 'KPM 评估指标']

## 统一条件接口(Unified Condition Interface)
- **Notation**: 图像条件 $\mathbf{i}=(i_1,\ldots,i_n)\in\mathbb{R}^{n\times d}$；布局条件 $\mathbf{l}=(l_1,\ldots,l_k)\in\mathbb{R}^{k\times d}$；文本条件 $\mathbf{e}=(e_1,\ldots,e_m)\in\mathbb{R}^{m\times d}$；动作条件 $\mathbf{a}\in\mathbb{R}^{2\times d}$；第 t 帧统一条件: $$\mathbf{c}_t = [\mathbf{i}_0,\mathbf{l}_0,\mathbf{e}_0,\mathbf{a}_t]\in\mathbb{R}^{(n+k+m+2)\times d}$$
- **Definition**: 将多种异构条件（初始上下文帧、参考视角图像、3D 检测框/HD 地图/BEV 分割等布局信息、CLIP 文本嵌入、以及自车动作）统一映射到 d 维特征空间后沿 token 长度维度拼接，作为去噪 UNet 的跨注意力输入，无需为每种条件设计独立接口。
- **Boundary conditions**: 动作被简化为二维位置增量，未显式编码姿态、加速度等信息，需下游规划器（如 VAD）提供完整轨迹候选；布局条件将 3D 信息投影到 2D 透视图，存在深度信息损失；接口在统一维度 d 下运作，不同条件间表达能力受模态编码器质量制约。
- **Related concepts**: ['驾驶世界模型', '多视角联合时序建模', '视图分解生成']

## 基于图像的奖励函数(Image-based Reward Function)
- **Notation**: 总奖励 = 地图奖励 × 障碍物奖励（论文仅给出文字定义，未给出显式数学公式）；感知使用基于图像的 3D 目标检测器[37]和在线 HDMap 预测器[38]
- **Definition**: 在世界模型生成的未来视频上运行图像感知模型，得到地图奖励（距路缘距离 + 中心线一致性）和障碍物奖励（纵横向离其他交通参与者的距离），二者相乘得到总奖励，用于在树形规划展开中筛选最优轨迹候选。
- **Boundary conditions**: 奖励计算依赖扩散模型生成视频的质量与感知模型的精度，生成噪声或感知误差会导致奖励信号不准；当前方案需在每个规划步运行多轮视频生成（对应不同轨迹候选），推理时延较高；非向量化奖励（如 GPT-4V 路径）在论文中仅作为概念验证展示，未在主定量实验中评测。
- **Related concepts**: ['树形规划展开', '驾驶世界模型', '端到端自动驾驶规划']

## 树形规划展开(Tree-based Rollout)
- **Notation**: 动作定义 $\mathbf{a}_t = (x_{t+1}-x_t,\, y_{t+1}-y_t)$；利用公式(5)中的统一条件进行每一步的视频生成与奖励评估
- **Definition**: 在每个决策时刻，从端到端规划器中采样多条轨迹候选（「直行」「左转」「右转」），以各轨迹对应的动作序列驱动世界模型生成对应的未来多视角视频，通过图像奖励函数评估后选出最优轨迹，并将该时刻扩展为规划树的下一节点；如此迭代形成树结构的滚动预测。
- **Boundary conditions**: 每步需对所有轨迹候选（当前实验为 3 条）独立运行视频生成，计算代价随候选数线性增长；树的深度受世界模型生成质量的积累误差限制；当前实现为开环评估，闭环反馈效果尚未完整验证。
- **Related concepts**: ['基于图像的奖励函数', '驾驶世界模型', '统一条件接口']

## 关键点匹配一致性评分(KPM, Key Points Matching Score)
- **Notation**: $$\text{KPM}(\%) = \frac{1}{|\text{images}|}\sum_i \frac{\text{matched\_pts\_generated}_i}{\text{matched\_pts\_real}_i} \times 100$$（论文以文字定义，此为结构化表述，分析推断，论文未显式声明该公式形式）；每场景均匀采样 8 帧计算
- **Definition**: 一种专为多视角生成视频设计的新评估指标，利用预训练特征匹配模型（LoFTR）计算生成图像与相邻视角在重叠区域的匹配关键点数量，再与真实数据的匹配点数取比值后平均，衡量多视角生成一致性。FID 和 FVD 无法量化跨视角一致性，KPM 作为补充指标解决此问题。
- **Boundary conditions**: KPM 依赖 LoFTR 匹配模型，在纹理稀疏（如空旷路面、夜间）区域匹配点数可能本身较少，造成比值方差偏大；仅量化重叠区域的结构一致性，不反映单视角图像质量（由 FID/FVD 覆盖）；当真实数据匹配点数接近零时分母趋小，需特殊处理。
- **Related concepts**: ['视图分解生成', '多视角联合时序建模']
