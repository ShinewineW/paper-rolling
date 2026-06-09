# Environment
- **Python**: 论文未说明具体Python版本
- **Framework**: 论文未说明具体深度学习框架(论文网站提供公开实现)
- **Hardware**: 每个agent使用单张Nvidia A100 GPU;Minecraft实验额外使用64个远程CPU worker进行并行环境采样
- **Key dependencies**: MineRL v0.4.4(Minecraft实验环境), Minecraft版本1.11.2(Minecraft实验环境)
- **Random seeds**: 大多数基准每个算法运行5个随机种子;ProcGen因计算限制仅使用1个;BSuite按基准要求使用10个;Minecraft使用10个以可靠统计钻石发现率
