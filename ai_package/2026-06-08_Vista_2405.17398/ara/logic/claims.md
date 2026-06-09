# Claims

## C1: 在驾驶世界模型自动评估指标上达到最优
- **Statement**: Vista 在 nuScenes 验证集的 FID 和 FVD 指标上超越所有已报告的驾驶世界模型，FID 相较最优基线提升 55%，FVD 相较最优基线提升 27%
- **Status**: supported
- **Falsification criteria**: 若存在已公开的驾驶世界模型在 nuScenes 验证集上获得更低 FID 或 FVD，则本主张不成立
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 以标准扩散损失为基础，叠加动态增强损失与结构保留损失，并注入历史帧动态先验，共同驱动了显著的定量提升
- **Tags**: ['improvement']

## C2: 在人类评估中超越通用视频生成器
- **Statement**: Vista 在跨越 nuScenes、Waymo、OpenDV-YouTube-val 及 CODA 四个数据集的人类评估中，对视觉质量和运动合理性两个维度均超过最先进通用视频生成器超过 70% 的比较次数
- **Status**: supported
- **Falsification criteria**: 若受控人类评估复现后 Vista 胜率不超过 50%，则本主张不成立
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 人类评估覆盖四个代表性数据集（含未见域 Waymo 和角点案例 CODA），结果显示模型对驾驶动态的理解优于仅在网络规模数据上训练的通用生成器
- **Tags**: ['improvement', 'generalization']

## C3: 动态增强损失提升关键区域运动预测
- **Statement**: 与仅使用标准扩散损失相比，引入动态增强损失后，模型对运动实例（如移动车辆）的预测更加真实，能够生成符合物理规律的运动（如车辆正常前行、场景几何随转向正确偏移）
- **Status**: supported
- **Falsification criteria**: 若消融掉动态增强损失后，定性视觉观察中运动真实性无退化，则本主张不成立
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 动态感知权重通过计算相邻帧预测与真值之间的运动差异，自适应强调高运动区域的训练信号，从而改善扩散损失均匀监督对动态区域的局限性
- **Tags**: ['improvement', 'causal']

## C4: 结构保留损失改善高分辨率预测的结构细节
- **Statement**: 在高分辨率驾驶场景预测中，引入基于高频特征的结构保留损失可抑制运动物体轮廓的模糊与崩溃，保留车辆边缘等结构信息
- **Status**: supported
- **Falsification criteria**: 若消融掉结构保留损失后，视频质量无可见的结构退化，则本主张不成立
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 通过在频域中提取高频成分（FFT + 高通滤波 + IFFT）并对其施加额外监督，损失函数显式引导模型学习结构信息，补充了感知质量与运动强度之间的权衡
- **Tags**: ['improvement', 'causal']

## C5: 潜在替换方法支持长时域连贯自回归预测
- **Statement**: 将最多三帧历史帧的干净潜在编码替换对应位置的噪声潜在，可为模型提供位置、速度、加速度三阶运动先验，从而在自回归长时域预测中保持与历史帧的连贯性；引入越多先验帧，轨迹一致性越好
- **Status**: supported
- **Falsification criteria**: 若使用单帧先验与三帧先验的轨迹差异指标无显著区别，则本主张不成立
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 使用更多动态先验帧持续降低轨迹差异指标，验证了位置-速度-加速度三阶先验对长时域一致性的贡献；相比通道拼接方式，潜在替换对预训练权重扰动更小且灵活度更高
- **Tags**: ['improvement', 'causal']

## C6: 多模态行动控制能力以零样本方式泛化至未见数据集
- **Statement**: Vista 在 nuScenes 上学习到的多模态行动控制（轨迹、角度与速度、命令、目标点）可以零样本方式泛化到训练域以外的 Waymo 数据集，行动控制仍能有效引导预测运动
- **Status**: supported
- **Falsification criteria**: 若在 Waymo 数据集上 Vista 的行动控制预测与无行动控制预测的轨迹差异无显著区别，则本主张不成立
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 协作训练策略将 OpenDV-YouTube（无标注）与 nuScenes（有标注）联合训练，行动独立约束防止训练资源分散于组合，使每种行动模式在相同训练步数内得到充分优化
- **Tags**: ['generalization']

## C7: 基于预测不确定性的泛化奖励函数可在无真值动作下评估驾驶行为
- **Statement**: 利用 Vista 自身对同一条件帧与动作的多轮去噪的条件方差可定义奖励函数，该奖励随轨迹 L2 误差的增大而单调下降，无需访问真值动作，且能泛化到训练域外的 Waymo 数据集
- **Status**: supported
- **Falsification criteria**: 若在 Waymo 数据集上高 L2 误差轨迹的平均奖励不低于低 L2 误差轨迹，则本主张不成立
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 分布外条件（劣质动作）使生成多样性增大从而条件方差升高、奖励降低；该机制无需感知模块或真值标注，直接继承 Vista 的跨场景泛化能力
- **Tags**: ['generalization', 'descriptive']
