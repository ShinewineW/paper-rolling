# 多视角驾驶世界模型生成质量与多视角一致性评估（Tab. 24）
- **Source**: Table 24
- **Caption**: "多视角驾驶视频生成质量（FID/FVD，基于1000个样本）与多视角几何一致性（TSE/CSE，基于800个样本）对比；TSE=时间Sampson误差，CSE=跨视角Sampson误差"

| 方法 | FID↓ | FVD↓ | TSE↓ | CSE↓ |
| --- | --- | --- | --- | --- |
| VideoLDM-MultiView | 60.84 | 884.46 | 1.24 | 6.48 |
| Cosmos-Predict1-7B-Text2World-Sample-MultiView | 32.16 | 210.23 | 0.68 | 2.11 |
| Cosmos-Predict1-7B-Text2World-Sample-MultiView-TrajectoryCond | - | - | 0.59 | 2.02 |
| Real Videos (Reference) | - | - | 0.69 | 1.71 |
