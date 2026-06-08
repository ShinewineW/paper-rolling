# Table 5: GB200 NVL72不同GPU数量下的生成时间
- **Source**: Table 5
- **Caption**: "Cosmos-Transfer1-7B在不同并行GPU数量下生成一个5秒视频的计算时间。64块B200 GPU时端到端时间为4.2秒，低于5秒实现实时吞吐量；从1到64 GPU约实现40倍加速（纯扩散时间：141.0s→3.5s）。"

| Number of GPUs | 1 | 4 | 8 | 16 | 32 | 64 |
| --- | --- | --- | --- | --- | --- | --- |
| Diffusion only | 141.0 s | 39.3 s | 20.1 s | 10.3 s | 5.4s | 3.5 s |
| End-to-end | 141.7 s | 40.0 s | 20.8 s | 11.0 s | 6.1 s | 4.2 s |
