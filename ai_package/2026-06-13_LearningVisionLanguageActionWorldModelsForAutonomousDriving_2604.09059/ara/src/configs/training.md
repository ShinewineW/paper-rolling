## 三阶段训练流程
- **Value**: visual pretraining -> supervised fine-tuning -> reinforcement learning with GRPO
- **Rationale**: 先激活视觉生成能力，再用多任务混合数据注入驾驶概念知识，最后通过与生成未来交互的强化学习细化决策。
- **Search range**: 论文只报告这一条主流程，并在消融中移除 P.T.、SFT、RL 做对照。
- **Sensitivity**: 高；论文指出完整 VLA-World 最优，SFT 对结构化多步推理的冷启动尤其关键，RL 在 SFT 之后进一步细化策略。
- **Source**: Fig 1; Sec 3; Sec 4.3; Supp B.2

## 预训练数据规模
- **Value**: ≈500k
- **Rationale**: 用于视觉生成预训练，输入当前 multi-view observations、egocentric coordinate system 和 physical units，目标是自回归预测未来帧 discrete visual tokens。
- **Search range**: 论文未报告其他预训练数据规模。
- **Sensitivity**: 中；预训练增强驾驶环境的时空理解，移除 P.T. 会降低规划表现。
- **Source**: Supp B.1; Table 4

## SFT/RL 数据规模
- **Value**: ≈20k / 20K samples
- **Rationale**: nuScenes-GR-20K 面向 future frames generation 和 conditioned reasoning，服务于 SFT 与 RL 阶段。
- **Search range**: 论文只报告 nuScenes-GR-20K 这一规模。
- **Sensitivity**: 高；移除 mixed data 会造成明显退化，说明多任务监督信号是关键。
- **Source**: Sec 4.1; Supp B.1; Table 7

## 预训练轮数
- **Value**: 30 epochs
- **Rationale**: 预训练阶段用 AdamW 训练以激活视觉生成和时空先验。
- **Search range**: 论文未报告预训练 epoch 搜索范围。
- **Sensitivity**: 未做单独轮数敏感性；其阶段贡献由 w/o. P.T. 消融体现。
- **Source**: Sec 4.1; Supp B.2

## 预训练学习率
- **Value**: $5 \times 1 0 ^ { - 4 }$
- **Rationale**: 作为预训练阶段 AdamW 的 initial learning rate。
- **Search range**: 论文未报告学习率搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp B.2

## 预训练 per-device batch size
- **Value**: 16
- **Rationale**: 与 AdamW 和 30 epochs 共同定义预训练批量配置。
- **Search range**: 论文未报告 batch size 搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp B.2

## SFT 轮数
- **Value**: 12 epochs
- **Rationale**: SFT 用 imitation learning 在多任务混合数据上注入 perception、prediction、visual、think、action、answer 的概念链条。
- **Search range**: 论文未报告 SFT epoch 搜索范围。
- **Sensitivity**: 高；w/o. SFT 表明缺少冷启动监督会难以探索结构化多步推理空间。
- **Source**: Sec 3.4; Sec 4.1; Sec 4.3; Supp B.2

## SFT 学习率
- **Value**: $1 \times 1 0 ^ { - 4 }$
- **Rationale**: 作为 supervised fine-tuning 阶段 AdamW 的 initial learning rate。
- **Search range**: 论文未报告学习率搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp B.2

## RL 优化轮数
- **Value**: one epoch
- **Rationale**: 从 SFT checkpoint 出发，进一步用 GRPO 优化策略。
- **Search range**: 论文未报告 RL epoch 搜索范围。
- **Sensitivity**: 中到高；RL 作为完整流程最后阶段可直接优化规划，但没有 SFT 冷启动时效果受限。
- **Source**: Sec 4.1; Sec 4.3; Supp B.2

## RL 学习率
- **Value**: $1 \times 1 0 ^ { - 6 }$
- **Rationale**: 用于 GRPO policy training。
- **Search range**: 论文未报告学习率搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp B.2

## RL global batch size
- **Value**: 16
- **Rationale**: 用于 GRPO 阶段的 policy training。
- **Search range**: 论文未报告 batch size 搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp B.2

## 每个 prompt 的候选响应数
- **Value**: 8
- **Rationale**: GRPO 为每个 prompt 采样候选响应来估计 policy gradient。
- **Search range**: 论文未报告候选数搜索范围；方法部分以 G 泛化描述。
- **Sensitivity**: 论文未单独报告。
- **Source**: Sec 4.1; Supp A.1; Supp B.2

## KL 正则系数
- **Value**: $1 \times 1 0 ^ { - 2 }$
- **Rationale**: 用于保留 SFT 学到的行为并稳定优化，防止策略偏离参考模型过多。
- **Search range**: 论文未报告 KL 系数搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Supp B.2

## 学习率调度
- **Value**: cosine learning rate scheduler with warm-up ratio of 0.1
- **Rationale**: 用于所有训练阶段以稳定早期优化。
- **Search range**: 论文未报告 scheduler 或 warm-up 搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Supp B.2

## gradient accumulation step
- **Value**: 2
- **Rationale**: 与 multi-view 输入和最大像素配置共同控制训练显存与有效批量。
- **Search range**: 论文未报告搜索范围。
- **Sensitivity**: 论文未单独报告。
- **Source**: Supp B.2

## RL 奖励集合
- **Value**: $R _ { \mathrm { f m t } }$, $R _ { \mathrm { p r e d } }$, $R _ { \mathrm { v i s } }$, $R _ { \mathrm { a c t } }$, $R _ { \mathrm { t r a j } }$
- **Rationale**: 分别约束输出格式、短期预测、视觉 token 可解码性、高层 action 和三秒轨迹。
- **Search range**: 论文在消融中分别移除 $R _ { \mathrm { p r e d } }$、$R _ { \mathrm { v i s } }$、$R _ { \mathrm { a c t } }$、$R _ { \mathrm { t r a j } }$。
- **Sensitivity**: 高；不同 reward 均有正向作用，trajectory 和 action rewards 贡献最大。
- **Source**: Sec 3.5; Sec 4.3; Table 4
