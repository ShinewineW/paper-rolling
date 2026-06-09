# Related Work

## R1: van den Oord et al. [28], Neural discrete representation learning, NeurIPS 2017
- **DOI**: NeurIPS 2017
- **Type**: method_adopted
- **Delta**:
  - What changed: GAIA-1采用VQ框架对视频帧进行离散化编码，但在编码器训练中额外加入DINO蒸馏损失以引导语义表征，且解码器仅用于训练标记器、不纳入最终系统
  - Why: 离散词元化是将连续视频帧转化为序列建模问题的关键前提，VQ方法提供了成熟的量化训练技术
- **Claims affected**: ['C1', 'C4']
- **Adopted elements**: ['向量量化（最近邻嵌入查找）', 'embedding loss', 'commitment loss']

## R2: Caron et al. [30], Emerging properties in self-supervised vision transformers, ICCV 2021
- **DOI**: ICCV 2021
- **Type**: method_adopted
- **Delta**:
  - What changed: 将预训练DINO模型的特征作为蒸馏目标，通过余弦相似度损失引导图像标记器，DINO参数本身冻结不参与训练
  - Why: DINO以其语义丰富的中间层特征著称，蒸馏这些特征可使词元空间具备语义聚类性质，降低世界模型的序列建模难度
- **Claims affected**: ['C4']
- **Adopted elements**: ['DINO特征作为蒸馏目标', '余弦相似度损失（inductive bias loss）']

## R3: Janner et al. [10], Offline reinforcement learning as one big sequence modeling problem, NeurIPS 2021
- **DOI**: NeurIPS 2021
- **Type**: method_adopted
- **Delta**:
  - What changed: GAIA-1将该将强化学习视为序列建模的思路推广至自动驾驶视频生成，处理比游戏环境复杂得多的真实视觉序列
  - Why: 序列建模框架使世界模型能够直接受益于大规模语言模型的架构设计和缩放特性
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['将状态/动作序列统一为词元流', '下一词元预测目标']

## R4: Kaplan et al. [49], Scaling laws for neural language models, arXiv 2020
- **DOI**: arXiv 2020
- **Type**: finding_extended
- **Delta**:
  - What changed: 验证了LLM中的幂律缩放规律在自动驾驶世界模型领域同样成立，将适用范围从语言建模拓展至视觉序列建模
  - Why: 如果世界模型满足缩放定律，则可通过小模型预测实验优化计算资源分配，无需训练完整大模型即可评估规模效益
- **Claims affected**: ['C2']
- **Adopted elements**: ['幂律拟合形式', '计算量估算公式C = 6N × 训练词元数']

## R5: Ho et al. [16], Imagen Video: High definition video generation with diffusion models, arXiv 2022
- **DOI**: arXiv 2022
- **Type**: method_adopted
- **Delta**:
  - What changed: GAIA-1采用视频扩散解码器从世界模型的离散词元还原高质量视频，并采用其v参数化和图像/视频多任务联合训练策略，额外加入自回归解码任务
  - Why: 扩散模型可生成时序一致的高分辨率视频，v参数化可避免色彩偏移和长期不一致问题，图像联合训练可提升单帧质量
- **Claims affected**: ['C1']
- **Adopted elements**: ['v参数化去噪目标', '图像与视频联合多任务训练', '3D U-Net骨干（空间+时间分离注意力）']

## R6: Ho & Salimans [45], Classifier-free diffusion guidance, arXiv 2022
- **DOI**: arXiv 2022
- **Type**: method_adopted
- **Delta**:
  - What changed: 将分类无关引导从连续扩散模型适配至离散词元自回归Transformer，通过在条件与无条件logits之间线性外推实现文本对齐增强，并设计了跨词元位置和帧的动态引导调度
  - Why: 训练文本标注质量有限，推理时引导可改善文本-图像对齐，通过动态调度因子在多样性与保真度之间取得平衡
- **Claims affected**: ['C1']
- **Adopted elements**: ['条件/无条件logits线性插值公式（论文公式3）', '负向提示（negative prompting）']
