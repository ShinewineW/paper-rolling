# Claims

## C1: 视频协训练是WAMs性能的主要来源,测试时显式未来想象并非必要
- **Statement**: 视频预测在WAMs中的主要价值在于训练期间改善世界表示,而非在测试时生成未来观测;去除视频协训练目标导致的性能下降远大于去除测试时未来想象所带来的下降
- **Status**: supported
- **Falsification criteria**: 若在移除测试时未来帧生成(如Fast-WAM)相比保留该步骤的变体(如Fast-WAM-Joint或Fast-WAM-IDM)出现显著更大的性能下降,则该主张被证伪;或若去除视频协训练对性能的影响可忽略不计,则同样被证伪
- **Proof**: [E1, E2, E3]
- **Evidence basis**: ['E1', 'E2', 'E3']
- **Interpretation**: 这一发现表明视频联合训练为模型提供了物理世界的隐式先验,使视频DiT学习到具有物理意义的运动和交互结构,而测试时逐步去噪生成未来帧并非产生性能优势的核心因素,可以去除以节省推理成本
- **Tags**: ['causal', 'scoping']

## C2: Fast-WAM在无具身预训练的情况下实现与最先进方法竞争的仿真及真实世界性能
- **Statement**: Fast-WAM在LIBERO和RoboTwin基准上实现了有竞争力的结果,无需依赖其他WAMs使用的具身预训练,表明视频协训练具有强大的数据效率
- **Status**: supported
- **Falsification criteria**: 若Fast-WAM在主要评测基准上的成功率显著低于有具身预训练的对比方法(如LingBot-VA或Motus),则该主张被证伪
- **Proof**: [E1, E2, E3]
- **Evidence basis**: ['E1', 'E2', 'E3']
- **Interpretation**: 视频协训练作为一种可替代具身预训练的学习信号,能够为模型注入充分的物理动态理解能力;Fast-WAM使用Wan2.2-5B视频DiT作为骨干,结合视频协训练目标,在无需大量具身数据预训练的情况下便可达到相近甚至更高的任务成功率
- **Tags**: ['improvement', 'descriptive']

## C3: Fast-WAM推理延迟显著低于imagine-then-execute WAMs,可实现实时机器人控制
- **Statement**: 通过在测试时跳过未来视频生成,Fast-WAM的推理延迟远低于imagine-then-execute WAMs(如Fast-WAM-IDM),速度差距超过4倍,支持实时机器人控制部署
- **Status**: supported
- **Falsification criteria**: 若Fast-WAM在实际部署中的推理延迟高于或接近相比的imagine-then-execute变体,则该主张被证伪
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 去除测试时迭代视频去噪显著减少了推理计算量;Fast-WAM与Fast-WAM-IDM变体之间存在数倍的延迟差距,充分说明测试时未来帧生成是产生高延迟的主要原因,去除后可大幅提升实时部署可行性
- **Tags**: ['improvement', 'descriptive']

## C4: 保留视频协训练的变体之间性能相近,均显著优于去除视频协训练的变体
- **Statement**: 在LIBERO、RoboTwin两个基准以及真实世界任务上,Fast-WAM与Fast-WAM-Joint和Fast-WAM-IDM之间的性能差异远小于去除视频协训练后的性能下降幅度,这一规律在所有评测设置中保持一致
- **Status**: supported
- **Falsification criteria**: 若Fast-WAM与任意一个imagine-then-execute变体之间的性能差距大于Fast-WAM与Fast-WAM-w.o.-video-co-train之间的差距,则该主张被证伪
- **Proof**: [E1, E2, E3]
- **Evidence basis**: ['E1', 'E2', 'E3']
- **Interpretation**: 受控对比设计有效隔离了「测试时未来想象」与「训练期视频协训练」这两个在先前WAMs中通常耦合的因素,清晰表明训练时的视频建模目标是WAM性能增益的主要来源,而非测试时的未来帧生成方式
- **Tags**: ['causal', 'descriptive']
