## 训练输入时间范围
- **Value**: 历史 multi-view camera images over two timesteps
- **Rationale**: 训练时使用两个历史时间步的多视角相机图像，为未来状态预测提供历史上下文。
- **Search range**: 论文未给出可调范围；附录表明输入帧数与 memory queue length 被做过消融。
- **Sensitivity**: 增加输入帧数与 memory queue length 会提升性能，但主要延迟开销来自 historical encoder。
- **Source**: Appendix C.3；Table 9；Sec D.1

## 预测时间范围
- **Value**: future occupancy over two seconds；each timestep corresponding to a 0.5-second interval
- **Rationale**: 训练目标覆盖未来两秒占据预测，并以固定时间间隔形成自回归预测序列。
- **Search range**: 论文主实验还按 nuScenes 的 2s 与 Lyft-Level5 的 0.8s 时间间隔报告结果。
- **Sensitivity**: 较近时间戳对规划更关键，因此论文使用加权的未来 mIoU 指标强调近未来预测。
- **Source**: Appendix C.3；Appendix C.1；Appendix C.2

## 优化器
- **Value**: AdamW
- **Rationale**: 用于训练 Drive-OccWorld 的端到端优化。
- **Search range**: 论文未给出替代优化器范围。
- **Sensitivity**: 论文未对优化器选择做消融。
- **Source**: Appendix C.3

## 初始学习率
- **Value**: 2 × 10 ^ -4
- **Rationale**: 作为 AdamW 的初始学习率。
- **Search range**: 论文未给出学习率搜索范围。
- **Sensitivity**: 论文未报告学习率敏感性。
- **Source**: Appendix C.3

## 学习率调度
- **Value**: cosine annealing scheduler
- **Rationale**: 用于训练过程中的学习率退火。
- **Search range**: 论文未给出替代调度器范围。
- **Sensitivity**: 论文未报告调度器敏感性。
- **Source**: Appendix C.3

## 总体训练目标
- **Value**: 历史归一化、未来预测、轨迹规划端到端联合优化
- **Rationale**: 论文将 normalization loss、forecasting loss 与 planning loss 组合为总损失。
- **Search range**: 训练期包括 L_norm、L_fcst、L_plan；论文未给出各项权重。
- **Sensitivity**: 语义、二值占据与 Lovasz 监督的组合会带来进一步收益；规划损失用于约束安全候选与模仿专家轨迹。
- **Source**: Appendix B；Appendix D.3；Sec 3.4

## 占据预测监督
- **Value**: cross-entropy loss、Lovasz loss、binary occupancy loss
- **Rationale**: 这些损失共同约束未来 occupancy predictions 的语义与几何。
- **Search range**: Table 10 消融了 cross entropy、binary occupancy、Lovasz 的组合。
- **Sensitivity**: 仅使用 cross-entropy 已有可用表现，加入额外监督继续提升，并间接改善 flow forecasting。
- **Source**: Sec 3.2；Appendix B；Table 10

## flow 监督
- **Value**: l1 loss
- **Rationale**: 用于监督历史与未来 3D backward centripetal flow predictions。
- **Search range**: 论文未给出替代 flow loss。
- **Sensitivity**: agent-motion aware normalization 与 flow 质量相关，补偿其他 agents 运动可改善实例关联。
- **Source**: Sec 3.2；Appendix B；Table 6

## 规划训练动作条件
- **Value**: predicted trajectories as action conditions for both training and testing
- **Rationale**: 端到端规划时使用预测轨迹作为动作条件，避免 GT ego actions 泄漏到 planner。
- **Search range**: 论文也报告了 GT trajectory 与 Pred trajectory 的上界对比。
- **Sensitivity**: GT trajectory 的规划指标更好，但 predicted trajectory 对 occupancy 与 flow forecasting 有轻微增益。
- **Source**: Sec 3.4；Table 4
