# GAIA-1三组件模型配置与训练规格
- **Source**: Section 4.1, Section 4.2, Section 4.3
- **Caption**: "GAIA-1三个可训练组件的参数量、训练步数、训练时长、批大小及GPU配置（数字逐字来自论文Section 4.1/4.2/4.3）"

| 组件 | 参数量 | 训练步数 | 训练时长 | 批大小 | GPU配置 |
| --- | --- | --- | --- | --- | --- |
| 图像标记器 | 0.3B | 200k steps | 4 days | 160 | 32 A100 80GB GPUs |
| 世界模型 | 6.5B | 100k steps | 15 days | 128 | 64 A100 80GB GPUs |
| 视频解码器 | 2.6B | 300k steps | 15 days | 64 | 32 A100 80GB GPUs |
