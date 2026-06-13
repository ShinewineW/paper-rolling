# NAVSIM v1 navtest closed-loop metrics
- **Source**: Table 1
- **Caption**: "NAVSIM v1 navtest split 上 closed-loop metrics 的性能比较；论文说明 C 和 L 分别表示 camera 与 LiDAR 输入，所有结果均在 ResNet-34 image-backbone 设置下报告。"

| Method | Img. Backbone | Input | $\mathbf { N C \dag }$ | DAC个 | TTC个 | Comf. 个 | $\mathbf { E P \uparrow }$ | PDMS 个 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VADv2 [5] | ResNet-34 | C&L | 97.2 | 89.1 | 91.6 | 100 | 76.0 | 80.9 |
| UniAD [21] | ResNet-34 | Camera | 97.8 | 91.9 | 92.9 | 100 | 78.8 | 83.4 |
| PARA-Drive [66] | ResNet-34 | Camera | 97.9 | 92.4 | 93.0 | 99.8 | 79.3 | 84.0 |
| TransFuser [7] | ResNet-34 | C&L | 97.7 | 92.8 | 92.8 | 100 | 79.2 | 84.0 |
| LAW [36] | ResNet-34 | Camera | 96.4 | 95.4 | 88.7 | 99.9 | 81.7 | 84.6 |
| DiffusionDrive [44] | ResNet-34 | C&L | 98.2 | 96.2 | 94.7 | 100 | 82.2 | 88.1 |
| WoTE [38] | ResNet-34 | C&L | 98.5 | 96.8 | 94.9 | 99.9 | 81.9 | 88.3 |
| SeerDrive [77] | ResNet-34 | C&L | 98.4 | 97.0 | 94.9 | 99.9 | 83.2 | 88.9 |
| ResWorld*[78] | ResNet-34 | C&L | 98.9 | 96.5 | 95.6 | 100 | 83.1 | 89.0 |
| MeanFuser [62] | ResNet-34 | Camera | 98.6 | 97.0 | 95.0 | 100 | 82.8 | 89.0 |
| DiffE2Et [80] | ResNet-34 | C&L | 99.2 | 96.8 | 96.7 | 100 | 83.6 | 89.8 |
| IDOL | ResNet-34 | C&L | 98.8 | 97.6 | 95.9 | 100 | 83.8 | 90.0 |
