## 训练流程
- **Value**: Phase 1 先训练 tokenizer 与 world model；Phase 2 加入任务输入并训练 policy、reward、value
- **Rationale**: 先学习视频与动作条件动态，再把任务条件的行为与奖励头接入，最后在 world model 内进行 imagination training。
- **Search range**: 论文给出两阶段流程，未给出替代阶段数。
- **Sensitivity**: 高；流程顺序决定 agent 是否能先保留视频预测能力再进行离线策略改进。
- **Source**: Algorithm 1; Sec 3

## tokenizer 重建损失
- **Value**: MSE 加 0.2 LPIPS
- **Rationale**: 用简单重建目标训练 causal tokenizer，并用 loss normalization 简化两个损失项的加权。
- **Search range**: LPIPS 权重显式为 0.2，未报告扫描范围。
- **Sensitivity**: 中；论文说明 MAE 训练改善 dynamics model 生成视频的空间一致性。
- **Source**: Sec 3.1; Eq 5

## MAE patch dropout
- **Value**: p 从 U(0,0.9) 采样
- **Rationale**: 随机遮蔽输入 patches，让 tokenizer 学到更好的表示，同时包含推理时使用的 p=0 情况。
- **Search range**: 0 到 0.9。
- **Sensitivity**: 中；论文明确称其改善 dynamics model 生成视频的空间一致性。
- **Source**: Sec 3.1

## shortcut forcing 采样步数
- **Value**: K=4；对应 d=1/4
- **Rationale**: 让 dynamics model 每帧只需少量 forward passes，支持交互式生成。
- **Search range**: ablation 从 K=64 的 diffusion forcing baseline 对比到 K=4 的 shortcut forcing。
- **Sensitivity**: 高；更少采样步显著提高速度，但单纯减少步数会损害质量，shortcut model 用来恢复质量。
- **Source**: Sec 3.2; Sec 4.4; Fig 8

## 历史上下文轻微加噪
- **Value**: tau_ctx=0.1
- **Rationale**: 推理时轻微腐蚀过去输入，使模型对自身生成中的小瑕疵更鲁棒。
- **Search range**: 论文只报告 tau_ctx=0.1。
- **Sensitivity**: 中；直接影响长 rollout 时对累积误差的鲁棒性。
- **Source**: Sec 3.2

## MTP 长度
- **Value**: L=8
- **Rationale**: policy 与 reward heads 通过 multi-token prediction 从 task output embeddings 预测未来动作与奖励。
- **Search range**: 论文只报告 L=8。
- **Sensitivity**: 中；影响行为克隆与奖励建模的预测跨度。
- **Source**: Sec 3.3; Eq 9

## TD discount
- **Value**: gamma=0.997
- **Rationale**: value head 用 TD-learning 预测 lambda returns，从而让 policy 能优化超出 imagination horizon 的未来奖励。
- **Search range**: 论文只报告 gamma=0.997。
- **Sensitivity**: 高；长程 Minecraft 任务依赖远期奖励传播。
- **Source**: Sec 3.3; Eq 10

## PMPO 权重
- **Value**: alpha=0.5；beta=0.3
- **Rationale**: alpha 平衡正负 advantage 集合，beta 对 behavioral prior 施加较弱约束。
- **Search range**: 论文称三项缩放在实践中高度鲁棒，未报告具体扫描范围。
- **Sensitivity**: 中；影响 imagined RL 对数据行为空间的偏离程度。
- **Source**: Sec 3.3; Eq 11

## 数据混合
- **Value**: 50% uniform sequences 与 50% relevant sequences
- **Rationale**: 放大任务相关信号；BC loss 只用于 relevant fraction，dynamics loss 只用于 uniform sequences 以避免 optimistic generations。
- **Search range**: 论文只报告 50% 与 50%。
- **Sensitivity**: 高；同时影响 reward、BC 与 world model 训练信号。
- **Source**: Sec 4.1

## 无上下文起始帧训练
- **Value**: batch 中 30% videos 作为 separate images
- **Rationale**: 改善无上下文生成能力，使 dynamics model 学会生成 start frames。
- **Search range**: 论文只报告 30%。
- **Sensitivity**: 中；主要影响无 context 生成与评测场景。
- **Source**: Sec 4
