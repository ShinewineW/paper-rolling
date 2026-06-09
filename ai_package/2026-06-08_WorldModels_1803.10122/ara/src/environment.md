# Environment
- **Python**: 论文未明确指定Python版本
- **Framework**: 论文未明确指定深度学习框架；网页交互演示使用deeplearn.js（Google PAIR团队开发的浏览器端硬件加速机器学习框架）
- **Hardware**: Google Cloud Platform提供的Ubuntu虚拟机；VAE和MDN-RNN训练使用单GPU（训练时间低于一小时）；CMA-ES在单机64核CPU并行运行
- **Key dependencies**: OpenAI Gym (Brockman et al., 2016), VizDoom (Kempka et al., 2016), CMA-ES (Hansen, 2016), deeplearn.js（仅用于网页演示，非训练环境）
- **Random seeds**: CMA-ES每个个体使用16个不同随机初始种子评估适应度（取均值作为适应度值）；CarRacing最优个体最终使用1024次随机回放评估
