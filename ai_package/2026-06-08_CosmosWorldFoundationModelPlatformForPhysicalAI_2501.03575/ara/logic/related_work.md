# Related Work

## R1: Ha and Schmidhuber, 2018
- **DOI**: 
- **Type**: 概念先驱
- **Delta**:
  - What changed: Cosmos将世界模型从低维潜空间循环神经网络扩展到视觉观测空间的大规模基础模型，引入「预训练→后训练」范式支持多物理AI任务
  - Why: Ha和Schmidhuber 2018年工作提出用神经网络学习世界模型以预测未来状态的基本思路，是世界模型概念的奠基文献
- **Claims affected**: ['C1']
- **Adopted elements**: ['世界模型作为物理AI数字孪生的核心概念']

## R2: Karras et al., 2022, 2024 (EDM)
- **DOI**: 
- **Type**: 方法基础
- **Delta**:
  - What changed: Cosmos在EDM框架基础上引入多任务学习的连续不确定性加权函数u(σ)，用于平衡不同噪声级别的损失贡献，并增加了混合精度训练和渐进式训练课程
  - Why: EDM提供了严格的去噪得分匹配训练目标、预条件化设计和噪声级别对数正态分布采样，是Cosmos扩散型WFM训练损失的直接理论基础
- **Claims affected**: ['C3']
- **Adopted elements**: ['去噪得分匹配损失（公式5）', 'EDM预条件化参数化', '噪声级别对数正态采样（公式8）']

## R3: Peebles and Xie, 2023 (DiT)
- **DOI**: 
- **Type**: 架构基础
- **Delta**:
  - What changed: Cosmos在DiT基础上引入3D因子化FPS感知RoPE、AdaLN-LoRA参数精简（从11B减少至7B）、QK归一化、跨注意力文本条件化和3D分块化，使其适用于可控长视频生成
  - Why: DiT将扩散模型与Transformer架构结合，提供了可扩展的去噪网络设计，是Cosmos扩散型WFM网络骨干的直接基础
- **Claims affected**: ['C3']
- **Adopted elements**: ['自适应层归一化（AdaLN）', 'Transformer去噪骨干架构']

## R4: Blattmann et al., 2023 (VideoLDM)
- **DOI**: 
- **Type**: 基线方法
- **Delta**:
  - What changed: Cosmos扩散型WFM通过大规模预训练、改进的tokenizer和后训练微调策略，在3D一致性、视频质量和多下游任务上显著超越VideoLDM
  - Why: VideoLDM是视频潜在扩散模型的代表性基线，在3D一致性评估、机器人操控和自动驾驶后训练实验中均作为对比基准
- **Claims affected**: ['C3', 'C5', 'C6']
- **Adopted elements**: []

## R5: Cai et al., 2024 (Medusa)
- **DOI**: 
- **Type**: 推理优化方法
- **Delta**:
  - What changed: Cosmos将Medusa框架适配到视频自回归WFM：合并多Medusa头权重矩阵以最大化并行性，通过消融确定最优头数（9个）和最优微调策略（仅解冻最后两个transformer层），不使用Medusa原版的树形注意力机制
  - Why: Medusa通过在骨干网络后添加多个并行解码头实现投机解码，可显著减少自回归生成的前向传播次数
- **Claims affected**: ['C8']
- **Adopted elements**: ['多头投机解码框架', '拒绝采样验证机制']

## R6: Abbas et al., 2023 (SemDeDup)
- **DOI**: 
- **Type**: 数据处理方法
- **Delta**:
  - What changed: Cosmos复用InternVideo2嵌入，结合GPU加速K-means聚类（k=10,000）和块内对角距离矩阵计算，将SemDeDup扩展到约2000万小时量级的大规模视频数据语义去重
  - Why: SemDeDup提出基于语义嵌入的数据去重方法，适合在保留多样性的同时删除冗余样本
- **Claims affected**: ['C7']
- **Adopted elements**: ['语义嵌入去重策略', 'K-means聚类识别重复样本的流程']

## R7: Mentzer et al., 2023 (FSQ)
- **DOI**: 
- **Type**: 量化方法
- **Delta**:
  - What changed: Cosmos使用FSQ设计离散tokenizer，采用(8,8,8,5,5,5)六维量化级别（词汇表64,000），无需VQ-VAE的承诺损失（commitment loss），简化了大规模视频tokenizer训练
  - Why: FSQ通过对连续隐变量每维独立进行有限级量化，避免了VQ代码本坍塌问题，适合大规模视频tokenizer
- **Claims affected**: ['C2']
- **Adopted elements**: ['有限标量量化（FSQ）量化器设计']

## R8: Xu et al., 2024 (CamCo)
- **DOI**: 
- **Type**: 基线方法
- **Delta**:
  - What changed: Cosmos相机控制模型在相同训练集下，相机位姿估计成功率、轨迹对齐精度和FID/FVD上均显著优于CamCo，且在训练→测试分布偏移下具有更强泛化能力
  - Why: CamCo是相机可控视频生成的代表性方法，在相同数据集（DL3DV-10K）上的公平对比是验证Cosmos相机控制能力的关键基线
- **Claims affected**: ['C4']
- **Adopted elements**: []
