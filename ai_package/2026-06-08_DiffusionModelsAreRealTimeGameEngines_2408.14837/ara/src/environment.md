# Environment
- **Python**: 论文未明确指定 Python 版本
- **Framework**: 论文未明确指定深度学习框架；RL 智能体使用 Stable Baselines 3 训练（CPU，基于 PyTorch）；生成模型在 TPU-v5e 上训练，底层框架论文未显式声明
- **Hardware**: {'inference': '单块 TPU-v5（每步去噪耗时 10ms，自编码器评估耗时 10ms）', 'training_generative': '128 块 TPU-v5e（数据并行）', 'training_agent': 'CPU（通过 Stable Baselines 3 基础设施）'}
- **Key dependencies**: Stable Diffusion v1.4（Rombach et al., 2022）, ViZDoom（Wydmuch et al., 2019）, Stable Baselines 3（Raffin et al., 2021）, PPO（Schulman et al., 2017）, DDIM（Song et al., 2020）, Adafactor（Shazeer & Stern, 2018）, v-prediction 参数化（Salimans & Ho, 2022）
- **Random seeds**: 论文未报告随机种子
