# Related Work

## R1: Diffuser [37]
- **DOI**: 
- **Type**: 规划扩散基线
- **Delta**:
  - What changed: 论文将full-sequence diffusion规划替换为因果Diffusion Forcing，并在采样时让远未来保持更高不确定性，还加入MCG来优化未来结果分布上的期望奖励。
  - Why: Diffuser按相同噪声水平处理整条轨迹，且实现中依赖手工PD controller而忽略生成动作；本文要验证因果一致动作生成和不同噪声日程的价值。
- **Claims affected**: ['C1']
- **Adopted elements**: ['D4RL迷宫规划设置', 'goal-based planning convention', 'Diffuser作为主要基线']

## R2: Diffusion policy [10]
- **DOI**: 
- **Type**: 机器人模仿学习基线
- **Delta**:
  - What changed: 论文把无记忆的action diffusion策略扩展为带潜状态记忆的Diffusion Forcing策略，使同一模型可在长程非马尔可夫任务中利用历史。
  - Why: 水果换位任务中当前观察无法唯一决定下一步动作，作者用该基线凸显记忆机制的必要性。
- **Claims affected**: ['C3']
- **Adopted elements**: ['imitation learning setting', 'action generation comparison']

## R3: TimeGrad [50]
- **DOI**: 
- **Type**: 时间序列扩散基线
- **Delta**:
  - What changed: 论文将teacher forcing训练的next-token diffusion时间序列模型作为主要比较对象，评估独立每token噪声水平的Diffusion Forcing目标是否造成通用预测退化。
  - Why: TimeGrad与本文同属扩散式时间序列建模，适合作为新训练目标的直接基线。
- **Claims affected**: ['C4']
- **Adopted elements**: ['covariates convention', 'CRPS_sum benchmark comparison']

## R4: Transformer-MAF [51]
- **DOI**: 
- **Type**: 概率时间序列基线
- **Delta**:
  - What changed: 论文在相同GluonTS设置中与transformer-based normalizing flow方法比较，展示Diffusion Forcing作为通用序列模型的竞争性。
  - Why: 该工作是高维多变量概率预测中的强基线，可检验本文方法是否只适合规划和视频。
- **Claims affected**: ['C4']
- **Adopted elements**: ['covariate construction reference', 'time series benchmark']

## R5: ScoreGrad sub-VP SDE [68]
- **DOI**: 
- **Type**: 时间序列扩散基线
- **Delta**:
  - What changed: 论文把ScoreGrad作为强扩散预测基线，并承认Diffusion Forcing整体与其接近但在Wikipedia上不是最优。
  - Why: 该比较限定了本文时间序列主张的强度，即竞争性而非所有数据集绝对领先。
- **Claims affected**: ['C4']
- **Adopted elements**: ['diffusion-based time series comparison']

## R6: Video diffusion models [32]
- **DOI**: 
- **Type**: 视频生成扩散相关工作
- **Delta**:
  - What changed: 论文针对长视频生成中full-sequence diffusion常用sliding window的问题，展示CDF可用因果滚动和稳定化采样延伸到训练视野之外。
  - Why: 该相关工作代表视频扩散路线，帮助定位本文在长滚动稳定性上的差异。
- **Claims affected**: ['C2']
- **Adopted elements**: ['video generation comparison framing']

## R7: Teacher forcing [65]
- **DOI**: 
- **Type**: next-token训练范式
- **Delta**:
  - What changed: 论文从teacher forcing的next-token预测出发，引入每token独立噪声水平，使模型不只预测立即下一个干净token，而能按任意噪声日程去噪序列。
  - Why: teacher forcing是本文要结合并突破的自回归训练基础，也用于视频next-frame diffusion基线。
- **Claims affected**: ['C2', 'C4']
- **Adopted elements**: ['next-token prediction framing', 'teacher forcing baseline']
