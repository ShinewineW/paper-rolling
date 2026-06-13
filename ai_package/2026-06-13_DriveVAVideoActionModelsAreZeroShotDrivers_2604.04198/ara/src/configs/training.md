## 预训练骨干
- **Value**: Wan2.2-TI2V-5B
- **Rationale**: 作者将大规模视频生成模型作为迁移起点，用其视频先验适配驾驶域视频续写与动作 grounding。
- **Search range**: 论文只报告 Wan2.2-TI2V-5B 作为主设置；消融包含 From Scratch、LoRA Fine-tune、Full Fine-tune。
- **Sensitivity**: 高；从头训练和 LoRA Fine-tune 均明显弱于 Full Fine-tune，说明有效迁移需要端到端适配视频先验。
- **Source**: Sec 5.2; Sec 5.7; Table 7

## 训练样本帧构成
- **Value**: 4 history frames + 8 future frames at 2 FPS
- **Rationale**: 用历史观测作为条件，并监督短窗口未来视频与轨迹，使滚动规划转化为连续的视频续写问题。
- **Search range**: 未来视频帧数消融为 4、8、12；历史帧数未报告其他设置。
- **Sensitivity**: 高；论文称 8 frames 最好，4 frames 覆盖不足，12 frames 会积累漂移并损害 video–trajectory consistency。
- **Source**: Sec 5.2; Sec 5.7; Table 6

## 输入分辨率
- **Value**: $8 3 2 \times 4 8 0$
- **Rationale**: 训练样本以该分辨率构造视频帧，进入 Wan2.2-TI2V-5B 的 3D-causal VAE 编码流程。
- **Search range**: 论文未报告其他分辨率。
- **Sensitivity**: 论文未给出分辨率消融；影响为分析推断,论文未显式声明。
- **Source**: Sec 5.2

## 优化器
- **Value**: AdamW
- **Rationale**: 用于分布式 bf16 mixed-precision 训练下的全量微调。
- **Search range**: 论文未报告其他优化器。
- **Sensitivity**: 论文未给出优化器消融。
- **Source**: Sec 5.2

## 学习率与权重衰减
- **Value**: learning rate $1 0 ^ { - 4 }$; weight decay 0.01
- **Rationale**: 作为主训练设置，配合 warm-up 后常数学习率计划。
- **Search range**: warm-up 从 $1 0 ^ { - 3 }$ of the base learning rate 开始；论文未报告其他学习率或权重衰减。
- **Sensitivity**: 论文未给出学习率或权重衰减消融。
- **Source**: Sec 5.2

## 训练阶段与 batch size
- **Value**: batch size 80 for 20k steps, then another 10k steps with effective batch size 640 via gradient accumulation
- **Rationale**: 先用较小 batch 快速收敛，再用梯度累积扩大有效 batch 继续微调。
- **Search range**: 论文只报告这两个阶段。
- **Sensitivity**: 论文未给出步数或 batch size 消融。
- **Source**: Sec 5.2

## 学习率计划
- **Value**: linear warm-up over first 1k steps, followed by constant learning rate schedule
- **Rationale**: 训练早期平滑启动，之后保持常数学习率。
- **Search range**: warm-up 初始为 $1 0 ^ { - 3 }$ of the base learning rate。
- **Sensitivity**: 论文未给出学习率计划消融。
- **Source**: Sec 5.2

## 训练目标
- **Value**: flow-matching loss for future-frame generation + trajectory prediction loss
- **Rationale**: 联合监督未来视频生成与轨迹预测，让动作被未来视觉演化约束。
- **Search range**: 消融包含移除 Video Loss、Action Only、Default dual-prediction。
- **Sensitivity**: 很高；移除 Video Loss 或改为 Action Only 会显著削弱闭环规划与一致性。
- **Source**: Sec 5.2; Sec 5.7; Appendix E; Table 5; Table 10

## 混合精度与分布式训练
- **Value**: distributed bf16 mixed-precision training
- **Rationale**: 用于训练 Wan2.2-TI2V-5B 级别视频动作模型。
- **Search range**: 论文未报告其他精度设置。
- **Sensitivity**: 论文未给出精度消融。
- **Source**: Sec 5.2

## CARLA Mix Training
- **Value**: 默认消融最优配置包含 CARLA Mix Training
- **Rationale**: Bench2Drive/CARLA 模拟数据提供多样 corner-case 场景，补充 NAVSIM 真实数据。
- **Search range**: Table 5 对比包含与不包含 CARLA Mix Training 的设置。
- **Sensitivity**: 中等；论文称它从无混合训练配置进一步提升 PDMS，但主增益来自 video loss 与 video continuation。
- **Source**: Sec 5.7; Table 5
