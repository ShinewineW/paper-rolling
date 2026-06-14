# KV memory 策略消融
- **Source**: Table 5
- **Caption**: "KV memory strategies 消融。ADE/FDE 在 20s clips 上测量，KV memory 和 GFLOPs 在 300s clip 下 profile。"

| KV memory | ADE@4s↓ | FDE@4s↓ | Mem.(GB)↓ | GFLOPs↓ |
| --- | --- | --- | --- | --- |
| Full | 0.83 | 2.47 | 3.07 | 17.37 |
| FIFO | 1.40 | 3.47 | 0.25 | 1.05 |
| Selective | 0.89 | 2.52 | 0.25 | 1.44 |
