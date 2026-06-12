# Single-view inference timings on NVIDIA GB300
- **Source**: Table 2
- **Caption**: "单视角推理每分块计时；KV-cache update 不计入 Total。"

| Stage | $1 \times \mathrm { G P U }$ | $2 \times \mathrm { G P U }$ | $4 \times \mathrm { G P U }$ | 8×GPU |
| --- | --- | --- | --- | --- |
| World scenario encoding Diffusion DiT RGB Decoder | 28ms 84ms 6ms | 26ms 71ms 5ms | 26ms 49 ms 5ms | 26ms 47ms 5ms |
| KV-cache update (separate thread) | 42ms | 34ms | 23 ms | 22 ms |
| Total Effective FPS | 118 ms 68 | 102 ms 78 | 80 ms 100 | 78 ms 103 |
