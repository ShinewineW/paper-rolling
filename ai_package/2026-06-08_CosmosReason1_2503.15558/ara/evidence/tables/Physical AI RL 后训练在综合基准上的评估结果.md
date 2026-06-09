# Physical AI RL 后训练在综合基准上的评估结果
- **Source**: Table 9
- **Caption**: "Physical AI RL 后训练效果对比（准确率 %）。RL 使 Cosmos-Reason1-7B 综合平均准确率从 60.7 提升至 65.7（提升 5.0 个百分点）；大多数子任务均有提升，RoboFail 任务改善有限。"

| Models | Common Sense | BridgeData V2 | RoboVQA | Agibot | HoloAssist | AV | RoboFail | Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cosmos-Reason1-7B | 54.3 | 58.8 | 83.8 | 49.4 | 63.0 | 55.6 | 60.0 | 60.7 |
| + Physical AI RL | 56.2 | 73.5 | 86.8 | 54.2 | 60.0 | 67.0 | 62.0 | 65.7 (+5.0) |
