# Number of Queries 消融
- **Source**: Table 6
- **Caption**: "Number of Queries 消融；论文称更多 query tokens 提供更高容量的上下文槽位，从而增强 generation 与 planning。"

| Depth Queries | Video Queries | Action Queries | AbsRel↓ | $\delta _ { 1 } \uparrow$ | $\delta _ { 2 } \uparrow$ | $\delta _ { 3 } \uparrow$ | LPIPS↓ | PSNR↑ | FVD↓ | NC↑ | DAC↑ | TTC↑ | $C↑$ | EP↑ | PDMS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 32 | 32 | 48 | 9.7 | 90.2 | 97.9 | 99.4 |  | 0.20 | 20.67 | 57.97 | 98.2 | 97.0 | 95.0 | 100.0 | 83.2 | 88.9 |
| 64 | 64 |  | 8.1 | 92.8 | 98.6 | 99.5 | 0.20 |  | 21.05 | 53.59 | 98.4 | 97.1 | 95.1 | 100.0 | 83.5 | 89.2 |
