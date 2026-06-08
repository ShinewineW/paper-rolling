# Related Work

## R1: Zhang et al., 2023
- **DOI**: ICCV 2023
- **Type**: 方法基础
- **Delta**:
  - What changed: 原始ControlNet针对UNet架构设计；Cosmos-Transfer1将其扩展至DiT架构，并引入多分支多模态控制和时空控制图，且采用推理时多分支融合而非联合训练
  - Why: ControlNet提供了通过添加可训练编码器分支（零初始化线性层）扩展预训练扩散模型的核心范式，Cosmos-Transfer1沿用该范式并推广至视频世界模型
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['零初始化线性层设计', '冻结基础模型权重仅训练控制分支的训练策略', '条件编码器分支继承基础模型权重初始化']

## R2: Chen et al., 2024
- **DOI**: arXiv:2401.05252
- **Type**: 直接前驱
- **Delta**:
  - What changed: Chen et al.将ControlNet从UNet扩展至Transformer（DiT）架构；Cosmos-Transfer1进一步扩展至多模态视频世界生成，引入多分支并行设计与时空自适应权重，并专注于Physical AI应用
  - Why: 提供了DiT-based ControlNet的直接架构参考，验证了ControlNet范式在Transformer架构上的可行性
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['DiT架构ControlNet控制分支设计', '控制块输出经线性层注入主分支的连接方式']

## R3: NVIDIA, 2025
- **DOI**: arXiv:2501.03575
- **Type**: 基础模型
- **Delta**:
  - What changed: Cosmos-Predict1提供预训练的DiT世界基础模型；Cosmos-Transfer1在其基础上进行后训练（post-training），添加多模态控制分支，扩展其条件生成能力
  - Why: 提供视频生成的基础能力与预训练权重，Cosmos-Transfer1所有控制分支均继承其权重初始化，高质量微调数据集也沿用自该平台
- **Claims affected**: ['C1', 'C3', 'C4']
- **Adopted elements**: ['Cosmos-Predict1-7B-Video2World基础模型架构与权重', '高质量微调数据集', '56K token视频生成配置（5秒1280x704p 24fps）']

## R4: Yang et al., 2024
- **DOI**: arXiv:2406.09414
- **Type**: 工具/预处理模块
- **Delta**:
  - What changed: DepthAnything V2直接作为深度图提取工具用于训练数据制备和评估阶段，Cosmos-Transfer1未对其做修改
  - Why: 提供高质量单目深度估计，无需额外传感器即可获得几何控制信号；同时用于评估中计算Depth si-RMSE
- **Claims affected**: ['C5']
- **Adopted elements**: ['深度图提取流程（归一化至[0,1]）', '深度对齐评估中的DepthAnythingV2推理']

## R5: Ho et al., 2021
- **DOI**: ICRA 2021
- **Type**: 对比/背景方法
- **Delta**:
  - What changed: RetinaGAN使用无监督GAN增强仿真场景真实感；Cosmos-Transfer1使用扩散模型+多模态条件控制替代GAN，在保持结构的同时提供更高多样性和质量，且不需要强化学习辅助信号
  - Why: 代表了早期Sim2Real视觉增强的GAN路线，作为扩散模型方法的对照背景
- **Claims affected**: ['C6']
- **Adopted elements**: []

## R6: Zhao et al., 2024
- **DOI**: IEEE IV 2024
- **Type**: 相关方法
- **Delta**:
  - What changed: Zhao et al.使用扩散模型+ControlNet进行Sim2Real驾驶图像生成；Cosmos-Transfer1将该思路扩展至多模态视频世界生成，并引入自适应时空控制权重和多种Physical AI场景
  - Why: 验证了扩散+ControlNet路线在Sim2Real驾驶场景中优于GAN方法，为Cosmos-Transfer1的方法选择提供背景支持
- **Claims affected**: ['C6', 'C7']
- **Adopted elements**: []
