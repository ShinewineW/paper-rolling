# pretrain、future-frame modeling 与 depth conditioning 消融
- **Source**: Table 3
- **Caption**: "pretraining、future-frame modeling 与 depth conditioning 对规划质量和未来帧生成质量的影响。"

| Pretrain | Future Frames | Depth | NC↑ | DAC ↑ | EP↑ | TTC ↑ | Comf. 个 | PDMS ↑ | FVD↓ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| × | × | × | 97.1 | 91.4 | 77.4 | 91.5 | 100.0 | 82.1 | - |
| √ | × | × | 98.8 | 95.8 | 82.0 | 95.8 | 100.0 | 88.2 | - |
| √ | √ | × | 98.8 | 96.5 | 82.9 | 96.4 | 100.0 | 89.2 | 164.2 |
| √ | √ | √ | 98.7 | 96.7 | 83.2 | 96.1 | 100.0 | 89.4 | 141.8 |
