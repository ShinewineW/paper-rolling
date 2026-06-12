# Minecraft 世界模型比较
- **Source**: Table 1
- **Caption**: "Minecraft 世界模型比较。Dreamer 4 被报告为能准确模拟多种物体交互和游戏机制，并在保持实时交互推理的同时扩展上下文长度。"

| Model | Parameters | Resolution | Context | FPS | Success |
| --- | --- | --- | --- | --- | --- |
| MineWorld | 1.2B | 384×224 | 0.8s | 2 |  |
| Lucid-v1 | 1.1B | 640×360 | 1.0s | 44 | 0/16 |
| Oasis (small) | 500M | 640×360 | 1.6s | 20 | 0/16 |
| Oasis (large) | 一 | 360×360 | 1.6s | ~5 | 5/16 |
| Dreamer 4 | 2B | 640×360 | 9.6s | 21 | 14/16 |
