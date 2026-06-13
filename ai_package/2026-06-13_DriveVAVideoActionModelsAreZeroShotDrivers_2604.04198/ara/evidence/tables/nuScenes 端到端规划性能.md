# nuScenes 端到端规划性能
- **Source**: Table 3
- **Caption**: "nuScenes 数据集上的端到端 motion planning 性能，∗ 表示仅使用 front camera。"

| Method | nuScenes Finetune | Ref | Input | Auxiliary Supervision | L2 1s | L2 2s | L2 3s | L2 Avg. | Collision Rate 1s | Collision Rate 2s | Collision Rate 3s | Collision Rate Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST-P3 [25] | √ | ECCV&#x27;22 | Camera | Map&amp;Box&amp;Depth | 1.33 | 2.11 | 2.90 | 2.11 | 0.23 | 0.62 | 1.27 | 0.71 |
| UniAD [27] |  | CVPR23 | Camera | Map&amp;Box&amp;Motion | 0.48 | 0.96 | 1.65 | 1.03 | 0.05 | 0.17 | 0.71 | 0.31 |
| OccNet [51] |  | ICCV&#x27;23 | Camera | 3D-Occ&amp;Map&amp;Box | 1.29 | 2.13 | 2.99 | 2.14 | 0.21 | 0.59 | 1.37 | 0.72 |
| OccWorld [70] | √ | ECCV&#x27;24 | Camera | 3D-Occ | 0.52 | 1.27 | 2.41 | 1.40 | 0.12 | 0.40 | 2.08 | 0.87 |
| VAD-Tiny [30] | √ | ICCV&#x27;23 | Camera | Map&amp;Box&amp;Motion | 0.60 | 1.23 | 2.06 | 1.30 | 0.31 | 0.53 | 1.33 | 0.72 |
| VAD-Base [30] |  | ICCV&#x27;23 | Camera | Map&amp;Box&amp;Motion | 0.54 | 1.15 | 1.98 | 1.22 | 0.04 | 0.39 | 1.17 | 0.53 |
| GenAD [71] | √ | ECCV&#x27;24 | Camera | Map&amp;Box&amp;Motion | 0.36 | 0.83 | 1.55 | 0.91 | 0.06 | 0.23 | 1.00 | 0.43 |
| Doe-1 [72] | √ | arXiv&#x27;24 | |Camera* | QA | 0.50 | 1.18 | 2.11 | 1.26 | 0.04 | 0.37 | 1.19 | 0.53 |
| Epona [68] | √ | ICCV&#x27;25 | Camera* | None | 0.61 | 1.17 | 1.98 | 1.25 | 0.01 | 0.22 | 0.85 | 0.36 |
| Ours | X | - | Camera* | None | 0.33 | 0.76 1.43 |  | 0.84 | 0.00 | 0.07 | 0.12 | 0.06 |
