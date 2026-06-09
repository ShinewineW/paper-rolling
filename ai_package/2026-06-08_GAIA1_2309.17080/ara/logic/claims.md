# Claims

## C1: GAIA-1将世界建模重新表述为多模态无监督序列建模问题
- **Statement**: GAIA-1将世界建模定义为无监督下一词元预测问题，通过将视频帧、文本和动作编码为离散词元序列，利用自回归Transformer预测未来图像词元，实现对自车行为和场景特征具备精细控制能力的真实驾驶视频生成。
- **Status**: empirical
- **Falsification criteria**: 若模型无法根据文本/动作条件生成语义一致的视频，或生成质量远低于专用方法，则该声明不成立。
- **Proof**: [E1, E3, E5]
- **Evidence basis**: ['E1', 'E3', 'E5']
- **Interpretation**: 将LLM的下一词元预测范式迁移至自动驾驶视频生成领域，通过双组件设计（世界模型负责高层推理，扩散解码器负责像素质量）弥合语义建模与感知真实性之间的差距。
- **Tags**: ['improvement', 'descriptive']

## C2: LLM中的缩放定律同样适用于GAIA-1世界模型
- **Statement**: 与大型语言模型中观察到的缩放规律类似，GAIA-1世界模型的验证交叉熵与模型规模/计算量之间遵循幂律关系，可用不超过1/20计算量的小模型准确预测最终性能。
- **Status**: empirical
- **Falsification criteria**: 若幂律拟合在外推至6.5B模型时出现系统性偏差，或损失曲线在不同规模间不符合幂律形式，则该声明不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该结果表明以序列建模方式构建世界模型可获得与语言模型一致的缩放特性，为通过扩大数据和计算资源进一步提升性能提供了理论依据。
- **Tags**: ['generalization', 'descriptive']

## C3: GAIA-1通过自监督训练涌现高层场景理解与泛化能力
- **Statement**: GAIA-1在大规模真实驾驶数据上通过自监督训练后，涌现出包括高层结构与场景动态理解、泛化与创造性、上下文感知与3D几何理解在内的多项能力，并能外推至训练数据中未曾出现的驾驶行为（如超出道路边界行驶）。
- **Status**: empirical
- **Falsification criteria**: 若模型仅能复现训练集中的统计模式而无法泛化至新场景，或对超出分布的动作条件无法产生合理响应，则该声明不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 这些涌现性质表明，足够规模的自回归世界模型可以内化现实世界的生成规则，而非简单地记忆训练样本。
- **Tags**: ['descriptive', 'generalization']

## C4: DINO蒸馏引导图像标记器学习语义表征
- **Statement**: 在图像自编码器训练中加入DINO余弦相似度蒸馏损失，可引导离散词元学习语义化表征（同类物体具有相似嵌入），相较于纯基于VQ-GAN重建的词元表现出更强的语义聚类性质。
- **Status**: empirical
- **Falsification criteria**: 若DINO蒸馏词元在PCA可视化中不显示语义聚类，或去除该损失后世界模型性能无明显下降，则该声明不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 通过DINO蒸馏将语义归纳偏置注入离散词元空间，使世界模型的输入远离高频噪声，降低序列建模难度。
- **Tags**: ['improvement', 'causal']

## C5: Top-k采样在生成真实性与多样性之间取得最佳平衡
- **Statement**: 在世界模型自回归推理中，top-k=50采样策略生成的词元困惑度分布与真实图像词元相近，优于argmax（困惑度过低、生成陷入重复循环）和全分布采样（采样到概率尾部导致出分布问题）。
- **Status**: empirical
- **Falsification criteria**: 若实验中top-k采样的困惑度分布与真实词元存在系统性差异，或其他采样策略生成质量更高，则该声明不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 该策略借鉴了语言模型中的文本退化研究，将其适配至视频词元自回归生成场景，通过限制采样范围防止模型偏离真实分布。
- **Tags**: ['improvement', 'descriptive']
