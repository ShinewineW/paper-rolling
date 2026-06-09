# 驾驶先验对比（锚定高斯分布 vs 外推轨迹）
- **Source**: Table 8
- **Caption**: "驾驶先验对比实验。「Anchored Dist.」表示锚定高斯分布；「Extra. Traj.」表示基于当前状态的外推轨迹。Row-1（蓝色标注）为DiffusionDrive主论文基线。结果验证了多模式锚定高斯分布先验优于单一外推轨迹先验。"

| Train | Infer | NC↑ | DAC↑ | TTC↑ | Comf.↑ | EP↑ | PDMS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Anchored Dist. | Anchored. Dist. | 98.2 | 96.2 | 94.7 | 100 | 82.2 | 88.1 |
| Anchored Dist. | Extra. Traj. | 96.3 | 91.7 | 90.4 | 100 | 76.8 | 81.3 |
| Extra. Traj. | Extra. Traj. | 97.3 | 94.0 | 92.6 | 100 | 79.6 | 84.7 |
