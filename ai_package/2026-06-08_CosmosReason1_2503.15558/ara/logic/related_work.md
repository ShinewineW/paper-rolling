# Related Work

## R1: DeepSeek-AI, 2025
- **DOI**: 
- **Type**: foundational
- **Delta**:
  - What changed: Cosmos-Reason1 将 DeepSeek-R1 的蒸馏方法迁移至物理 AI 领域：从 DeepSeek-R1 提取长链式思维推理轨迹用于 SFT 数据标注，并沿用其基于规则可验证奖励的 RL 训练范式
  - Why: DeepSeek-R1 开源了面向数学和编程任务的高性能推理训练方法论，为构建 Physical AI 推理模型提供了直接的技术参照和数据蒸馏工具
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['DeepSeek-R1 推理轨迹蒸馏（用于物理常识和具身推理 SFT）', '基于规则可验证奖励的 RL 框架']

## R2: Shao et al., 2024
- **DOI**: 
- **Type**: methodological
- **Delta**:
  - What changed: 直接采用 GRPO 算法作为 RL 优化方法，无需额外训练独立 critic 模型；优势函数由同组响应的奖励均值/标准差归一化得到
  - Why: GRPO 以简洁性和计算效率见长（省去 critic 训练开销），适合大规模多模态 RL 训练场景
- **Claims affected**: ['C2']
- **Adopted elements**: ['GRPO 算法', '组内奖励归一化优势函数计算']

## R3: Bai et al., 2025 (Qwen2.5-VL)
- **DOI**: 
- **Type**: backbone
- **Delta**:
  - What changed: Cosmos-Reason1-7B 以 Qwen2.5-VL 为预训练起点，沿用其图像和视频处理方式，再经 Physical AI SFT 和 RL 两阶段后训练
  - Why: Qwen2.5-VL 提供高质量的视觉-语言预训练基础，是 7B 规模模型的骨干选择
- **Claims affected**: ['C1']
- **Adopted elements**: ['Qwen2.5-VL 预训练权重', '图像/视频处理流程']

## R4: NVIDIA, 2025 (Nemotron-H); Waleffe et al., 2024
- **DOI**: 
- **Type**: backbone
- **Delta**:
  - What changed: Cosmos-Reason1-56B 使用混合 Mamba-MLP-Transformer 预训练模型（Nemotron-H）作为 LLM 骨干，结合 InternViT-300M-V2.5 视觉编码器构成 56B 多模态架构
  - Why: 混合 Mamba-MLP-Transformer 架构在处理长序列时具有线性时间复杂度，相比纯 Transformer 在视频多帧推理场景下效率更高；少量 Transformer 层保留了对长上下文细节的精确建模能力
- **Claims affected**: ['C1', 'C6']
- **Adopted elements**: ['Nemotron-H 混合 Mamba-MLP-Transformer 骨干权重', '混合架构设计（线性状态空间 + 少量自注意力层）']

## R5: Liu et al., 2023 (LLaVA); Dai et al., 2024 (NVLM)
- **DOI**: 
- **Type**: architectural
- **Delta**:
  - What changed: Cosmos-Reason1 采用 decoder-only 多模态架构（与 LLaVA、NVLM-D 类似），将视频帧通过视觉编码器和两层 MLP projector（含 PixelShuffle 下采样）映射至文本 token 嵌入空间后输入 LLM 骨干
  - Why: Dai et al. (2024) 的对比实验表明，decoder-only 架构在视觉上下文中的多学科知识和数学推理任务上比交叉注意力架构推理能力更强
- **Claims affected**: ['C1']
- **Adopted elements**: ['decoder-only 多模态统一输入架构', '两层 MLP projector + PixelShuffle 下采样']

## R6: Zawalski et al., 2024 (ECoT)
- **DOI**: 
- **Type**: related
- **Delta**:
  - What changed: Cosmos-Reason1 在具身推理 SFT 数据标注中，将 ECoT 提供的动作序列标注作为 BridgeData V2 captioning prompt 的补充信息；在 related work 中将 ECoT 视为具身链式思维框架的代表性工作
  - Why: ECoT 展示了通过显式链式推理提升机器人决策能力的可行性，是具身 CoT 推理范式的直接先验
- **Claims affected**: ['C1']
- **Adopted elements**: ['ECoT 动作序列标注（用于辅助 BridgeData V2 视频标注）']

## R7: Walke et al., 2023 (BridgeData V2); Sermanet et al., 2024 (RoboVQA); AgiBot, 2024; Wang et al., 2023 (HoloAssist)
- **DOI**: 
- **Type**: dataset
- **Delta**:
  - What changed: 将上述机器人操作和具身推理数据集重新处理为 Physical AI SFT 和 RL 所需的 MCQ 格式：通过 VLM captioning + DeepSeek-R1 推理轨迹提取 + 规则清洗流程生成训练样本
  - Why: 这些数据集覆盖多样化的具身推理场景（机器人臂、人类、自动驾驶车辆等），是构建通用具身推理能力的基础数据来源
- **Claims affected**: ['C1']
- **Adopted elements**: ['BridgeData V2（60,096 轨迹，13 种技能，24 种环境）', 'RoboVQA（约 220K 片段，6 种问题类型）', 'AgiBot World（3,300 视频，36 项任务）', 'HoloAssist（166 小时以自我为中心的视频，1,758 段）']
