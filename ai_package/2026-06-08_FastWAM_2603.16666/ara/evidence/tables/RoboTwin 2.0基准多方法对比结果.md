# RoboTwin 2.0基准多方法对比结果
- **Source**: Table 1
- **Caption**: "RoboTwin结果。Fast-WAM在无具身预训练情况下与强预训练WAM基线性能相当;两个imagine-then-execute变体结果高度可比;去除视频协训练导致显著性能下降"

| Method | Embodied PT. | Clean | Rand. | Average |
| --- | --- | --- | --- | --- |
| πo[10] | - | 65.92 | 58.40 | 62.2 |
| π0.5[11] | - | 82.74 | 76.76 | 79.8 |
| Motus [5] | √ | 88.66 | 87.02 | 87.8 |
| LingBot-VA [3] | √ | 92.90 | 91.50 | 92.2 |
| LingBot-VA from WAN2.2 | × | 80.60 | - | 80.6 |
| Fast-WAM (Ours) | × | 91.88 | 91.78 | 91.8 |
| Fast-WAM-Joint | × | 90.84 | 90.32 | 90.6 |
| Fast-WAM-IDM | × | 91.16 | 91.34 | 91.3 |
| Fast-WAM w.o. video co-train | × | 82.76 | 84.80 | 83.8 |
