## 优化器
- **Value**: AdamW
- **Rationale**: 遵循Transfuser基线的训练配置
- **Search range**: 论文未说明其他备选
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 学习率
- **Value**: 6×10^{-4}
- **Rationale**: 遵循Transfuser基线的训练超参数设置
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 总批量大小
- **Value**: 512
- **Rationale**: 在8块GPU上进行分布式训练的总批量大小
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 训练轮数（NAVSIM）
- **Value**: 100
- **Rationale**: 在NAVSIM navtrain数据集上从头训练的总轮数
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 训练轮数（nuScenes第二阶段）
- **Value**: 10
- **Rationale**: 在nuScenes数据集上替换规划模块后的第二阶段微调轮数
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 中
- **Source**: Appendix A

## 训练锚点数量（N_anchor，NAVSIM）
- **Value**: 20
- **Rationale**: 通过K-Means聚类训练集轨迹得到的先验锚点数量，相比VADv2的8192个锚点减少400倍，同时具备更好的多模式分布覆盖能力
- **Search range**: 论文未直接对训练锚点数进行消融；对比参照VADv2的8192与Hydra-MDP的8192
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 训练锚点数量（N_anchor，nuScenes）
- **Value**: 18
- **Rationale**: 在nuScenes数据集上基于SparseDrive基线设置的锚点数量
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 高
- **Source**: Sec 4.7

## 截断扩散步数（T_trunc/T）
- **Value**: 50/1000
- **Rationale**: 将完整1000步扩散噪声调度截断至前50步，仅在锚点附近添加少量高斯噪声以形成锚定高斯分布
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 训练硬件
- **Value**: 8块NVIDIA 4090 GPU
- **Rationale**: 分布式训练所用硬件配置
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.2
