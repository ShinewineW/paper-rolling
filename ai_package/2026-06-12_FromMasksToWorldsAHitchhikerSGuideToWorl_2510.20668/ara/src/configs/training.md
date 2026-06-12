## mask_reconstruct_generalize
- **Value**: 遮蔽、补全并泛化
- **Rationale**: 论文将 Stage I 的训练范式概括为通过重建缺失或损坏的输入部分来学习，并认为它为后续阶段提供统一的预训练基础。
- **Search range**: 语言、视觉、视频、音频、3D 与结构化数据等模态
- **Sensitivity**: 高；论文把该范式视为通向 unified generation 的起点，但也指出单独的专门模型不能形成整体世界观。
- **Source**: Sec 3

## fixed_ratio_masking
- **Value**: 固定比例随机遮蔽
- **Rationale**: 论文以 BERT 为例说明 MLM 通过随机替换输入 token 并从上下文预测，作为语言遮蔽建模的基础做法。
- **Search range**: 主要作为 Stage I 语言模态的代表性设置
- **Sensitivity**: 中；后续工作用 span masking、denoising autoencoding、replacement detection 与动态遮蔽来改进固定比例方式。
- **Source**: Sec 3.1

## dynamic_masking_and_iterative_denoising
- **Value**: 动态遮蔽、重遮蔽低置信 token、按时间噪声调度迭代去噪
- **Rationale**: 论文把 RoBERTa、Mask-Predict 与 discrete diffusion models 连接成一条从固定遮蔽到动态去噪的训练路线。
- **Search range**: 非自回归语言生成与离散扩散式统一建模
- **Sensitivity**: 高；论文认为动态去噪范式已成熟到可在质量与推理速度上竞争或超过自回归基线。
- **Source**: Sec 3.1

## high_ratio_tube_masking
- **Value**: 高比例 tube masking
- **Rationale**: 论文指出 VideoMAE 与 MaskFeat 表明该训练方式能以数据高效方式学习时空表示。
- **Search range**: 视频表示学习
- **Sensitivity**: 中；论文强调它能捕捉静态场景与动态，但并未把它等同于可交互世界模型。
- **Source**: Sec 3.2

## mixed_chain_of_thought_finetuning
- **Value**: mixed chain-of-thought fine-tuning
- **Rationale**: 论文在 MMaDA 描述中提到该训练策略，用于在统一离散扩散架构中统一推理与生成。
- **Search range**: text 和 image 的统一离散扩散模型
- **Sensitivity**: 中；这是代表性统一模型的训练策略，论文未给出消融或超参细节。
- **Source**: Sec 4.1

## policy_gradient_rl_unigrpo
- **Value**: UniGRPO policy-gradient RL algorithm
- **Rationale**: 论文把 UniGRPO 作为 MMaDA 统一 reasoning 和 generation 的训练算法之一。
- **Search range**: MMaDA 的多模态 reasoning 与 generation 场景
- **Sensitivity**: 中；论文只综述其作用，未提供训练配方、奖励设计或稳定性细节。
- **Source**: Sec 4.1

## mask_based_persistent_memory_training
- **Value**: 论文未给出明确训练配方
- **Rationale**: 论文明确说 mask-based persistent memory 仍 underexplored 且差异很大，因此 Stage IV 采取 architecture-agnostic 视角。
- **Search range**: 持久记忆与一致性建模
- **Sensitivity**: 高；这意味着从遮蔽建模直接扩展到持久世界记忆仍是开放工程问题。
- **Source**: Sec 6
