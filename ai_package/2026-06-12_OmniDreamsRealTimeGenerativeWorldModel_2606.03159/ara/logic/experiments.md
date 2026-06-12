# Experiments

## E1: 单视角与多视角实时推理计时实验
- **Verifies**: C1
- **Setup**:
  - Model: OmniDreams-SV 与 OmniDreams-MV
  - Hardware: NVIDIA GB300
  - Dataset: 闭环推理配置使用论文中的驾驶视频分块设置
  - System: FlashDreams 推理栈、流式 KV cache、CUDA Graphs、LightTAE 解码与上下文并行
- **Procedure**:
  1. 在固定分辨率下运行已蒸馏的少步扩散模型。
  2. 分别测量世界场景编码、Diffusion DiT、RGB Decoder、KV-cache update、Total 与 Effective FPS。
  3. 比较不同 GPU 配置下单视角和四视角分块吞吐。
- **Metrics**: ['每分块延迟', 'Effective FPS', 'KV-cache update 热路径外耗时']
- **Expected outcome**: 随着并行资源增加，分块延迟下降，有效帧率上升，并达到实时交互要求。
- **Baselines**: ['较少 GPU 配置', '单视角与四视角部署配置']
- **Dependencies**: ['流式静态形状 KV cache', '局部时间注意力', '轻量编码器与解码器', '多 GPU 上下文并行']

## E2: 训练阶段仿真质量消融
- **Verifies**: C2
- **Setup**:
  - Model: OmniDreams-SV
  - Hardware: 论文未在该实验处单独指定硬件
  - Dataset: RDS-HQ-1M held-out evaluation split
  - System: StyleGAN-V FVD、BEVFormer、LATR 与 Temporal Sampson 评测管线
- **Procedure**:
  1. 从 held-out evaluation split 抽取评测 clips。
  2. 比较 Bidirectional、Causal Diffusion Forcing 与 Distilled Self Forcing 训练阶段。
  3. 在生成帧上计算视频质量、三维车辆检测与车道线指标。
  4. 另比较 Original VAE 与 LightTAE decoder 的质量权衡。
- **Metrics**: ['FVD', 'Temp. Sampson', 'LET-AP', 'LET-APL', 'LET-APH', 'F1', 'x-err. far', 'Cat. Acc.']
- **Expected outcome**: Self Forcing 蒸馏阶段相对因果阶段整体更好；LightTAE decoder 换取速度时带来质量下降。
- **Baselines**: ['Bidirectional AV adapted', 'Causal Diffusion Forcing', 'Distilled Original VAE']
- **Dependencies**: ['高质量蒸馏数据集', 'Self Forcing', 'DMD', 'BEVFormer', 'LATR']

## E3: 长 rollout 分段 FVD 实验
- **Verifies**: C3
- **Setup**:
  - Model: OmniDreams 自回归模型
  - Hardware: 论文未在该实验处单独指定硬件
  - Dataset: real-video front-wide reference distribution
  - System: 分段 FVD 长时程评测
- **Procedure**:
  1. 生成长时程自回归 rollout。
  2. 把每个 rollout 按时间切成连续窗口。
  3. 将每个窗口与同一 real-video front-wide reference distribution 比较。
  4. 比较短上下文教师与 progressive long-context teacher。
- **Metrics**: ['分段 FVD', 'Mean', '△']
- **Expected outcome**: progressive long-context teacher 在各时间窗口和总体退化上低于 short-context teacher。
- **Baselines**: ['Short-context teacher']
- **Dependencies**: ['Self Forcing', '长上下文双向教师', '滚动 KV cache', '局部注意力窗口']

## E4: 闭环 NuRec 与 OmniDreams 策略排序比较
- **Verifies**: C4
- **Setup**:
  - Model: OmniDreams sensor simulator 与 NVIDIA NuRec sensor simulator
  - Hardware: 论文未在该实验处单独指定硬件
  - Dataset: Physical AI Autonomous Vehicles NuRec dataset subset
  - System: AlpaSim 闭环栈，多个 Alpamayo 1.5 相机配置与 OmniDreams WAM 策略
- **Procedure**:
  1. 固定 AlpaSim、交通与物理服务以及每个场景初始状态。
  2. 只在 NuRec 与 OmniDreams 之间替换 sensor simulator。
  3. 对多个策略类别执行闭环 rollout。
  4. 比较 All Incidents 及不同 incident 类型下的相对策略排名。
- **Metrics**: ['All Incidents', 'Collision Front', 'Collision Lateral', 'Collision Rear', 'Offroad']
- **Expected outcome**: 切换到 OmniDreams 后策略相对排名应保持一致。
- **Baselines**: ['NVIDIA NuRec', 'Alpamayo 1.5 4 cameras', 'Alpamayo 1.5 2 cam', 'Alpamayo 1.5 1 cam']
- **Dependencies**: ['AlpaSim', 'NuRec reconstructions', 'world-scenario map', 'Alpamayo 1.5 protocol']

## E5: OmniDreams WAM 闭环策略评测
- **Verifies**: C5
- **Setup**:
  - Model: OmniDreams WAM 与 Alpamayo 1.5
  - Hardware: 论文未在该实验处单独指定硬件
  - Dataset: Physical AI Autonomous Vehicles NuRec dataset
  - System: AlpaSim closed-loop stack
- **Procedure**:
  1. 将 OmniDreams-SV checkpoint 微调为端到端 trajectory predictor。
  2. 在原 Alpamayo 1.5 协议下评测同一 WAM checkpoint。
  3. 排除 WAM 训练中使用过的场景。
  4. 比较碰撞相关闭环指标和参数规模。
- **Metrics**: ['Collision', 'collision_front', 'collision_lateral', 'collision_rear', 'parameter count']
- **Expected outcome**: OmniDreams WAM 的碰撞相关指标低于 Alpamayo 1.5，并使用更少参数。
- **Baselines**: ['Alpamayo 1.5']
- **Dependencies**: ['OmniDreams causal DiT backbone', 'DINOv2 encoder features', 'front-wide camera', 'front-telescope camera', 'flow matching trajectory head']
