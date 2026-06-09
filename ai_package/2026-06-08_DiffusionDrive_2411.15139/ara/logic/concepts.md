# Concepts

## 截断扩散策略
- **Notation**: $T_{\mathrm{trunc}}$：截断后的扩散步数；$i \in [1, T_{\mathrm{trunc}}]$；$\tau_k^i = \sqrt{\bar{\alpha}^i}\mathbf{a}_k + \sqrt{1-\bar{\alpha}^i}\epsilon,\ \epsilon \sim \mathcal{N}(0,\mathbf{I})$
- **Definition**: 一种改进的扩散策略，将标准扩散过程截断，仅在先验锚点轨迹上添加少量高斯噪声，使模型从锚点高斯分布出发进行去噪，而非从纯高斯噪声出发。训练时扩散步数截断为 $T_{\mathrm{trunc}} \ll T$，推理时仅需 2 步去噪即可生成高质量多模态轨迹。
- **Boundary conditions**: 截断范围为噪声调度的 50/1000，适用于驾驶轨迹生成场景；该策略与图像生成领域的 TDPM 在动机上相似，但后者使用隐式中间分布，本方法引入显式驾驶先验。对于分布外（OOD）极端场景，锚点覆盖能力存在上限，但论文实验证明 20 个锚点已能覆盖主要驾驶模式。
- **Related concepts**: ['锚点高斯分布', 'K-Means先验锚点', '条件扩散模型', 'DDIM']

## 锚点高斯分布
- **Notation**: $\{\mathbf{a}_k\}_{k=1}^{N_{\mathrm{anchor}}}$：先验锚点集合；$\tau_k^i \sim \mathcal{N}(\sqrt{\bar{\alpha}^i}\mathbf{a}_k,\ (1-\bar{\alpha}^i)\mathbf{I})$
- **Definition**: 通过对 K-Means 聚类得到的先验锚点轨迹加入少量高斯噪声所形成的分布集合。每个锚点对应一个以该锚点为中心的子高斯分布，整体构成多个子高斯分布的混合，覆盖多模态驾驶行为空间。
- **Boundary conditions**: 锚点数量远小于 VADv2 的 8192 个固定词汇锚点，但通过扩散模型的分布表达能力弥补了数量不足。锚点通过 K-Means 从训练集聚类得到，本身不携带测试集信息，论文用跨数据集实验（NAVSIM 锚点在 CARLA 上泛化）验证了这一点。
- **Related concepts**: ['截断扩散策略', 'K-Means先验锚点', '推理灵活性']

## 模式多样性得分
- **Notation**: $$\mathcal{D} = 1 - \frac{1}{N}\sum_{i=1}^{N}\frac{\mathrm{Area}(\tau_i \cap \bigcup_{j=1}^{N}\tau_j)}{\mathrm{Area}(\tau_i \cup \bigcup_{j=1}^{N}\tau_j)}$$
- **Definition**: 一种基于 mIoU 定义的轨迹多样性量化指标，衡量一组去噪轨迹中各条轨迹相对于所有轨迹并集的独特覆盖程度。得分越高表示轨迹越多样，模式坍塌程度越低。
- **Boundary conditions**: 该指标通过轨迹区域面积的 IoU 计算，仅反映轨迹空间覆盖的多样性，不直接衡量轨迹质量或可行性。需结合 PDMS 等质量指标共同评估规划效果，论文中 Tab.2 同时报告两者。
- **Related concepts**: ['截断扩散策略', '模式坍塌', '轨迹去噪']

## 级联扩散解码器
- **Notation**: $f_\theta(\{\tau_k^i\}_{k=1}^{N_{\mathrm{anchor}}}, z) = \{\hat{s}_k, \hat{\tau}_k\}_{k=1}^{N_{\mathrm{anchor}}}$；其中 $z$ 为条件场景上下文
- **Definition**: 一种基于 Transformer 的高效扩散解码器，通过稀疏可变形注意力与 BEV/PV 特征交互，同时与感知模块的 agent/map 查询进行跨注意力，并采用级联机制在每个去噪步骤内迭代精化轨迹预测。解码器参数在不同去噪时间步间共享。
- **Boundary conditions**: 级联层数存在收益递减：2层到4层仅有微小提升，但参数从 60M 增至 65M。解码器设计依赖感知模块提供的结构化查询（object queries、BEV features），若感知模块不提供这些特征则需适配。参数在去噪时间步间共享（非级联层间共享）。
- **Related concepts**: ['截断扩散策略', '稀疏可变形注意力', 'Timestep Modulation', '锚点高斯分布']

## 训练目标函数
- **Notation**: $$\mathcal{L} = \sum_{k=1}^{N_{\mathrm{anchor}}}[y_k \mathcal{L}_{\mathrm{rec}}(\hat{\tau}_k, \tau_{\mathrm{gt}}) + \lambda\mathrm{BCE}(\hat{s}_k, y_k)]$$
- **Definition**: DiffusionDrive 的训练损失由轨迹重建损失和二元交叉熵分类损失组成，仅对最近锚点（正样本）计算重建损失，所有锚点均参与分类损失。
- **Boundary conditions**: 重建损失仅作用于正样本锚点，负样本仅参与分类监督，这意味着负锚点的去噪质量由隐式的分类信号间接约束。$\lambda$ 的具体取值论文未显式说明。
- **Related concepts**: ['截断扩散策略', '级联扩散解码器', '锚点高斯分布']

## K-Means先验锚点
- **Notation**: $\{\mathbf{a}_k\}_{k=1}^{N_{\mathrm{anchor}}}$，其中 $\mathbf{a}_k = \{(x_t, y_t)\}_{t=1}^{T_f}$；NAVSIM 实验中 $N_{\mathrm{anchor}}=20$，nuScenes 实验中 $N_{\mathrm{anchor}}=18$
- **Definition**: 通过在训练集上对驾驶轨迹运行 K-Means 聚类算法得到的一组代表性轨迹，作为截断扩散策略中锚点高斯分布的中心点，捕捉主要驾驶模式（如直行、左转、右转、变道等）。
- **Boundary conditions**: 锚点从训练集聚类，对训练集分布的覆盖有依赖；若测试集包含训练集中极少出现的极端机动（如掉头、极急变道），锚点可能无法提供有效先验。此外，K-Means 聚类结果受随机初始化影响，论文未说明具体聚类超参数。
- **Related concepts**: ['锚点高斯分布', '截断扩散策略', '推理灵活性']

## 推理灵活性
- **Notation**: $N_{\mathrm{infer}}$：推理时采样数量，可与 $N_{\mathrm{anchor}}$ 不同；训练时 $N_{\mathrm{anchor}}=20$，推理时论文对比了 $N_{\mathrm{infer}} \in \{10, 20, 40\}$
- **Definition**: DiffusionDrive 在推理阶段可独立于训练时的锚点数量 $N_{\mathrm{anchor}}$，动态调整采样轨迹数量 $N_{\mathrm{infer}}$，以适应不同计算资源或应用需求，实现采样数量与规划质量之间的灵活权衡。
- **Boundary conditions**: 增大 $N_{\mathrm{infer}}$ 的收益在 40 个采样时已基本饱和（88.2 PDMS，仅比 20 个的 88.1 高 0.1），说明锚点高斯分布对动作空间的覆盖存在上限；进一步增大采样数量带来的增益受限于先验锚点的分布覆盖范围。
- **Related concepts**: ['锚点高斯分布', 'K-Means先验锚点', '截断扩散策略']
