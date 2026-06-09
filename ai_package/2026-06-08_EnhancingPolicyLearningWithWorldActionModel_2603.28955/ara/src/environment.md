# Environment
- **Python**: 论文未明确说明
- **Framework**: 论文未明确说明具体深度学习框架;采用AdamW优化器、DPPO[16]、DDPM采样
- **Hardware**: 论文未明确说明GPU型号或数量
- **Key dependencies**: DreamerV2 (RSSM世界模型基础架构,参考[4][17]), CALVIN benchmark 环境D (7-DoF Franka Emika Panda机器人操作台,参考[13]), DPPO (扩散策略PPO优化,参考[16]), DiWA (下游策略学习基线流水线,参考[8]), AdamW (世界模型优化器,权重衰减0.05), DDPM采样 (扩散策略去噪采样)
- **Random seeds**: seed 42 用于从每任务50个专家演示中提取特征及生成奖励标签
