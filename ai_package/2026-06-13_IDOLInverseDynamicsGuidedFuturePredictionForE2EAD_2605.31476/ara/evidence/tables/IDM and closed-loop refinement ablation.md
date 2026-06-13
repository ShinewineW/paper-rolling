# IDM and closed-loop refinement ablation
- **Source**: Table 3
- **Caption**: "NAVSIM navtest split 上 inverse dynamics model 与 closed-loop refinement 的主消融；IDM 表示 inverse dynamics model，CL 表示 closed-loop refinement。"

| IDM | CL iters. | NC↑ | DAC个 | TTC↑ | Comf.个 | EP↑ | PDMS ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| × | × | 98.5 | 95.0 | 95.2 | 100 | 81.5 | 87.3 |
| √ | × | 98.6 | 97.0 | 95.4 | 100 | 83.3 | 89.2 |
| √ | 2 | 98.8 | 97.6 | 95.9 | 100 | 83.8 | 90.0 |
| √ | 3 | 98.6 | 97.3 | 95.2 | 100 | 83.5 | 89.4 |
