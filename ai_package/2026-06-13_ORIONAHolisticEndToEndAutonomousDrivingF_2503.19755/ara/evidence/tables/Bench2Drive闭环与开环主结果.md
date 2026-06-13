# Bench2Drive闭环与开环主结果
- **Source**: Table 1
- **Caption**: "Bench2Drive base set上E2E-AD方法的闭环与开环结果；C/L表示camera/LiDAR，NC表示navigation command，TP表示target point。"

| Method | Reference | Condition | Modality | DS↑ | SR(%)↑ | Efficiency↑ | Comfortness↑ | Open-loop Metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TCP* [61] | NeurIPS 22 | TP | C | 40.70 | 15.00 | 54.26 | 47.80 | Avg. L2↓ 1.70 |
| TCP-ctrl* | NeurIPS 22 | TP | C | 30.47 | 7.27 | 55.97 | 51.51 | - |
| TCP-traj* | NeurIPS 22 | TP | C | 59.90 | 30.00 | 76.54 | 18.08 | 1.70 |
| TCP-traj w/o distillation | NeurIPS 22 | TP | C | 49.30 | 20.45 | 78.78 | 22.96 | 1.96 |
| ThinkTwice* [22] | CVPR 23 | TP | C | 62.44 | 31.23 | 69.33 | 16.22 | 0.95 |
| DriveAdapter* [21] | ICCV 23 | TP | C&amp;L | 64.22 | 33.08 | 70.22 | 16.01 | 1.01 |
| AD-MLP [64] | arXiv 23 | NC | C | 18.05 | 0.00 | 48.45 | 22.63 | 3.64 |
| UniAD-Tiny [18] | CVPR 23 | NC | C | 40.73 | 13.18 | 123.92 | 47.04 | 0.80 |
| UniAD-Base [18] | CVPR 23 | NC | C | 45.81 | 16.36 | 129.21 | 43.58 | 0.73 |
| VAD [25] | ICCV 23 | NC | C | 42.35 | 15.00 | 157.94 | 46.01 | 0.91 |
| GenAD [70] | ECCV 24 | NC | C | 44.81 | 15.90 | - | - | - |
| MomAD[52] | CVPR25 | NC | C | 44.54 | 16.71 | 170.21 | 48.63 | 0.87 |
| DriveTransformer-Large [24] | ICLR 25 | NC | C | 63.46 | 35.01 | 100.64 | 20.78 | 0.62 |
| ORION(Ours) |  | NC | C | 77.74(+14.28) | 54.62(+19.61) | 151.48 | 17.38 | 0.68 |
