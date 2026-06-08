# Related Work

## R1: Shao et al., 2024 (DeepSeekMath)
- **DOI**: arXiv:2402.03300
- **Type**: method
- **Delta**:
  - What changed: 采用GRPO作为RL优化算法，利用组内响应归一化计算优势函数，无需维护独立的Critic模型；公式为 $$A_i = \frac{R(o_i) - \text{mean}(\mathcal{G})}{\text{std}(\mathcal{G})}$$
  - Why: GRPO无需Critic模型，计算简洁高效，适合Physical AI这类需要大规模视频多模态RL训练的场景
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['GRPO算法整体框架', '基于组内均值与标准差归一化的优势函数计算方式']

## R2: DeepSeek-AI, 2025 (DeepSeek-R1)
- **DOI**: arXiv:2501.12948
- **Type**: dataset_and_method
- **Delta**:
  - What changed: 将DeepSeek-R1用作数据蒸馏工具，从视频文字描述中提取长链式推理轨迹以生成Physical AI SFT数据；同时借鉴其规则化可验证奖励的RL训练范式
  - Why: DeepSeek-R1具备强大的文本推理能力，可将视觉信息压缩到文本后生成高质量推理轨迹，解决了大规模带思维链SFT数据稀缺的问题
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['DeepSeek-R1用于物理常识推理轨迹提取（Sec. 5.1.1）', 'DeepSeek-R1用于具身推理轨迹提取（Sec. 5.1.2）', '规则化可验证奖励的RL训练设计理念']

## R3: Bai et al., 2025 (Qwen2.5-VL)
- **DOI**: arXiv:2502.13923
- **Type**: pretrained_model
- **Delta**:
  - What changed: 以Qwen2.5-VL作为Cosmos-Reason1-7B的预训练骨干，沿用其图像和视频处理流程（包括动态分辨率调整和视频帧采样策略）
  - Why: Qwen2.5-VL提供了高质量视觉-语言预训练基础，可通过Physical AI专项SFT和RL进一步专门化为物理AI推理模型
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['Qwen2.5-VL作为7B模型骨干（预训练权重+架构）', 'Qwen2.5-VL的图像和视频处理流程']

## R4: Waleffe et al., 2024; NVIDIA, 2025 (Nemotron-H)
- **DOI**: arXiv:2406.07887; arXiv:2504.03624
- **Type**: architecture_and_pretrained_model
- **Delta**:
  - What changed: 采用混合Mamba-MLP-Transformer架构（Nemotron-H）作为Cosmos-Reason1-56B的LLM骨干，结合InternViT-300M-V2.5视觉编码器构建56B多模态模型
  - Why: 混合架构在线性时间复杂度长序列处理（Mamba部分）与全局长文本建模（Transformer层）之间取得平衡，适合视频输入的长上下文建模，同时降低推理计算开销
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['Mamba-MLP-Transformer混合架构设计用于56B模型LLM骨干', 'Nemotron-H预训练权重作为56B模型初始化', 'TP=8、PP=2并行策略用于56B模型训练']

## R5: Liu et al., 2023 (LLaVA); Dai et al., 2024 (NVLM-D)
- **DOI**: NeurIPS 2023; arXiv:2409.11402
- **Type**: architecture
- **Delta**:
  - What changed: 采用Decoder-only多模态架构，将视觉编码器输出通过含PixelShuffle降采样的2层MLP投影器对齐到文本token空间，遵循LLaVA和NVLM-D的设计路线
  - Why: NVLM研究表明Decoder-only架构在大学水平多学科知识和数学推理任务上优于Cross-attention架构，且对所有模态统一处理更简洁，利于推理能力的发展
- **Claims affected**: ['C1']
- **Adopted elements**: ['Decoder-only多模态架构整体设计', '2层MLP投影器含PixelShuffle（2×2）降采样', 'NVLM-D的图像分块（tile）处理策略用于56B模型（动态分辨率1-12个448×448 tile）']

## R6: Hu et al., 2024 (OpenRLHF); Sheng et al., 2024 (HybridFlow)
- **DOI**: arXiv:2405.11143; arXiv:2409.19256
- **Type**: baseline_system
- **Delta**:
  - What changed: 与这两个主流同位RL训练框架对比，指出其因同步开销导致资源利用率低，并提出全异步异构部署框架加以解决
  - Why: 同位框架的策略训练与Rollout之间的同步等待是训练效率的主要瓶颈，异步框架通过两者分离实现约160%的效率提升
- **Claims affected**: ['C3']
- **Adopted elements**: []

## R7: Chen et al., 2024 (InternVL2.5 / InternViT)
- **DOI**: arXiv:2412.05271
- **Type**: pretrained_model
- **Delta**:
  - What changed: 采用InternViT-300M-V2.5作为Cosmos-Reason1-56B的视觉编码器，处理448×448分辨率输入，每帧生成1024个视觉token后经PixelShuffle降采样至256个token
  - Why: InternViT-300M-V2.5是高质量开源视觉编码器，适合高分辨率视频帧处理，与Nemotron-H骨干组合构建高效的56B多模态模型
- **Claims affected**: ['C1']
- **Adopted elements**: ['InternViT-300M-V2.5视觉编码器（24层，模型维度1024）']
