# PhysicalAI-Autonomous-Vehicles 主结果
- **Source**: Table 2
- **Caption**: "在 PhysicalAI-Autonomous-Vehicles benchmark 的 curated 1,000-clip test subset 上比较。# Params 表示模型参数数量；SV 表示 single-view camera；∗ 表示使用 released checkpoint 评测，且只支持 up to 3s prediction。"

| Method | Source | Sensors | #Params |  ADE@3s↓ | FDE@3s ↓ | ADE@4s↓ | FDE@4s↓ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VaVAM* [23] | Valeo | sv | 1.3B | 2.31 | 4.32 | 1 | 1 |
| Alpamayo-1.5 [28] | NVIDIA | SV | 10B | 0.80 | 2.31 | 1.44 | 4.18 |
| DriveWAM | 1 | sv | 5B+8B | 0.47 | 1.35 | 0.83 | 2.47 |
