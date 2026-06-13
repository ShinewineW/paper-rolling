## 训练数据规模
- **Value**: 1,000 rounds, approximately 7 hours or 1.2 million frames
- **Rationale**: 用于让世界模型从 Tekken 3 观测视频中学习多智能体动态，并在只条件化 Player 1 输入时隐式捕捉 Player 2 行为。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 数据覆盖不足会削弱角色动作、回合节奏和反应行为的学习；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.2, Sec 4.1

## 输入帧分辨率
- **Value**: 3 × 448 × 736
- **Rationale**: 数据集中每帧以该分辨率采集，并作为 DCAE 压缩前的原始视觉输入。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 分辨率影响视觉细节与计算成本；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.2, Sec 4.1

## 标注模态
- **Value**: Player 1 和 Player 2 动作输入、health and timer status、68-point body pose coordinates、player segmentation masks
- **Rationale**: 同步标注支持动作条件、行为评估和姿态增强表征。
- **Search range**: 论文未给出替代标注配置。
- **Sensitivity**: 缺少姿态或游戏状态标注会限制姿态增强模型和基于 health 的评估；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.2

## Autoencoder Training 步数
- **Value**: 68,000 steps
- **Rationale**: 先训练 340M parameter DCAE 获得紧凑 latent representation，再供世界模型训练使用。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 训练不足可能导致重建质量下降并传递到世界模型；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## Autoencoder Training 时长
- **Value**: approx. 75 hours
- **Rationale**: 论文报告 DCAE 在 Tekken dataset 上训练到该时长。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 该值主要反映训练成本，不足以单独推断质量敏感性；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## DCAE 训练目标
- **Value**: L2 reconstruction loss、perceptual similarity loss、KL divergence term
- **Rationale**: 用重建、感知相似性和 latent regularization 共同训练 compact latent representation。
- **Search range**: 论文未给出权重或替代目标搜索范围。
- **Sensitivity**: 各项权重未披露，因此只能判断这些项共同约束重建质量和 latent 空间规则性；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## World Model Training 序列长度
- **Value**: 128 frames
- **Rationale**: DiT 在视频片段上训练，用 128-frame 序列预测下一个 latent frame，并结合局部与全局 temporal dependency。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 较短上下文可能削弱长期战术依赖，较长上下文会增加计算成本；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## 条件信号
- **Value**: Player 1 actions
- **Rationale**: 世界模型以 Player 1 动作作为条件，Player 2 action labels 不作为监督输入，从而检验隐式行为学习。
- **Search range**: 论文对比传统 imitation learning，但未给出条件信号消融范围。
- **Sensitivity**: 若加入 Player 2 动作监督，研究问题会从部分观测行为涌现转向更接近完整动作监督；该判断为分析推断,论文未显式声明。
- **Source**: Sec 3.1, Sec 4.1

## Step Distillation 步数
- **Value**: 2,500 steps
- **Rationale**: 使用 CausVid DMD 将 fully-trained DiT 蒸馏为 4-step variant，并在该步数收敛。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 蒸馏不足可能影响实时模型保真度，过度蒸馏的影响论文未报告；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## Step Distillation 目标
- **Value**: DMD loss 和 critic loss
- **Rationale**: 用于减少 world model 推理所需步数并保留生成质量。
- **Search range**: 论文未给出损失权重或替代目标搜索范围。
- **Sensitivity**: 损失权重和 critic 设计可能影响质量与速度折中；该判断为分析推断,论文未显式声明。
- **Source**: Sec 4.1

## 优化器
- **Value**: Muon optimizer
- **Rationale**: 论文称采用 Muon optimization 来提升 large-scale diffusion transformers 的训练效率。
- **Search range**: 论文提到相对 AdamW 的训练速度背景，但未给出本文优化器消融。
- **Sensitivity**: 优化器会影响大模型训练效率和稳定性；该判断为分析推断,论文未显式声明。
- **Source**: Sec 2.4
