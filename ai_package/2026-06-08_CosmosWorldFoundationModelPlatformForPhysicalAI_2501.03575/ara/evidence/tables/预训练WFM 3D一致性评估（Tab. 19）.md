# 预训练WFM 3D一致性评估（Tab. 19）
- **Source**: Table 19
- **Caption**: "基础Cosmos WFM与VideoLDM在RealEstate10K测试集500个视频上的几何一致性和新视角合成一致性评估结果"

| 方法 | Sampson误差↓ | 位姿估计成功率(%)↑ | PSNR↑ | SSIM↑ | LPIPS↓ |
| --- | --- | --- | --- | --- | --- |
| VideoLDM (Blattmann et al., 2023) | 0.841 | 4.4% | 26.23 | 0.783 | 0.135 |
| Cosmos-Predict1-7B-Text2World | 0.355 | 62.6% | 33.02 | 0.939 | 0.070 |
| Cosmos-Predict1-7B-Video2World | 0.473 | 68.4% | 30.66 | 0.929 | 0.085 |
| Cosmos-Predict1-4B | 0.433 | 35.6% | 32.56 | 0.933 | 0.090 |
| Cosmos-Predict1-5B-Video2World | 0.392 | 27.0% | 32.18 | 0.931 | 0.090 |
| Real Videos (Reference) | 0.431 | 56.4% | 35.38 | 0.962 | 0.054 |
