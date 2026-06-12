# Concepts

## DIAMOND
- **Notation**: D_θ、π_φ、R_ψ、V_φ
- **Definition**: DIAMOND 是一种在扩散世界模型中训练的强化学习智能体，核心思想是用图像空间的条件扩散模型直接生成下一帧观察，并让策略在该模型的想象轨迹中学习。
- **Boundary conditions**: DIAMOND 不是单纯的视频生成器；在主实验中它包含下一观察生成、奖励与终止预测、以及在想象中训练的 actor-critic。
- **Related concepts**: ['扩散世界模型', '自回归想象', 'EDM', '奖励与终止模型', '视觉细节一致性']

## 扩散世界模型
- **Notation**: p(x_next | x_past, a_past)、x_t^τ、x_t^0
- **Definition**: 扩散世界模型是把扩散模型改造成环境动态模型的方法：给定过去观察和动作历史，模型学习条件分布并直接生成下一张图像观察。
- **Boundary conditions**: 它只显式生成观察；奖励和终止在 DIAMOND 主方法中由单独模型 R_ψ 预测，而不是并入扩散模型。
- **Related concepts**: ['Score-based diffusion', '条件生成', '自回归想象', 'POMDP']

## Score-based diffusion
- **Notation**: τ、p^τ、S_θ(x, τ)、D_θ(x^τ, τ)、σ(τ)
- **Definition**: Score-based diffusion 是通过正向加噪过程把数据分布变成可处理先验，再学习反向过程从噪声恢复数据的生成建模框架。
- **Boundary conditions**: 论文采用该框架服务于世界建模，不把它作为策略、规划器或奖励模型来使用。
- **Related concepts**: ['反向扩散', '去噪分数匹配', 'EDM', 'NFE']

## EDM
- **Notation**: F_θ、c_in^τ、c_out^τ、c_noise^τ、c_skip^τ、σ_data
- **Definition**: EDM 是本文选择的扩散范式，使用 Karras et al. 提出的噪声调度、网络预条件和训练目标，使扩散世界模型在少量去噪步骤下更稳定。
- **Boundary conditions**: EDM 的优势在文中主要针对低 NFE、长时间自回归 rollout 的世界建模语境；不能泛化为所有扩散任务都优于 DDPM。
- **Related concepts**: ['网络预条件', '自适应信号噪声混合', 'DDPM', '长时程稳定性']

## DDPM 对照
- **Notation**: β_i、ξ_θ、g(τ)、f(x,τ)
- **Definition**: DDPM 是论文讨论的自然扩散候选，它使用离散噪声调度和噪声预测目标，但在本文低去噪步数设定中出现更严重的自回归漂移。
- **Boundary conditions**: DDPM 在本文中是设计选择的比较对象；论文没有把 DDPM 作为最终 DIAMOND 的主模型。
- **Related concepts**: ['EDM', '复合误差', '去噪步数', '长时程稳定性']

## 自回归想象
- **Notation**: x_past^0、a_past、x_t^τ、x_t^0、π_φ
- **Definition**: 自回归想象指策略在学习到的世界模型里选择动作，扩散模型生成下一观察，然后该预测观察和动作被加入历史条件，用于后续时间步生成。
- **Boundary conditions**: 它不同于一次性生成完整视频块；本文主方法按环境时间逐步生成下一观察。
- **Related concepts**: ['DIAMOND', '扩散世界模型', '复合误差', 'NFE']

## NFE 与去噪步数
- **Notation**: NFE、n、Euler、Heun、Euler-Maruyama
- **Definition**: NFE 表示生成一个样本所需的网络前向调用次数；在扩散世界模型中，去噪步数直接决定推理成本，并影响下一帧视觉质量。
- **Boundary conditions**: 更多去噪步骤通常提高视觉质量，但不是无成本改进；在智能体训练中成本会按想象轨迹长度累积。
- **Related concepts**: ['采样质量', '推理成本', 'EDM', '单步采样', '多步采样']

## 单步采样与多步采样
- **Notation**: n、x_t^τ→x_t^0
- **Definition**: 单步采样是在极少去噪调用下直接预测下一观察；多步采样通过迭代去噪把生成推向某个具体模式。
- **Boundary conditions**: 单步采样在某些确定性更强的游戏中可能稳定，但论文最终不是把它作为所有实验的默认选择。
- **Related concepts**: ['多模态观察分布', '部分可观测性', 'NFE 与去噪步数', 'Boxing']

## 视觉细节一致性
- **Notation**: image-space observation、64×64
- **Definition**: 视觉细节一致性指世界模型在连续帧中稳定保留小目标、奖励、敌人、砖块和分数等对策略有影响的像素级信息。
- **Boundary conditions**: 这是论文的定性解释和对照分析，不等同于对所有游戏性能差异的唯一因果证明。
- **Related concepts**: ['离散潜变量压缩', 'IRIS', 'DIAMOND', '强化学习性能']

## 离散潜变量压缩
- **Notation**: discrete latents、tokens、K
- **Definition**: 离散潜变量压缩是许多近期世界模型用离散表示建模环境动态的做法，它有助于减少长时程复合误差，但可能丢失重建质量和任务相关细节。
- **Boundary conditions**: 论文并未否认离散潜变量的稳定性收益；其批评集中在视觉细节和重建保真度的潜在损失。
- **Related concepts**: ['IRIS', 'DreamerV3', '视觉细节一致性', '扩散世界模型']

## Frame stacking 条件机制
- **Notation**: concat[x_t^τ, x_past^0]、U-Net 2D、Adaptive Group Normalization
- **Definition**: Frame stacking 是本文主方法中观察条件化的方式：把过去观察与当前带噪下一帧一起输入 U-Net 2D，并结合动作和扩散时间条件。
- **Boundary conditions**: Frame stacking 只提供有限历史记忆；论文把更长时记忆和更可扩展的时间建模留作未来方向。
- **Related concepts**: ['扩散世界模型', 'U-Net 2D', '动作条件化', 'Cross-attention']

## 奖励与终止模型
- **Notation**: R_ψ、r_t、d_t、LSTM
- **Definition**: 奖励与终止模型 R_ψ 是与扩散观察模型分开的预测器，用 CNN 和 LSTM 根据帧与动作序列预测奖励和 episode 终止。
- **Boundary conditions**: 论文明确将它与扩散模型分开；把奖励或终止整合进扩散模型被列为未来工作。
- **Related concepts**: ['DIAMOND', 'actor-critic', '想象训练', 'POMDP']

## CS:GO 神经游戏引擎
- **Notation**: CS:GO、Dust II、upsampler、keyboard and mouse
- **Definition**: 论文把 DIAMOND 的扩散世界模型单独训练在 Counter-Strike: Global Offensive 的静态 gameplay 数据上，使其成为可交互的神经游戏引擎。
- **Boundary conditions**: 该部分不进行强化学习或在线数据收集；论文也说明少见地图区域、遮挡和有限记忆会导致漂移或状态遗忘。
- **Related concepts**: ['扩散世界模型', '图像空间生成', '离线数据限制', '长时程漂移']
