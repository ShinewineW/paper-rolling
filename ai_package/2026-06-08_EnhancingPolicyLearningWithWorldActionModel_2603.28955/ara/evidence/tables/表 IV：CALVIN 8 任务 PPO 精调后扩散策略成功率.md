# 表 IV：CALVIN 8 任务 PPO 精调后扩散策略成功率
- **Source**: Table IV
- **Caption**: "800 轮模型内 PPO 精调后，8 个 CALVIN 任务上的扩散策略成功率（%）。DPPO 列报告匹配 DiWA 性能所需的环境步数（越少越高效）。"

| Task | Diffusion Policy Base | DiWA Offline Fine-Tuning | WAM (Ours) Online Fine-Tuning | DPPO Vision WM Encoder Env Steps to Match DiWA | Vision Env Steps to Match DiWA |
| --- | --- | --- | --- | --- | --- |
| open drawer | 73.3 ± 4.8 | 74.44 ± 1.92 | 96.7 ± 2.4 | 117,600 ± 23,758 | 134,400 ± 26,508 |
| close drawer | 89.7 ± 3.1 | 91.95 ± 1.99 | 96.6 ± 1.8 | 600,600 ± 27,651 | 1,545,600 ± 261,346 |
| move slider left | 68.8 ± 5.2 | 83.33 ± 1.80 | 87.5 ± 3.7 | 270,933 ± 28,780 | 1,377,600 ± 251,439 |
| move slider right | 82.8 ± 3.9 | 82.76 ± 3.45 | 89.7 ± 3.2 | 249,600 ± 09,050 | 537,600 ± 23,758 |
| turn on lightbulb | 51.5 ± 4.6 | 91.92 ± 1.75 | 100.0 ± 0.0 | 302,933 ± 15,964 | 588,000 ± 62,859 |
| turn off lightbulb | 17.2 ± 3.4 | 77.01 ± 1.99 | 75.9 ± 4.3 | 327,066 ± 13,546 | 1,260,000 ± 142,552 |
| turn on LED | 41.4 ± 4.1 | 86.21 ± 3.45 | 96.6 ± 2.1 | 494,933 ± 45,655 | 2,251,200 ± 33,940 |
| turn off LED | 68.8 ± 4.7 | 82.33 ± 6.53 | 100.0 ± 0.0 | 277,333 ± 31,928 | 184,800 ± 23,758 |
| Total Physical Interactions |  | 0 | 0 | ~2.5M | ~8M |
