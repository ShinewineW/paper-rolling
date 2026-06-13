# model_size_scaling_architectures_compute
- **Source**: Table 10
- **Caption**: "Model size scaling 的架构与 compute usage；用于支撑 Figure 9 的 scaling 实验背景。"

| Parameters | num _layers | num_heads | d_model | $\mathrm { k / q }$ size | training hardware | training time | FLOPs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 41M | 18 | 8 | 512 | 64 | 64 TPUv2 | 3 days |  $2 . 0 5 \times 1 0 ^ { 2 0 }$  |
| 96M | 16 | 16 | 768 | 64 | 64 TPUv2 | 6days |  $3 . 5 8 \times 1 0 ^ { 2 0 }$  |
| 192M | 20 | 18 | 1024 | 64 | 64 TPUv2 | 9 days |  $6 . 4 \times 1 0 ^ { 2 0 }$  |
| 404M | 21 | 12 | 1536 | 128 | 64 TPUv2 | 18 days |  $1 . 2 \times 1 0 ^ { 2 1 }$  |
| 811M | 20 | 20 | 2048 | 128 | 128 TPUv3 | 7 days |  $2 . 2 \times 1 0 ^ { 2 1 }$  |
| 1.6B | 28 | 22 | 2560 | 128 | 128 TPUv3 | 12 days |  $4 . 0 4 \times 1 0 ^ { 2 1 }$  |
| 2.7B | 36 | 22 | 3072 | 128 | 256 TPUv3 | 16 days |  $6 . 9 1 \times 1 0 ^ { 2 1 }$  |
