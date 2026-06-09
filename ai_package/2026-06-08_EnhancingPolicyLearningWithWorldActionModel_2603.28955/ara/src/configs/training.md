## 世界模型序列长度
- **Value**: T = 50
- **Rationale**: 长序列使模型能充分学习操作任务中的时序动态结构
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## 世界模型训练批量大小
- **Value**: 500
- **Rationale**: 较大批量可稳定RSSM随机潜变量的梯度估计
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## 世界模型学习率
- **Value**: 3×10^{-4}
- **Rationale**: AdamW常用学习率设置
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## AdamW权重衰减
- **Value**: 0.05
- **Rationale**: 抑制世界模型过拟合
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## KL平衡系数
- **Value**: α = 0.8
- **Rationale**: 平衡先验与后验对KL梯度的贡献比例,沿用DreamerV2设置
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## KL损失权重 λ_KL
- **Value**: 3.0
- **Rationale**: 对KL项适当加权,防止后验坍塌至先验
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 论文指出需仔细调节以平衡重建质量与动作预测
- **Source**: Sec IV.A

## 图像重建损失权重 λ_img
- **Value**: 1.0
- **Rationale**: 作为三项联合损失的参考基准权重
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 论文指出需仔细调节以平衡重建质量与动作预测
- **Source**: Sec IV.A

## 动作预测损失权重 λ_act
- **Value**: 1000.0
- **Rationale**: 动作预测的L1误差数量级远小于图像重建误差,需要大权重才能有效正则化编码器
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 高;论文明确指出需仔细调节以平衡重建质量与动作预测效果
- **Source**: Sec IV.A

## 世界模型训练步数
- **Value**: 230K 梯度步
- **Rationale**: 约为基线DreamerV2(2M步)的1/8.7,在显著更少步数下仍达到更强的下游策略性能
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 高;训练步数直接关系到模型质量与训练效率之间的权衡
- **Source**: Sec IV.A

## BC训练轮数
- **Value**: 5000 epochs
- **Rationale**: 确保扩散策略在专家演示的潜特征上充分收敛
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## BC批量大小
- **Value**: 256
- **Rationale**: 扩散策略BC训练的标准批量设置
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## BC学习率(余弦衰减)
- **Value**: 初始 10^{-4},衰减至 10^{-5}
- **Rationale**: 余弦衰减在训练末期降低学习率以精细调节策略参数
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## BC权重衰减
- **Value**: 10^{-6}
- **Rationale**: 轻量正则化,防止策略网络对少量专家演示过拟合
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## EMA衰减系数
- **Value**: 0.995
- **Rationale**: 指数移动平均可稳定扩散策略的推理时输出分布
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## BC阶段去噪步数 K
- **Value**: 20
- **Rationale**: BC训练时采用完整去噪链以充分学习动作分布
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## 动作预测时域 T_a
- **Value**: 4
- **Rationale**: 每次策略调用生成4步动作块,降低决策频率以提高执行平滑性
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO批量大小
- **Value**: 7500
- **Rationale**: 较大的on-policy批量有助于PPO稳定梯度估计
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO每迭代更新轮数
- **Value**: 10
- **Rationale**: 充分利用每次imagined rollout收集的数据
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO Actor学习率
- **Value**: 10^{-5}
- **Rationale**: 较小学习率防止策略更新步幅过大导致性能崩溃
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO Critic学习率
- **Value**: 10^{-3}
- **Rationale**: Critic需要更快速的更新以准确估计价值函数
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## 折扣因子 γ
- **Value**: 0.999
- **Rationale**: 接近1的折扣系数适合操作任务中奖励延迟较长的情形
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## GAE λ
- **Value**: 0.95
- **Rationale**: 广义优势估计的标准设置,平衡偏差与方差
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO总迭代次数
- **Value**: 800
- **Rationale**: 微调的实验上限,每25次迭代评估一次
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec IV.B

## PPO阶段推理去噪步数
- **Value**: 10
- **Rationale**: imagined rollout中使用较少去噪步数以提高采样吞吐量
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec III.B, Sec IV.B

## BC正则化系数 α_BC
- **Value**: 0.025
- **Rationale**: 在PPO微调期间保留BC先验,防止灾难性遗忘
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec III.B, Sec IV.B

## PPO阶段并行imagined rollout数
- **Value**: 50
- **Rationale**: 足够的rollout多样性保证PPO梯度估计稳定
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 未讨论
- **Source**: Sec III.B, Sec IV.B
