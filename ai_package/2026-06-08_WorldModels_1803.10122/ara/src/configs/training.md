## 随机策略数据收集量
- **Value**: 10000 rollouts
- **Rationale**: 用随机策略探索环境，收集足够多样的观察帧以训练VAE和MDN-RNN
- **Search range**: 论文两个任务均固定为10000，未作对比消融
- **Sensitivity**: 中等；数据不足会导致VAE学到不完整的潜在空间表征
- **Source**: Sec 3.1, Sec 4.2

## VAE训练轮数
- **Value**: 1 epoch
- **Rationale**: 单GPU单次遍历数据即可收敛，训练时间不足一小时；论文称无需耗尽超参调整即可获得满意结果
- **Search range**: 论文仅报告1 epoch，未对比多轮
- **Sensitivity**: 低；论文明确说明单轮已足够
- **Source**: Appendix A.1，脚注3

## MDN-RNN训练轮数
- **Value**: 20 epochs
- **Rationale**: 序列预测任务需要多次遍历数据以充分学习时序依赖关系
- **Search range**: 论文两个任务均固定为20 epochs
- **Sensitivity**: 中等
- **Source**: Appendix A.2

## CMA-ES种群规模
- **Value**: 64
- **Rationale**: 在数百至千余参数的解空间规模下足够维持种群多样性，同时可在64核机器上完全并行评估
- **Search range**: 论文固定为64
- **Sensitivity**: 中等；种群过小可能导致收敛到局部最优
- **Source**: Appendix A.4

## 每个体适应度评估次数
- **Value**: 16（不同随机初始种子）
- **Rationale**: 通过多次评估取均值降低环境随机性带来的适应度估计噪声
- **Search range**: 论文固定为16
- **Sensitivity**: 高；评估次数越少，适应度方差越大，进化稳定性越低
- **Source**: Appendix A.4

## CMA-ES训练代数（CarRacing）
- **Value**: 1800代
- **Rationale**: 1800代时最优个体在1024次随机回放中平均得分达到900.46，满足解决任务的要求
- **Search range**: 论文报告1800代完成求解
- **Sensitivity**: 中等；取决于任务难度、种群规模及评估次数
- **Source**: Appendix A.4

## VizDoom梦境训练温度参数τ
- **Value**: 1.15
- **Rationale**: 略高于1.0的温度使幻梦环境更具挑战性，防止控制器利用世界模型的缺陷学到无法迁移的对抗性策略
- **Search range**: 论文对比了0.10、0.50、1.00、1.15、1.30
- **Sensitivity**: 极高；τ=0.10时模型发生模式崩溃，真实环境得分仅193±58；τ=1.15时真实环境得分最高
- **Source**: Sec 4.5, Table 2, Appendix A.5

## VAE训练损失
- **Value**: L2重建损失 + KL散度损失
- **Rationale**: L2损失衡量重建质量；KL损失将潜在空间约束为高斯先验，提升对MDN-RNN生成z向量时的鲁棒性
- **Search range**: 标准VAE训练目标，两项权重论文未详细说明
- **Sensitivity**: 中等；KL约束过强会丢失信息，过弱则潜在空间结构不规则
- **Source**: Appendix A.1
