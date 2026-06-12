# Experiments

## E1: Atari 100k benchmark 中的 world model 代理比较
- **Verifies**: C1
- **Setup**:
  - Model: DIAMOND 与 SimPLe、TWM、IRIS、DreamerV3、STORM
  - Hardware: Nvidia RTX 4090
  - Dataset: Atari 100k benchmark
  - System: 代理完全在 world model imagination 中训练，并在真实环境经验预算后评估
- **Procedure**:
  1. 在 Atari 100k benchmark 的各游戏上从头训练 DIAMOND。
  2. 按论文采用的 human-normalized score 聚合方式计算 Mean 与 IQM。
  3. 将 DIAMOND 与近期完全在 world model 中训练的 baseline 逐游戏和聚合比较。
- **Metrics**: ['raw return', 'human-normalized score', 'Mean HNS', 'IQM', '#Superhuman']
- **Expected outcome**: DIAMOND 的聚合表现应优于 world model baseline，并在若干重视觉细节游戏中更强。
- **Baselines**: ['SimPLe', 'TWM', 'IRIS', 'DreamerV3', 'STORM']
- **Dependencies**: ['Table 1']

## E2: DDPM 与 EDM world model 的长时序稳定性比较
- **Verifies**: C2
- **Setup**:
  - Model: DDPM-based world model 与 EDM-based world model
  - Hardware: 论文未在该小节单独指定硬件
  - Dataset: Breakout expert-policy 静态数据
  - System: 共享网络架构，在相同静态数据上训练并自回归生成 imagined trajectories
- **Procedure**:
  1. 在共享静态数据上训练 DDPM 与 EDM 变体。
  2. 用不同 denoising steps 自回归生成长时序轨迹。
  3. 观察 compounding error 与 out-of-distribution drift，并用附录中的 pixel drift 图进行量化对照。
- **Metrics**: ['average pixel drift', 'trajectory stability', 'visual quality', 'NFE']
- **Expected outcome**: EDM 应比 DDPM 更稳定，尤其在低 denoising steps 下更少漂移。
- **Baselines**: ['DDPM-based world model']
- **Dependencies**: ['Figure 3', 'Figure 8']

## E3: 减少 denoising steps 的定量消融
- **Verifies**: C3
- **Setup**:
  - Model: DIAMOND EDM diffusion world model
  - Hardware: 论文未在该小节单独指定硬件
  - Dataset: DIAMOND 高表现 Atari 游戏子集
  - System: 比较默认多步采样与单步采样对代理表现的影响
- **Procedure**:
  1. 选取 DIAMOND 表现较高的 Atari 游戏。
  2. 将 EDM diffusion world model 的 denoising steps 从默认设置减少到单步。
  3. 比较各游戏 raw return 与聚合 Mean HNS，并结合 Boxing 的质性样例解释模糊预测。
- **Metrics**: ['raw return', 'Mean HNS', 'visual sharpness']
- **Expected outcome**: 减少到单步后总体表现应下降，部分多模态或部分可观测游戏下降更明显。
- **Baselines**: ['DIAMOND default denoising setting']
- **Dependencies**: ['Table 7', 'Figure 4']

## E4: DIAMOND 与 IRIS 的视觉细节一致性比较
- **Verifies**: C4
- **Setup**:
  - Model: DIAMOND 与 IRIS
  - Hardware: 论文未在该小节单独指定硬件
  - Dataset: expert-policy 静态 Atari 数据
  - System: 两个 world model 在相同静态数据上训练并生成连续 imagined frames
- **Procedure**:
  1. 在相同 expert-policy 静态数据上训练 DIAMOND 与 IRIS。
  2. 比较 Asterix、Breakout 和 Road Runner 的连续生成帧。
  3. 检查奖励、敌人、砖块、分数和道路奖励等小视觉元素是否跨帧一致。
  4. 把视觉一致性观察与 Atari benchmark 中相同游戏的代理表现对应起来。
- **Metrics**: ['visual consistency', 'raw return']
- **Expected outcome**: DIAMOND 应生成更一致的关键视觉细节，并在相关游戏上表现更好。
- **Baselines**: ['IRIS']
- **Dependencies**: ['Figure 5', 'Table 1']

## E5: 参数量与训练时间的附加比较
- **Verifies**: C5
- **Setup**:
  - Model: IRIS、DreamerV3 与 DIAMOND
  - Hardware: Nvidia RTX 4090
  - Dataset: Atari 100k benchmark
  - System: 比较模型规模、训练时间和聚合表现，并对 DIAMOND 的训练时间分解做 profiling
- **Procedure**:
  1. 汇总 IRIS、DreamerV3 与 DIAMOND 的参数量、训练天数和 Mean HNS。
  2. 对 DIAMOND 的单次更新、epoch 和完整 run 进行时间分解。
  3. 判断表现提升是否能由更大参数量或更久训练简单解释。
- **Metrics**: ['#parameters', 'Training days', 'Mean HNS', 'update time', 'epoch time', 'run time']
- **Expected outcome**: DIAMOND 应在模型规模较小的同时取得更高 Mean HNS，训练时间介于主要 baseline 之间。
- **Baselines**: ['IRIS', 'DreamerV3']
- **Dependencies**: ['Table 4', 'Table 5']

## E6: 3D environments 的视觉生成质量评估
- **Verifies**: C6
- **Setup**:
  - Model: DIAMOND frame-stack、DIAMOND cross-attention、DreamerV3、IRIS variants
  - Hardware: Nvidia RTX A6000
  - Dataset: CS:GO Clean dataset 与 motorway driving dataset
  - System: 在静态数据上训练 world model，不执行 reinforcement learning；以真实动作序列条件生成视频
- **Procedure**:
  1. 从测试集取真实视频，并生成相同长度的条件视频。
  2. 模型条件包括过去真实帧和真实 action sequence。
  3. 计算 FVD、FID 与 LPIPS，并记录单 GPU 顺序采样速率。
  4. 比较 frame-stack 与 cross-attention 架构以及 DreamerV3、IRIS baseline。
- **Metrics**: ['FID', 'FVD', 'LPIPS', 'Sample rate', 'Parameters']
- **Expected outcome**: DIAMOND frame-stack 应在视觉质量指标上优于 baseline；cross-attention 不应优于 frame-stack。
- **Baselines**: ['DreamerV3', 'IRIS $( K = 1 6 )$', 'IRIS (K = 64)', 'DIAMOND cross-attention']
- **Dependencies**: ['Table 8', 'Figure 10', 'Figure 11', 'Figure 12']
