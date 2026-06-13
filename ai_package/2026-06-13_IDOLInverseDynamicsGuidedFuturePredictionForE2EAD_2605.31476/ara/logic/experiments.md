# Experiments

## E1: NAVSIM v1 navtest 主结果对比
- **Verifies**: C5
- **Setup**:
  - Model: IDOL，ResNet-34 图像骨干，C&L 输入
  - Hardware: NVIDIA RTX 3090
  - Dataset: NAVSIM v1 navtest
  - System: 官方 closed-loop evaluation protocol
- **Procedure**:
  1. 在 NAVSIM v1 navtest 上运行 IDOL。
  2. 按官方 closed-loop 指标计算 NC、DAC、TTC、Comf.、EP 与 PDMS。
  3. 与同一 ResNet-34 image-backbone 设置下的端到端规划方法比较。
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: IDOL 的主规划分数应优于可比学习式基线，同时保持安全与进度相关指标有竞争力。
- **Baselines**: ['VADv2', 'UniAD', 'PARA-Drive', 'TransFuser', 'LAW', 'DiffusionDrive', 'WoTE', 'SeerDrive', 'ResWorld*', 'MeanFuser', 'DiffE2Et']
- **Dependencies**: ['NAVSIM v1', 'ResNet-34', 'TransFuser backbone', 'closed-loop metrics']

## E2: NAVSIM v2 navhard 两阶段主结果对比
- **Verifies**: C5
- **Setup**:
  - Model: IDOL，ResNet34 backbone
  - Hardware: 论文实现细节所述训练与推理配置
  - Dataset: NAVSIM v2 navhard
  - System: two-stage pseudo-simulation protocol
- **Procedure**:
  1. 在 NAVSIM v2 navhard split 上执行 two-stage pseudo-simulation。
  2. 分别记录 Stage 1 与 Stage 2 的闭环扩展指标。
  3. 用最终 EPDMS 与可比方法和 privileged planner 对比。
- **Metrics**: ['NC', 'DAC', 'DDC', 'TLC', 'EP', 'TTC', 'LK', 'HC', 'EC', 'EPDMS']
- **Expected outcome**: IDOL 应在可比学习式方法中取得更高最终 EPDMS，并在困难 navhard 设置下保持闭环鲁棒性。
- **Baselines**: ['PDM-Closed', 'LTF', 'GTRS-DP', 'DiffusionDrive', 'GuideFlow', 'WoTE']
- **Dependencies**: ['NAVSIM v2', 'navhard split', 'pseudo-simulation protocol', 'LTF replacement for unavailable LiDAR in second stage']

## E3: IDM 与闭环细化组件消融
- **Verifies**: C1, C2
- **Setup**:
  - Model: IDOL 组件变体
  - Hardware: 论文实现细节所述训练与推理配置
  - Dataset: NAVSIM navtest
  - System: closed-loop evaluation protocol
- **Procedure**:
  1. 构造无 IDM、加入 IDM、加入闭环细化的 IDOL 变体。
  2. 保持其他设置不变，仅改变 IDM 与 CL iters.。
  3. 比较各变体的 PDMS 及组成指标。
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 加入 IDM 应优于无 IDM；加入适度闭环细化应进一步提升；过多迭代可能回落。
- **Baselines**: ['w/o IDM', 'IDM without CL', 'IDM with CL']
- **Dependencies**: ['NAVSIM navtest', 'IDM', 'closed-loop refinement']

## E4: IDM 时间输入与动态分支设计消融
- **Verifies**: C3, C4
- **Setup**:
  - Model: IDOL 的 IDM 结构变体
  - Hardware: 论文实现细节所述训练与推理配置
  - Dataset: NAVSIM navtest
  - System: closed-loop evaluation protocol
- **Procedure**:
  1. 比较 IDM temporal input 的不同窗口设计。
  2. 分别移除 spatial branch 或 global branch。
  3. 在相同 navtest 设置下比较规划指标。
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 相邻转移输入应优于更长窗口；同时保留空间与全局分支应优于任一单分支变体。
- **Baselines**: ['4 frame', '2 frame', 'w/o spatial branch', 'w/o global branch', 'dual-branch IDM']
- **Dependencies**: ['IDM temporal input', 'spatial dynamics branch', 'global dynamics branch']

## E5: NAVSIM v2 扩展 navtest 与 navhard stage-1-only 对比
- **Verifies**: C5
- **Setup**:
  - Model: IDOL
  - Hardware: 论文实现细节所述训练与推理配置
  - Dataset: NAVSIM v2 navtest 与 NAVSIM-v2 navhard
  - System: extended closed-loop metrics 与 stage-1-only protocol
- **Procedure**:
  1. 在 NAVSIM v2 navtest 上用 extended closed-loop metrics 评测 IDOL。
  2. 在 NAVSIM-v2 navhard stage-1-only protocol 上评测 IDOL。
  3. 与公开论文中的学习式规划器和 human agent 对比。
- **Metrics**: ['NC', 'DAC', 'DDC', 'TLC', 'EP', 'TTC', 'LK', 'HC', 'EC', 'EPDMS']
- **Expected outcome**: IDOL 应在学习式方法中保持领先，并在 navhard stage-1-only 设置下显示稳定收益。
- **Baselines**: ['Human Agent', 'Ego Status MLP', 'TransFuser', 'Hydra-MDP++', 'DriveSuprim', 'ReCogDrive', 'DiffusionDrive', 'GTRS-Dense + SimScale', 'World4Drive', 'Epona', 'DiffusionDriveV2', 'VADv2', 'DriveVLA-W0', 'SGDrive', 'DiffRefiner', 'WorldRFTt', 'SafeDrive', 'MeanFuser', 'LTF', 'WoTE', 'Hydra-MDP+']
- **Dependencies**: ['NAVSIM v2', 'extended closed-loop metrics', 'stage-1-only protocol']

## E6: 转移感知未来建模与全局动态融合消融
- **Verifies**: C1, C4
- **Setup**:
  - Model: IDOL 的未来建模与融合策略变体
  - Hardware: 论文实现细节所述训练与推理配置
  - Dataset: NAVSIM navtest
  - System: closed-loop evaluation protocol
- **Procedure**:
  1. 比较 Future State Only、Latent Difference 与学习式 IDM。
  2. 比较 Additive、Concat-MLP 与 MLN 全局动态融合。
  3. 保持空间分支等其他设置一致，仅替换对应建模或融合操作。
- **Metrics**: ['NC', 'DAC', 'TTC', 'Comf.', 'EP', 'PDMS']
- **Expected outcome**: 学习式 IDM 应优于直接使用未来状态或简单差分；MLN 融合应更有效地整合全局转移信息。
- **Baselines**: ['Future State Only', 'Latent Difference', 'IDM', 'Additive', 'Concat-MLP', 'MLN']
- **Dependencies**: ['imagined future BEV states', 'global dynamics feature', 'MLN']
