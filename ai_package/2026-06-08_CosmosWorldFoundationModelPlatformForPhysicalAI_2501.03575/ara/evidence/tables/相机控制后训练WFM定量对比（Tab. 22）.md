# 相机控制后训练WFM定量对比（Tab. 22）
- **Source**: Table 22
- **Caption**: "后训练相机控制世界模型与CamCo在RealEstate10K测试集（500样本）上的相机轨迹对齐和视频生成质量定量对比；两模型均在DL3DV-10K训练集上微调"

| 方法 | 位姿估计成功率(%)↑ | 旋转误差(°)↓ | 平移误差↓ | FID↓ | FVD↓ |
| --- | --- | --- | --- | --- | --- |
| CamCo (Xu et al., 2024) | 43.0% | 8.277 | 0.185 | 57.49 | 433.24 |
| Cosmos-Predict1-7B-Video2World-Sample-CameraCond | 82.0% | 1.646 | 0.038 | 14.30 | 120.49 |
