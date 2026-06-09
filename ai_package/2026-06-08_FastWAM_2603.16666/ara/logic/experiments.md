# Experiments

## E1: RoboTwin 2.0双臂操控基准多变体受控对比实验
- **Verifies**: C1, C2, C4
- **Setup**:
  - Model: Fast-WAM(6B总参数;骨干为Wan2.2-5B视频DiT;动作专家DiT隐藏维度da=1024,约1B参数;动作时域h=32;视频帧时间下采样4×,每块9帧)
  - Hardware: NVIDIA RTX 5090D V2 32GB GPU
  - Dataset: RoboTwin 2.0(2500条干净场景演示加25000条场景随机化演示,覆盖50+任务)
  - System: 多任务双臂操控仿真基准,包含干净(Clean)和场景随机化(Rand.)两种评测设置
- **Procedure**:
  1. 以多任务方式混合训练全部演示数据,共训练30k步
  2. 在干净场景和随机化场景下分别对每个任务运行100次试验
  3. 记录各任务成功率并计算平均成功率
- **Metrics**: ['干净场景平均成功率(%)', '随机化场景平均成功率(%)', '总体平均成功率(%)']
- **Expected outcome**: Fast-WAM在无具身预训练情况下达到与有预训练WAMs相近的成绩;Fast-WAM与两个imagine-then-execute变体(Fast-WAM-Joint和Fast-WAM-IDM)之间的差距远小于去除视频协训练后的下降幅度
- **Baselines**: ['πo', 'π0.5', 'Motus(有具身预训练)', 'LingBot-VA(有具身预训练)', 'LingBot-VA from WAN2.2(无预训练)', 'Fast-WAM-Joint', 'Fast-WAM-IDM', 'Fast-WAM w.o. video co-train']
- **Dependencies**: ['Wan2.2-5B预训练权重', 'RoboTwin 2.0评测框架']

## E2: LIBERO四套件仿真基准多变体受控对比实验
- **Verifies**: C1, C2, C4
- **Setup**:
  - Model: Fast-WAM(与E1相同配置)
  - Hardware: NVIDIA RTX 5090D V2 32GB GPU
  - Dataset: LIBERO(四个suite:Spatial、Object、Goal、Long,各含500条演示共10任务)
  - System: 仿真机器人操控基准,覆盖空间关系、物体识别、目标条件化及长时程多步任务
- **Procedure**:
  1. 在各LIBERO suite上分别训练20k步
  2. 在40个任务上使用不同随机种子评测,共2000次试验
  3. 记录各suite成功率及平均成功率
- **Metrics**: ['LIBERO-Spatial成功率(%)', 'LIBERO-Object成功率(%)', 'LIBERO-Goal成功率(%)', 'LIBERO-Long成功率(%)', '平均成功率(%)']
- **Expected outcome**: Fast-WAM无具身预训练下达到与LingBot-VA、Motus等有预训练方法相近的整体性能;去除视频协训练后在Spatial和Long子集上出现更明显的下降;Fast-WAM与两个imagine-then-execute变体的差距小于无视频协训练变体的差距
- **Baselines**: ['OpenVLA', 'πo', 'π0.5', 'LingBot-VA(有具身预训练)', 'Motus(有具身预训练)', 'Fast-WAM-Joint', 'Fast-WAM-IDM', 'Fast-WAM w.o. video co-train']
- **Dependencies**: ['Wan2.2-5B预训练权重', 'LIBERO评测框架']

## E3: 真实世界长时程毛巾折叠任务性能与推理效率评估
- **Verifies**: C1, C2, C3, C4
- **Setup**:
  - Model: Fast-WAM及其变体
  - Hardware: NVIDIA RTX 5090D V2 32GB GPU加Galaxea R1 Lite机器人平台
  - Dataset: 60小时遥控操作演示(毛巾折叠任务)
  - System: 真实世界长时程可变形物体操控任务,要求策略具备长时程规划与精确闭环控制能力
- **Procedure**:
  1. 在毛巾折叠演示上训练所有模型30k步
  2. 评估平均任务成功率和平均任务完成时间
  3. 在单台NVIDIA RTX 5090D V2 GPU上测量各方法的推理延迟
- **Metrics**: ['平均成功率(%)', '平均任务完成时间', '推理延迟(ms)']
- **Expected outcome**: Fast-WAM实现远低于imagine-then-execute变体的推理延迟;所有保留视频协训练的Fast-WAM变体均显著优于无具身预训练的π0.5;去除视频协训练导致成功率和完成时间均出现更大幅度的恶化
- **Baselines**: ['π0.5(无具身预训练)', 'Fast-WAM-Joint', 'Fast-WAM-IDM', 'Fast-WAM w.o. video co-train']
- **Dependencies**: ['Wan2.2-5B预训练权重', 'Galaxea R1 Lite机器人平台']
