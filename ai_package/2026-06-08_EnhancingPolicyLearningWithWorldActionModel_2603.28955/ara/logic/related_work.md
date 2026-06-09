# Related Work

## R1: Hafner et al. 2022 [4] / Okada & Taniguchi 2022 [17]
- **DOI**: ICLR 2022（DreamerV2）; IROS 2022（DreamingV2）
- **Type**: baseline
- **Delta**:
  - What changed: WAM 在 DreamerV2 的 RSSM 骨干基础上增加逆动力学头，将训练目标从纯观测重建（仅 KL + 重建损失）扩展为同时预测动作和未来观测（增加 L_action 项）。
  - Why: DreamerV2 的潜表示仅针对像素重建和 KL 正则化优化，未被显式引导编码动作相关结构，导致下游策略使用的 f_t 特征缺乏动作感知信息。
- **Claims affected**: ['C1', 'C2', 'C4']
- **Adopted elements**: ['RSSM 架构（确定性循环状态 h_t 与随机范畴分布变量 z_t 的组合）', '双流 CNN 编码器处理静态相机与夹爪相机图像，融合本体感受状态', '32×32 范畴潜变量表示方案', 'KL 正则化（后验对先验）的训练目标结构']

## R2: Chandra et al. 2025 [8]
- **DOI**: CoRL 2025
- **Type**: baseline
- **Delta**:
  - What changed: WAM 使用与 DiWA 完全相同的策略架构（DiffusionMLP）和两阶段训练流程（BC 预训练→DPPO 精调），仅将世界模型替换为 WAM，以隔离世界模型表示质量的单一变量影响。
  - Why: DiWA 已验证「在冻结世界模型潜空间内精调扩散策略」这一范式的有效性，WAM 在其基础上探索更强的世界模型表示能否进一步提升策略性能，保持流程一致性确保对比的公平性。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['BC→DPPO 两阶段训练流程', 'DiffusionMLP 策略架构（K 步去噪生成动作块）', '对比奖励分类器的训练与评估完整流程', 'CALVIN 实验评估协议（29 个保留初始配置）']

## R3: Pathak et al. 2017 [11]
- **DOI**: ICML 2017
- **Type**: inspiration
- **Delta**:
  - What changed: WAM 将自监督逆动力学建模思想引入世界模型训练目标，在编码器嵌入层预测状态转移动作，而非用于好奇心驱动的探索场景。
  - Why: 逆动力学建模可迫使表示聚焦于环境的可控方面，过滤任务无关干扰，论文认为此性质有助于提升世界模型特征对下游控制策略的有效性。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['从连续帧编码器嵌入预测动作的逆动力学基本思想']

## R4: Cen et al. 2025 [10]
- **DOI**: arXiv:2506.21539
- **Type**: contrast
- **Delta**:
  - What changed: 相比 WorldVLA 通过自回归大型基础模型架构统一生成动作与图像的做法，WAM 仅在现有 DreamerV2 上添加轻量逆动力学头，属于「最小化扩展现有架构」而非「重新设计架构」的路线。
  - Why: 论文将 WAM 定位为与统一动作世界模型「不同且互补」的方案，强调无需大型基础模型即可改善现有世界模型的表示质量。
- **Claims affected**: ['C4']
- **Adopted elements**: []

## R5: Ren et al. 2024 [16]
- **DOI**: arXiv:2409.00588
- **Type**: adopted
- **Delta**:
  - What changed: WAM 直接采用 DPPO 算法在冻结世界模型潜空间中进行扩散策略精调，沿用其裁剪 PPO 替代目标和 BC 正则化设计，未作修改。
  - Why: DPPO 已被 DiWA 验证为在世界模型潜空间中精调扩散策略的有效算法，WAM 直接复用以聚焦于世界模型表示本身对策略性能的影响。
- **Claims affected**: ['C3']
- **Adopted elements**: ['DPPO 算法（裁剪 PPO 代理目标）', '推理期 10 步去噪配合 BC 正则化（α_BC）防止遗忘', '每轮 50 条并行想象 rollout 的训练设置']
