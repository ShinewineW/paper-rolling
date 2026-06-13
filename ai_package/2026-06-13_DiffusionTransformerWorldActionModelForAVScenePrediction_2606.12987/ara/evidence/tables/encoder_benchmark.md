# encoder_benchmark
- **Source**: Table 1
- **Caption**: "冻结编码器在nuScenes held-out test scenes上的动作预测RMSE；RMSE越低越好，V-JEPA2 rep64利用时间上下文并优于单帧编码器。"

| Encoder | Steer RMSE | Accel RMSE |
| --- | --- | --- |
| V-JEPA2 rep64 | $\mathbf { 0 . 0 5 8 } { \scriptstyle \pm . 0 1 2 }$ | $\mathbf { 0 . 0 5 5 } { \scriptstyle \pm . 0 0 4 }$ |
| V-JEPA2 rep1 | $0 . 0 9 7 { \scriptstyle \pm . 0 1 9 }$ | $0 . 0 5 9 { \scriptstyle \pm . 0 0 4 }$ |
| DINOv2-S/14 | $0 . 1 0 4 { \scriptstyle \pm . 0 1 7 }$ | $0 . 0 7 2 { \scriptstyle \pm . 0 0 4 }$ |
| CLIP ViT-B/32 | $0 . 1 1 7 { \scriptstyle \pm . 0 1 9 }$ | $0 . 0 6 7 { \scriptstyle \pm . 0 0 4 }$ |
| ViT-S/16 | $0 . 1 2 1 { \scriptstyle \pm . 0 1 9 }$ | $0 . 0 7 1 { \scriptstyle \pm . 0 0 4 }$ |
| VQ-VAE Tracker | $0 . 1 2 6 { \scriptstyle \pm . 0 2 1 }$ | $0 . 0 6 3 { \scriptstyle \pm . 0 0 5 }$ |
