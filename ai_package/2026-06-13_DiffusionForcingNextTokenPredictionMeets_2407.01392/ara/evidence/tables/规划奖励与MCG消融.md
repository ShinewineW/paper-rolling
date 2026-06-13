# 规划奖励与MCG消融
- **Source**: Table 1
- **Caption**: "Diffusion Forcing用于规划；采样时不同时间步可按不同噪声日程去噪，并报告跨运行最高平均奖励。"

| Environment | Task | MPPI | CQL | IQL | Diffuser* | Diffuser w/ diffused action | Ours wo/ MCG | Ours |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maze2D | U-Maze | 33.2 | 5.7 | 47.4 | $1 1 3 . 9 \pm 3 . 1$ | $6 . 3 \pm 2 . 1$ | $1 1 0 . 1 \pm 3 . 9$ | ${ \bf 1 1 6 . 7 \pm 2 . 0 }$ |
| Maze2D | Medium | 10.2 | 5.0 | 34.9 | $1 2 1 . 5 \pm 2 . 7$ | 13.5±2.3 | $1 3 6 . 1 \pm 1 0 . 2$ | ${ \bf 1 4 9 . 4 \pm 7 . 5 }$ |
| Maze2D | Large | 5.1 | 12.5 | 58.6 | $1 2 3 . 0 \pm 6 . 4$ | 6.3 ±2.1 | $1 4 2 . 8 \pm 5 . 6$ | ${ \bf 1 5 9 . 0 \pm 2 . 7 }$ |
| Single-task Average |  | 16.2 | 7.7 | 47.0 | 119.5 | 8.7 | 129.67 | 141.7 |
| Multi2D | U-Maze | 41.2 | - | 24.8 | $1 2 8 . 9 \pm 1 . 8$ | 32.8±1.7 | $1 0 7 . 7 \pm 4 . 9$ | ${ \bf 1 1 9 . 1 \pm 4 . 0 }$ |
| Multi2D | Medium | 15.4 | - | 12.1 | $1 2 7 . 2 \pm 3 . 4$ | 22.0±2.7 | $1 4 5 . 6 \pm 6 . 5$ | ${ \bf 1 5 2 . 3 \pm 9 . 9 }$ |
| Multi2D | Large | 8.0 | - | 13.9 | $1 3 2 . 1 \pm 5 . 8$ | 6.9 ±1.7 | $1 2 9 . 8 \pm 1 . 5$ | ${ \bf 1 6 7 . 1 \pm 2 . 7 }$ |
| Multi-task Average |  | 21.5 | - | 16.9 | 129.4 | 20.6 | 127.7 | 146.2 |
