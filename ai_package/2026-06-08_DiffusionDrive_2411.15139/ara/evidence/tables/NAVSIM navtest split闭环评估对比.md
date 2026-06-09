# NAVSIM navtest split闭环评估对比
- **Source**: Table 1
- **Caption**: "在规划导向的NAVSIM navtest split上进行闭环指标对比。C&L表示同时使用相机和激光雷达传感器输入。V8192表示8192个锚点。Hydra-MDP-V8192-W-EP是Hydra-MDP的变体,使用规则评估器额外监督和加权置信度后处理。DiffusionDrive仅从人类演示中学习且无后处理。"

| Method | Input | Img. Backbone | Anchor | NC↑ | DAC↑ | TTC↑ | Comf.↑ | EP↑ | PDMS↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UniAD [16] | Camera | ResNet-34 [13] | 0 | 97.8 | 91.9 | 92.9 | 100 | 78.8 | 83.4 |
| PARA-Drive [45] | Camera | ResNet-34 [13] | 0 | 97.9 | 92.4 | 93.0 | 99.8 | 79.3 | 84.0 |
| LTF [7] | Camera | ResNet-34[13] | 0 | 97.4 | 92.8 | 92.4 | 100 | 79.0 | 83.8 |
| Transfuser [7] | C&L | ResNet-34 [13] | 0 | 97.7 | 92.8 | 92.8 | 100 | 79.2 | 84.0 |
| DRAMA [52] | C&L | ResNet-34 [13] | 0 | 98.0 | 93.1 | 94.8 | 100 | 80.1 | 85.5 |
| VADv2-V8192 [3] | C&L | ResNet-34 [13] | 8192 | 97.2 | 89.1 | 91.6 | 100 | 76.0 | 80.9 |
| Hydra-MDP-V8192 [25] | C&L | ResNet-34 [13] | 8192 | 97.9 | 91.7 | 92.9 | 100 | 77.6 | 83.0 |
| Hydra-MDP-V8192-W-EP [25] | C&L | ResNet-34 [13] | 8192 | 98.3 | 96.0 | 94.6 | 100 | 78.7 | 86.5 |
| DiffusionDrive (Ours) | C&L | ResNet-34[13] | 20 | 98.2 | 96.2 | 94.7 | 100 | 82.2 | 88.1 |
