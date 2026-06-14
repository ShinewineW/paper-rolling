## 训练分辨率
- **Value**: 256×448
- **Rationale**: 所有模型均在该分辨率训练，以适配视频生成骨干和驾驶视频输入。
- **Search range**: 论文未报告其他训练分辨率。
- **Sensitivity**: 分析推断,论文未显式声明：分辨率会影响视频token数量、显存和细粒度几何建模。
- **Source**: Sec 4.2 Implementation Details

## 优化器
- **Value**: AdamW，β = ( 0 . 9 , 0 . 9 5 )
- **Rationale**: 用于全模型微调和新增模块训练。
- **Search range**: 论文未报告优化器搜索范围。
- **Sensitivity**: 分析推断,论文未显式声明：动量设置会影响扩散Transformer微调稳定性。
- **Source**: Sec 4.2 Implementation Details

## weight decay
- **Value**: 0.1
- **Rationale**: 作为AdamW正则化配置。
- **Search range**: 论文未报告其他weight decay。
- **Sensitivity**: 分析推断,论文未显式声明：过强可能抑制适配，过弱可能增加过拟合风险。
- **Source**: Sec 4.2 Implementation Details

## learning rate
- **Value**: 1 × 1 0 ^ { - 5 }
- **Rationale**: 用于DriveWAM训练的基础学习率。
- **Search range**: NAVSIM在50k、70k、90k迭代处按0.5因子衰减；论文未报告学习率网格。
- **Sensitivity**: 显式说明NAVSIM使用阶梯衰减；其他敏感性未报告。
- **Source**: Sec 4.2 Implementation Details

## per-device batch size
- **Value**: 1
- **Rationale**: 配合48 NVIDIA H20 GPUs训练。
- **Search range**: 论文未报告其他batch size。
- **Sensitivity**: 分析推断,论文未显式声明：更大batch可能受视频扩散骨干显存限制。
- **Source**: Sec 4.2 Implementation Details

## action loss weight
- **Value**: β_a = 1 . 0
- **Rationale**: 平衡未来世界建模与动作生成的联合flow-matching目标。
- **Search range**: 论文未报告β_a消融范围。
- **Sensitivity**: 论文说明β_a控制视频项和动作项的平衡；具体敏感性未报告。
- **Source**: Sec 3.1; Sec 4.2 Implementation Details

## chunk长度
- **Value**: 4-second chunk
- **Rationale**: DriveWAM按chunk进行video-action生成，并让VLM每个chunk生成一次指导。
- **Search range**: 论文未报告训练chunk长度搜索范围。
- **Sensitivity**: 分析推断,论文未显式声明：chunk长度影响语义指导频率、未来预测跨度和rollout粒度。
- **Source**: Sec 4.2 Implementation Details; Appendix B

## NAVSIM训练迭代
- **Value**: 100k iterations
- **Rationale**: NAVSIM设置使用当前帧作为条件并预测4-second future horizon。
- **Search range**: 学习率在50k、70k、90k处衰减；论文未报告其他迭代数。
- **Sensitivity**: 显式训练日程；迭代数敏感性未单独报告。
- **Source**: Sec 4.2 Implementation Details

## PhysicalAI训练迭代
- **Value**: 50k iterations
- **Rationale**: PhysicalAI-Autonomous-Vehicles主实验和消融使用固定训练步数。
- **Search range**: 数据规模消融使用4k、20k、100k clips，固定50k-iteration训练。
- **Sensitivity**: 论文显示更多数据在固定迭代下带来更好趋势，但未单独消融迭代数。
- **Source**: Sec 4.2; Sec 4.4 Data Scaling

## PhysicalAI训练样本裁剪
- **Value**: 12-second segment randomly cropped from a 20-second clip
- **Rationale**: 从长clip中随机裁剪训练片段，保持训练样本长度一致。
- **Search range**: 论文未报告其他裁剪长度。
- **Sensitivity**: 分析推断,论文未显式声明：裁剪长度影响可用历史和长时依赖覆盖。
- **Source**: Sec 4.2 Implementation Details

## 视频与动作采样率
- **Value**: video stream downsampled to 1 Hz，ego actions remain at 10 Hz
- **Rationale**: 视频低频建模场景演化，动作保持较高频率用于轨迹生成。
- **Search range**: 论文未报告其他采样率。
- **Sensitivity**: 分析推断,论文未显式声明：视频采样率影响视觉动态粒度，动作采样率影响控制平滑性。
- **Source**: Sec 4.2 Implementation Details

## guidance缓存策略
- **Value**: training时precomputed and cached；inference时once per decision step并复用所有denoising steps
- **Rationale**: 避免未来信息泄漏，同时使语义条件与当前预测horizon对齐。
- **Search range**: 论文未报告其他缓存策略。
- **Sensitivity**: 显式说明用于保持causal condition；延迟和一致性敏感性在效率分析中体现。
- **Source**: Sec 3.2 Causal guidance generation
