# scene-evolving guidance 与数据规模消融
- **Source**: Table 3
- **Caption**: "在 PhysicalAI-Autonomous-Vehicles benchmark 上，不同训练数据规模下 scene-evolving driving guidance 的消融。✗ 表示 fixed global prompt as text conditioning。"

| # Clips | #Iters | SE Guidance | ADE@4s ↓ | FDE@4s↓ |
| --- | --- | --- | --- | --- |
| 4k | 50k |  | 1.21 | 3.65 |
| 4k | 50k | × | 1.01 | 2.95 |
| 20k | 50k | × | 0.95 | 2.94 |
| 20k | 50k |  | 0.94 | 2.65 |
| 100k | 50k |  | 0.92 | 2.75 |
| 100k | 50k | X | 0.83 | 2.47 |
