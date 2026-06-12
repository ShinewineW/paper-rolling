# 3D environments visual quality results
- **Source**: Table 8
- **Caption**: "CS:GO 与 Driving 上真实轨迹和生成轨迹之间的视觉质量指标、采样速率和参数量。"

| Method | CS:GO FID↓ | CS:GO FVD↓ | CS:GO LPIPS ↓ | Driving FID↓ | Driving FVD↓ | Driving LPIPS ↓ | Sample rate (HZ) ↑ | Parameters (#) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DreamerV3 | 106.8 | 509.1 | 0.173 | 167.5 | 733.7 | 0.160 | 266.7 | 181M |
| IRIS  $( K = 1 6 )$  | 24.5 | 110.1 | 0.129 | 51.4 | 368.7 | 0.188 | 4.2 | 123M |
| IRIS (K = 64) | 22.8 | 85.7 | 0.116 | 44.3 | 276.9 | 0.148 | 1.5 | 111M |
| DIAMOND frame-stack (ours) DIAMOND cross-attention (ours) | 9.6 | 34.8 81.4 | 0.107 | 16.7 | 80.3 | 0.058 | 7.4 | 122M |
|  | 11.6 |  | 0.125 | 35.2 | 299.9 | 0.119 | 2.5 | 184M |
