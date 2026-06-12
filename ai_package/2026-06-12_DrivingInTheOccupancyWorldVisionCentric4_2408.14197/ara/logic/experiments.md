# Experiments

## E1: 4D占用与流预测主实验
- **Verifies**: C1
- **Setup**:
  - Model: Drive-OccWorldA与Drive-OccWorldP
  - Hardware: 论文主实验硬件未在对应小节单独说明；实现细节说明训练使用8 NVIDIA A100 GPUs
  - Dataset: nuScenes、nuScenes-Occupancy、Lyft-Level5
  - System: 使用历史多视角相机图像预测未来占用和3D backward centripetal flow，并按Cam4DOcc相关协议比较
- **Procedure**:
  1. 在nuScenes与Lyft-Level5上评估膨胀GMO和流预测。
  2. 在nuScenes-Occupancy上评估细粒度GMO以及细粒度GMO和GSO预测。
  3. 与SPC、OpenOccupancy-C、PowerBEV-3D、CONet-C、Cam4DOcc等基线比较。
- **Metrics**: ['mIoUc', 'mIoUf', 'mIoU f', 'VPQf']
- **Expected outcome**: Drive-OccWorld相对既有方法在当前、未来和流预测指标上更好。
- **Baselines**: ['SPC', 'OpenOccupancy-C', 'PowerBEV-3D', 'CONet-C', 'Cam4DOcc']
- **Dependencies**: ['Table 1', 'Table 2']

## E2: 动作条件与注入接口消融
- **Verifies**: C2, C4
- **Setup**:
  - Model: Drive-OccWorld及其动作条件变体
  - Hardware: 论文未在该实验处单独说明硬件
  - Dataset: nuScenes相关占用预测设置
  - System: 向world decoder注入轨迹、速度、转角、命令或预测轨迹等动作条件，并比较不同接口
- **Procedure**:
  1. 以无动作条件或基础条件作为对照。
  2. 分别注入traj、vel、angle、cmd以及预测轨迹条件。
  3. 比较addition、cross-attention和Fourier Embed等条件接口。
  4. 观察动作条件对预测质量和可控生成的影响。
- **Metrics**: ['mIoUc', 'mIoUf', 'VPQ', 'VPQf', 'L2', 'Collision']
- **Expected outcome**: 加入动作条件、使用cross-attention和Fourier Embed时整体表现更好；使用GT trajectory时规划上界更好。
- **Baselines**: ['无动作条件', 'addition接口', 'Pred trajectory']
- **Dependencies**: ['Table 3', 'Table 4', 'Table 7']

## E3: 端到端规划与占用代价消融
- **Verifies**: C3
- **Setup**:
  - Model: Drive-OccWorldP及占用代价规划器
  - Hardware: 论文未在该实验处单独说明硬件
  - Dataset: nuScenes开放环规划评估
  - System: 世界模型连续预测未来状态，规划器基于agent、road、volume成本和BEV refinement选择轨迹
- **Procedure**:
  1. 按ST-P3与UniAD相关协议报告NoAvg和TemAvg规划结果。
  2. 与NMP、SA-NMP、FF、EO、ST-P3、UniAD、VAD-Base、OccNet、Drive-WM、BEV-Planner等方法比较。
  3. 移除不同occupancy-based cost factors或BEV refinement进行消融。
- **Metrics**: ['L2', 'Collision']
- **Expected outcome**: Drive-OccWorldP的规划误差和碰撞率整体更低，各代价因子和BEV refinement对安全规划有正向贡献。
- **Baselines**: ['NMP', 'SA-NMP', 'FF', 'EO', 'ST-P3', 'UniAD', 'VAD-Base', 'OccNet', 'Drive-WM', 'BEV-Planner', '移除Agent成本', '移除Road成本', '移除Volume成本', '移除BEV Refine']
- **Dependencies**: ['Table 5', 'Table 8']

## E4: 条件归一化、历史记忆与语义损失消融
- **Verifies**: C4, C5
- **Setup**:
  - Model: Drive-OccWorld消融变体
  - Hardware: Table 9 latency measurements are conducted on an A6000 GPU；训练实现细节使用8 NVIDIA A100 GPUs
  - Dataset: nuScenes相关占用预测设置
  - System: 默认消融使用一个历史帧和当前图像预测两个未来时间戳的膨胀GMO
- **Procedure**:
  1. 分别开关semantic、ego-motion、agent-motion条件归一化。
  2. 改变历史帧数量、当前帧数量和memory queue长度，并记录延迟。
  3. 比较Cross Entropy、Binary Occupancy和Lovasz语义损失组合。
- **Metrics**: ['mIoUc', 'mIoUf', 'VPQ', 'Latency']
- **Expected outcome**: 条件归一化、更多历史信息、更长记忆队列和更多语义监督通常提升预测质量，但历史编码器带来更高延迟。
- **Baselines**: ['无对应条件归一化', '较少历史输入', '较短memory queue', '较少语义损失']
- **Dependencies**: ['Table 6', 'Table 9', 'Table 10']
