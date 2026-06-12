# Minecraft 智能体实验设置比较
- **Source**: Table 3
- **Caption**: "不同 Minecraft 智能体实验设置比较。Dreamer 4 被定位为纯离线经验学习，并使用高分辨率图像输入和低层键鼠动作。"

| Agent | Inputs | Actions | Data Offline | Data Web | Data Online |
| --- | --- | --- | --- | --- | --- |
| Dreamer 3 | 64×64, inventory | keyboard, camera, abstract crafting |  |  | 1.4K |
| VPT (RL) | 128×128 | keyboard, mouse | 2.5K | 270K | 194K |
| VPT (BC) | 128×128 | keyboard, mouse | 2.5K | 270K |  |
| Dreamer 4 | 360×640 | keyboard, mouse | 2.5K | 一 | 一 一 |
