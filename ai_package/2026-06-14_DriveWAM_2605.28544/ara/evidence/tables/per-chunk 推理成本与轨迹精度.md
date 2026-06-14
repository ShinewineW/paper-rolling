# per-chunk 推理成本与轨迹精度
- **Source**: Table 6
- **Caption**: "在 single H20 GPU 上的 per-chunk inference cost 和 trajectory prediction accuracy。∗ 表示 action denoising steps 从 10 reduced to 5。"

| Method | VLM (ms) | Video Gen (ms) | Action (ms) | ADE@4s↓ | FDE@4s↓ |
| --- | --- | --- | --- | --- | --- |
| Alpamayo-1.5 | 570 |  | 330 | 1.44 | 4.18 |
| DriveWAM (Ours) | 125 | 372 | 765 | 0.83 | 2.47 |
| DriveWAM*(Ours) | 125 | 372 | 374 | 0.84 | 2.45 |
