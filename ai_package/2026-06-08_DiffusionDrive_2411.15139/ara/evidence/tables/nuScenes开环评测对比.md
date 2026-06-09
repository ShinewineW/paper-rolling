# nuScenes开环评测对比
- **Source**: Table 7
- **Caption**: "nuScenes数据集开环评测对比。FPS在单块NVIDIA 4090 GPU上按SparseDrive评测流程测量，指标计算遵循ST-P3方法。"

| Method | Input | Img. Backbone | L2 1s↓ | L2 2s↓ | L2 3s↓ | L2 Avg.↓ | CR 1s↓ | CR 2s↓ | CR 3s↓ | CR Avg.↓ | FPS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST-P3 [15] | Camera | EffNet-b4 [40] | 1.33 | 2.11 | 2.90 | 2.11 | 0.23 | 0.62 | 1.27 | 0.71 | 1.6 |
| UniAD [16] | Camera | ResNet-101[13] | 0.45 | 0.70 | 1.04 | 0.73 | 0.62 | 0.58 | 0.63 | 0.61 | 1.8 |
| OccNet [41] | Camera | ResNet-50[13] | 1.29 | 2.13 | 2.99 | 2.14 | 0.21 | 0.59 | 1.37 | 0.72 | 2.6 |
| VAD [20] | Camera | ResNet-50[13] | 0.41 | 0.70 | 1.05 | 0.72 | 0.07 | 0.17 | 0.41 | 0.22 | 4.5 |
| SparseDrive [39] | Camera | ResNet-50[13] | 0.29 | 0.58 | 0.96 | 0.61 | 0.01 | 0.05 | 0.18 | 0.08 | 9.0 |
| DiffusionDrive (Ours) | Camera | ResNet-50[13] | 0.27 | 0.54 | 0.90 | 0.57 | 0.03 | 0.05 | 0.16 | 0.08 | 8.2 |
