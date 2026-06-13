# 零样本 nuScenes 与 Bench2Drive 规划性能
- **Source**: Table 2
- **Caption**: "所有方法在 NAVSIM 训练后不做任何 fine-tuning，直接评估到 nuScenes 与 Bench2Drive。"

| Method | Finetune | Ref | nuScenes L2 1s 2s | nuScenes L2 3s | nuScenes L2 Avg. | nuScenes Collision 1s 2s 3s | nuScenes Collision Avg. | Bench2Drive L2 1s 2s 3s | Bench2Drive L2 Avg. | Bench2Drive Collision 1s 2s 3s | Bench2Drive Collision Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VLA-World Model Methods |  |  |  |  |  |  |  |  |  |  |  |
| DriveVLA-W0 [35] | X | ICLR&#x27;26 | 0.431.26 2.60 |  | 1.43 | 0.220.66 1.42 | 0.77 | 1.01 2.77 5.22 | 3.00 | 1.492.53 3.53 | 2.52 |
| WorldModelMethods |  |  |  |  |  |  |  |  |  |  |  |
| PWM [69] | X | NeurIPS&#x27;25|2.063.916.00 |  |  | 3.99 | 0.12 0.15 0.86 | 0.36 | 1.70 2.743.97 | 2.80 | 4.01 3.73 3.53 | 3.76 |
| Ours | X | 1 | 0.330.761.43 0.84 |  |  | 0.00 0.07 0.12 0.06 |  | 0.691.29 2.031 | 31.33 | 1.381.97 2.65 | 51.79 |
