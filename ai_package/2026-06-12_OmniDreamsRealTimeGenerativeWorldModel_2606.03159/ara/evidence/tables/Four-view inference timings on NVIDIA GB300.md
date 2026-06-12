# Four-view inference timings on NVIDIA GB300
- **Source**: Table 3
- **Caption**: "四视角推理每分块计时；KV-cache update 不计入 Total。"

| Stage | 1×GPU | $4 \times \mathrm { G P U }$ | 8×GPU | 16×GPU |
| --- | --- | --- | --- | --- |
| Diffusion DiT | 1,184ms | 300ms | 179 ms | 121ms |
| RGB Decoder | 105 ms | 30ms | 30ms | 30ms |
|  KV-cache update (separate thread) | 558ms | 149 ms | 91ms | 67ms |
| Total | 1,289 ms | 330ms | 209ms | 151ms |
| Effective FPS | 12 | 48 | 74 | 105 |
