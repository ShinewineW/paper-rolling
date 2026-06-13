# Bench2Drive多能力结果
- **Source**: Table 2
- **Caption**: "Bench2Drive base set上E2E-AD方法的Multi-Ability结果。"

| Method | Reference | Condition Modality |  | Merging | Overtaking | Emergency Brake | Give Way | Traff c Sign | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TCP* [61] | NeurIPS 22 | TP | C | 16.18 | 20.00 | 20.00 | 10.00 | 6.99 | 14.63 |
| TCP-ctrl|* | NeurIPS 22 | TP | c | 10.29 | 4.44 | 10.00 | 10.00 | 6.45 | 8.23 |
| TCP-traj* | NeurIPS 22 | TP | C | 8.89 | 24.29 | 51.67 | 40.00 | 46.28 | 34.22 |
| TCP-traj w/o distillation | NeurIPS 22 | TP | C | 17.14 | 6.67 | 40.00 | 50.00 | 28.72 | 28.51 |
| ThinkTwice*[22] | CVPR 23 | TP | C | 27.38 | 18.42 | 35.82 | 50.00 | 54.23 | 37.17 |
| DriveAdapter* [21] | ICCV23 | TP | C&amp;L | 28.82 | 26.38 | 48.76 | 50.00 | 56.43 | 42.08 |
| AD-MLP [64] | arXiv 23 | NC | C | 0.00 | 0.00 | 0.00 | 0.00 | 4.35 | 0.87 |
| UniAD-Tiny [18] | CVPR23 | NC | C | 8.89 | 9.33 | 20.00 | 20.00 | 15.43 | 14.73 |
| UniAD-Base [18] | CVPR 23 | NC | c | 14.10 | 17.78 | 21.67 | 10.00 | 14.21 | 15.55 |
| VAD [25] | ICCV23 | NC | C | 8.11 | 24.44 | 18.64 | 20.00 | 19.15 | 18.07 |
| DriveTransformer-Large [24] | ICLR 25 | NC | c | 17.57 | 35.00 | 48.36 | 40.00 | 52.10 | 38.60 |
| ORION (Ours) |  | NC | C | 25.00 | 71.11 | 78.33 | 30.00 | 69.15 | 54.72(+16.12) |
