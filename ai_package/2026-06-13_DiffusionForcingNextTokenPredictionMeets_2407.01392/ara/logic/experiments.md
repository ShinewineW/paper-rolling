# Experiments

## E1: D4RL迷宫规划与MCG消融
- **Verifies**: C1
- **Setup**:
  - Model: Diffusion Forcing、Ours wo/ MCG、Diffuser、Diffuser w/ diffused action、MPPI、CQL、IQL
  - Hardware: 论文此处未单独点名硬件；附录D.10说明maze planning可用单张2080Ti训练。
  - Dataset: D4RL Maze2D与Multi2D迷宫环境，数据为随机游走轨迹。
  - System: 离线强化学习规划；用目标位置进行引导，奖励按episode reward报告。
- **Procedure**:
  1. 在每个迷宫环境训练一个Diffusion Forcing模型。
  2. 与MPPI、CQL、IQL、Diffuser及直接执行diffused action的Diffuser变体比较。
  3. 对Diffusion Forcing去掉MCG做消融，比较保留MCG时的结果。
  4. 按Table 1报告各环境episode reward和平均值。
- **Metrics**: ['episode reward', 'single-task average', 'multi-task average']
- **Expected outcome**: 保留MCG的Diffusion Forcing应高于去掉MCG的版本，并在平均奖励上优于列出的主要规划基线。
- **Baselines**: ['MPPI', 'CQL', 'IQL', 'Diffuser*', 'Diffuser w/ diffused action', 'Ours wo/ MCG']
- **Dependencies**: ['D4RL', 'Diffuser [37]', 'MCG', '不同时间步噪声日程']

## E2: Minecraft与DMLab视频长滚动生成
- **Verifies**: C2
- **Setup**:
  - Model: convolutional RNN实现的Causal Diffusion Forcing、next-frame diffusion teacher forcing基线、causal full-sequence diffusion基线
  - Hardware: 附录D.10说明video prediction使用A100 GPU；精确配置见证据表。
  - Dataset: Minecraft gameplay与DMLab navigation视频数据。
  - System: 从未见过的初始帧开始进行自回归视频滚动，并使用Section 3.3提出的稳定化采样。
- **Procedure**:
  1. 在Minecraft和DMLab视频数据上训练CDF和两个共享相同RNN架构的基线。
  2. 采样时从测试初始帧进行自回归滚动。
  3. 比较训练视野内的时序一致性和训练视野外的发散情况。
  4. 用Figure 3及附录非挑选可视化展示结果。
- **Metrics**: ['定性时序一致性', '训练视野外稳定性', '是否发散']
- **Expected outcome**: CDF应比teacher forcing和causal full-sequence diffusion基线更稳定，长滚动中更少出现发散。
- **Baselines**: ['next-frame diffusion teacher forcing', 'causal full-sequence diffusion']
- **Dependencies**: ['Minecraft dataset used by TECO [69]', 'DMLab dataset used by TECO [69]', 'RNN backbone', 'rollout stabilization']

## E3: Franka水果换位长程模仿与观测扰动
- **Verifies**: C3
- **Setup**:
  - Model: Diffusion Forcing、diffusion policy、next-frame diffusion baseline
  - Hardware: Franka robot，VR teleoperation与impedance control采集演示。
  - Dataset: 水果换位机器人演示数据，含手部相机和前方相机视频及机器人手部动作。
  - System: 真实机器人桌面操作，需要根据初始配置记忆决定后续动作，并测试视觉干扰和遮挡。
- **Procedure**:
  1. 收集专家演示并训练Diffusion Forcing完成水果换位。
  2. 与无记忆的diffusion policy比较长程任务成功情况。
  3. 执行时加入视觉干扰或完全遮挡相机。
  4. 比较Diffusion Forcing和next-frame diffusion baseline在扰动下的成功率。
- **Metrics**: ['success rate', '扰动下success rate']
- **Expected outcome**: Diffusion Forcing应在正常和扰动观察条件下都优于无记忆或必须把扰动当作真实观察的基线。
- **Baselines**: ['diffusion policy [10]', 'next-frame diffusion baseline']
- **Dependencies**: ['Franka robot', 'VR teleoperation', 'impedance control', 'Bayes filtering式先验']

## E4: GluonTS多变量概率时间序列预测
- **Verifies**: C4
- **Setup**:
  - Model: Diffusion Forcing与VES、VAR、VAR-Lasso、GARCH、DeepAR、LSTM-Copula、GP-Copula、KVAE、NKF、Transformer-MAF、TimeGrad、ScoreGrad sub-VP SDE
  - Hardware: 附录D.10说明time series实验可用单张2080Ti训练。
  - Dataset: GluonTS的Exchange、Solar、Electricity、Traffic、Taxi、Wikipedia。
  - System: 多变量概率时间序列预测，context window与prediction window设为相同长度，使用与TimeGrad相同的协变量。
- **Procedure**:
  1. 从GluonTS访问各时间序列数据集并构造验证集与测试集。
  2. 使用相同架构和超参数训练Diffusion Forcing。
  3. 在验证集上跟踪CRPS_sum并早停。
  4. 在测试集上估计CRPS_sum并与既有方法比较。
- **Metrics**: ['CRPS_sum']
- **Expected outcome**: Diffusion Forcing应在多个数据集上达到与强基线竞争的CRPS_sum，且并非在所有数据集都最优。
- **Baselines**: ['VES [36]', 'VAR [45]', 'VAR-Lasso [45]', 'GARCH [62]', 'DeepAR [55]', 'LSTM-Copula [54]', 'GP-Copula [54]', 'KVAE [41]', 'NKF [14]', 'Transformer-MAF [51]', 'TimeGrad [50]', 'ScoreGrad sub-VP SDE [68]']
- **Dependencies**: ['GluonTS [2]', 'CRPS_sum', 'quantiles', 'covariates from [50]']
