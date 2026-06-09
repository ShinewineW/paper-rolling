# Related Work

## R1: Blattmann et al., 2023 (VideoLDM) [2]
- **DOI**: 
- **Type**: 基础架构借鉴
- **Delta**:
  - What changed: Drive-WM 在 VideoLDM 的时序层插入范式基础上增加多视角注意力层，实现多摄像头联合时空建模
  - Why: VideoLDM 提供了「冻结空间层、微调时序层」的分阶段视频扩散训练范式，被 Drive-WM 直接沿用
- **Claims affected**: ['C1']
- **Adopted elements**: ['时序层插入方式', 'DDIM 采样策略', '分阶段微调流程（先图像后视频）']

## R2: Rombach et al., 2022 (Stable Diffusion) [44]
- **DOI**: 
- **Type**: 预训练基础模型
- **Delta**:
  - What changed: Drive-WM 以 Stable Diffusion 权重初始化空间参数，在此基础上微调时序层与多视角层
  - Why: 强大的图像生成先验大幅降低训练成本并提升生成质量
- **Claims affected**: ['C1']
- **Adopted elements**: ['预训练图像扩散权重初始化']

## R3: Gao et al., 2023 (MagicDrive) [17]
- **DOI**: 
- **Type**: 同期基线对比
- **Delta**:
  - What changed: Drive-WM 相比 MagicDrive 额外引入时序层实现视频生成，并提出分解式多视角建模以提升视角一致性
  - Why: MagicDrive 是同期最强的多视角图像生成基线，是 FID 对比中的主要竞争者
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: []

## R4: Wang et al., 2023 (DriveDreamer) [63]
- **DOI**: 
- **Type**: 单视角视频基线
- **Delta**:
  - What changed: Drive-WM 将单视角驾驶视频生成扩展至多视角，并在 FID/FVD 上大幅超越 DriveDreamer
  - Why: DriveDreamer 是并行工作中代表性的单视角动作条件化驾驶扩散视频生成方法
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R5: Kim et al., 2021 (DriveGAN) [31]
- **DOI**: 
- **Type**: 早期单视角视频基线
- **Delta**:
  - What changed: Drive-WM 采用扩散模型取代 GAN，在 FID 和 FVD 上均远优于 DriveGAN
  - Why: DriveGAN 是使用 GAN 进行可控驾驶神经仿真的代表性早期工作
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R6: Jiang et al., 2023 (VAD) [30]
- **DOI**: 
- **Type**: 集成规划组件
- **Delta**:
  - What changed: Drive-WM 将 VAD 作为候选轨迹生成器，通过图像奖励函数替代 VAD 的随机指令选取，提供更优的轨迹筛选
  - Why: VAD 是主流的向量化端到端规划方法，其随机指令选取在 OOD 场景下安全性不足
- **Claims affected**: ['C4', 'C5']
- **Adopted elements**: ['规划器候选轨迹采样接口', '自车动作定义方式（Δx, Δy 位移）']

## R7: Hafner et al., 2020 (Dreamer) [20]
- **DOI**: 
- **Type**: 概念来源
- **Delta**:
  - What changed: Drive-WM 将 Dreamer 的潜变量世界模型规划范式迁移至真实驾驶场景像素空间多视角视频，脱离模拟器环境
  - Why: Dreamer 系列奠定了「潜变量世界模型→预测未来状态→规划」的基本范式，但局限于游戏或实验室低分辨率场景
- **Claims affected**: ['C4']
- **Adopted elements**: ['世界模型用于规划的基本思路框架']

## R8: Yang et al., 2023 (BEVControl) [69]
- **DOI**: 
- **Type**: 多视角图像基线
- **Delta**:
  - What changed: Drive-WM 在 mAPobj 和 mIoUbg 等可控性指标上超越 BEVControl，并额外实现视频生成能力
  - Why: BEVControl 是代表性的多视角街景可控图像生成基线，也是可控性评估设计的参考来源
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['可控性评估方案（CVT 分割评估、感知模型量化可控性）']

## R9: Hu et al., 2023 (GAIA-1) [28]
- **DOI**: 
- **Type**: 单视角世界模型基线
- **Delta**:
  - What changed: Drive-WM 扩展至多视角视频生成，而 GAIA-1 仅支持单视角动作条件化视频生成
  - Why: GAIA-1 是同期动作条件化自动驾驶生成世界模型的代表，证明了动作控制生成视频的可行性
- **Claims affected**: ['C1']
- **Adopted elements**: []
