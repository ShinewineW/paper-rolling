# driving world models 视频生成质量对比
- **Source**: Table 2
- **Caption**: "driving world models 的视频生成质量比较，FVD 4.1 衡量未来视频序列真实感，并报告预测时长、帧率、数据集和视角。"

| Metric & Settings | WoVoGen [35] | DriveDreamer [48] | SVD [2,7] | DrivingGPT[7] | GenAD [55] | Ours |
| --- | --- | --- | --- | --- | --- | --- |
| FVD↓ | 417.7 | 340.8 | 227.5 | 142.6 | 184.0 | 141.8 |
| Max Duration/Fps | 2.5 s/2 Hz | 4s/2Hz | 4s/2Hz | 4s/2Hz | 4s/2Hz | 4s/2Hz |
| Dataset | nuScenes | nuScenes | NAVSIM | NAVSIM | OpenDV | NAVSIM |
| View | Multi | Multi | Front | Front | Front | Front |
