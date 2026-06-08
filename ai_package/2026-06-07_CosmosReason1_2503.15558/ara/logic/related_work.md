# Related Work

## R1: Shao et al., 2024 (DeepSeekMath)
- **DOI**: arXiv:2402.03300
- **Type**: methodology_adopt
- **Delta**:
  - What changed: 直接采用GRPO作为RL优化算法,利用组内归一化奖励计算优势函数,规避了独立批评模型的训练与维护开销
  - Why: GRPO计算高效且在数学推理领域已验证有效,适合Physical AI推理训练场景
- **Claims affected**: ['C2']
- **Adopted elements**: ['GRPO算法', '组内归一化优势函数']

## R2: DeepSeek-AI, 2025 (DeepSeek-R1)
- **DOI**: arXiv:2501.12948
- **Type**: data_source
- **Delta**:
  - What changed: 使用DeepSeek-R1作为教师模型,从压缩为文字描述的视频内容中提取物理常识与具身推理的长思维链推理迹,作为SFT监督信号;同时借鉴其基于规则可验证奖励的RL训练思路
  - Why: R1具备强大开放式推理能力且无需视觉输入即可从文字描述生成高质量CoT迹,适合蒸馏到VLM;其RL训练方法论已在代码/数学领域验证有效
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['长思维链推理迹蒸馏策略', '基于规则可验证奖励的RL训练范式']

## R3: Liu et al., 2023 (LLaVA)
- **DOI**: NeurIPS 2023
- **Type**: architecture_adopt
- **Delta**:
  - What changed: 采用decoder-only多模态架构,通过视觉编码器+投影层(含PixelShuffle下采样)将视频/图像token对齐到LLM文本嵌入空间后统一处理
  - Why: 相比交叉注意力架构,decoder-only架构在多模态推理任务上表现更强且对所有模态统一处理更简洁
- **Claims affected**: ['C1']
- **Adopted elements**: ['decoder-only多模态架构设计', '视觉token与文本embedding对齐方案']

## R4: Bai et al., 2025 (Qwen2.5-VL)
- **DOI**: arXiv:2502.13923
- **Type**: backbone_adopt
- **Delta**:
  - What changed: 以Qwen2.5-VL作为Cosmos-Reason1-7B的预训练起点,沿用其图像/视频处理方式(动态分辨率、帧采样策略),在其上进行Physical AI SFT和RL
  - Why: Qwen2.5-VL提供强大的视觉语言预训练基础,有助于降低从头训练的成本并提供良好的初始能力
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['Qwen2.5-VL预训练权重', '动态分辨率图像/视频处理流程']

## R5: NVIDIA, 2025 (Nemotron-H)
- **DOI**: arXiv:2504.03624
- **Type**: backbone_adopt
- **Delta**:
  - What changed: 以Nemotron-H作为Cosmos-Reason1-56B的LLM backbone,搭配InternViT-300M-V2.5视觉编码器,使用混合Mamba-MLP-Transformer架构处理长序列
  - Why: 混合Mamba-MLP-Transformer在保持长序列建模能力的同时降低计算复杂度,优于纯Transformer的二次复杂度
- **Claims affected**: ['C1']
- **Adopted elements**: ['Nemotron-H混合架构预训练权重', 'Mamba-MLP-Transformer混合骨干设计']

## R6: Zawalski et al., 2024 (ECoT)
- **DOI**: CoRL 2024
- **Type**: data_source
- **Delta**:
  - What changed: 在BridgeData V2字幕生成阶段,将ECoT提供的检测物体和动作序列标注信息注入VLM字幕提示,以提升结构化字幕质量从而改善SFT数据
  - Why: ECoT提供的动作原语标注信息有助于生成更准确反映机器人操作细节的视频字幕,提升推理迹提取质量
- **Claims affected**: ['C1']
- **Adopted elements**: ['BridgeData V2字幕增强中的物体检测与动作序列辅助标注']
