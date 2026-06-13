# Experiments

## E1: GM-100 真实世界跨平台对比评估
- **Verifies**: C1, C2
- **Setup**:
  - Model: LingBot-VLA w/o depth、LingBot-VLA w/ depth、WALL-OSS、GR00T N1.6、π0.5
  - Hardware: AgileX、Agibot G1、Galaxea R1Pro 真实机器人平台
  - Dataset: GM-100 后训练数据与相同任务规范
  - System: 相同后训练流水线、相同硬件任务配对、随机顺序测试
- **Procedure**:
  1. 从公开预训练检查点对所有模型进行同一后训练流程。
  2. 在同一 robot unit 与同一 task pair 上顺序测试模型。
  3. 保持物体位置和朝向随机化，并记录第三方视角、机器人状态与模型预测。
  4. 按 Success Rate 与 Progress Score 汇总平台平均与任务明细。
- **Metrics**: ['SR', 'PS']
- **Expected outcome**: LingBot-VLA 变体应在平均任务完成和进展上优于主要基线，w/ depth 在聚合表现上应进一步改善。
- **Baselines**: ['WALL-OSS', 'GR00T N1.6', 'π0.5']
- **Dependencies**: ['Table 1', 'Table S1', 'Table S2', 'Table S3', 'Table S4', 'Table S5', 'Table S6']

## E2: RoboTwin 2.0 仿真多任务评估
- **Verifies**: C2, C3
- **Setup**:
  - Model: LingBot-VLA w/o depth、LingBot-VLA w/ depth、π0.5
  - Hardware: 仿真环境
  - Dataset: RoboTwin 2.0 clean 与 randomized 场景数据
  - System: 从预训练检查点出发，在 RoboTwin 数据上继续微调并评估
- **Procedure**:
  1. 选择 RoboTwin 2.0 中代表性双臂操作任务。
  2. 分别在 clean 与 randomized 设置下训练和评估。
  3. 比较 π0.5、Ours w/o depth 与 Ours w/ depth 的平均成功率和逐任务成功率。
- **Metrics**: ['Average SR', 'Clean SR', 'Rand. SR']
- **Expected outcome**: LingBot-VLA 变体应优于 π0.5，加入深度信息的版本整体方向上更强。
- **Baselines**: ['π0.5']
- **Dependencies**: ['Table 2', 'Table S7']

## E3: 预训练数据规模消融
- **Verifies**: C4
- **Setup**:
  - Model: LingBot-VLA
  - Hardware: Agibot G1、AgileX、Galaxea R1Pro
  - Dataset: 不同规模真实世界预训练数据子集与 GM-100 代表性任务子集
  - System: 保持评估平台和指标一致，改变预训练数据规模
- **Procedure**:
  1. 按预训练数据规模构造多个训练设置。
  2. 在代表性真实世界任务上评估各设置。
  3. 比较 Progress Rate 与 Success Rate 随数据规模变化的趋势。
- **Metrics**: ['Progress Rate', 'Success Rate']
- **Expected outcome**: 随着预训练数据规模增加，两个指标应呈上升趋势。
- **Baselines**: ['较小预训练数据规模设置']
- **Dependencies**: ['Figure 5']

## E4: 训练吞吐分析
- **Verifies**: C5
- **Setup**:
  - Model: Qwen2.5-VL-3B-π、PaliGemma-3B-pt-224-π 的 π-like 复现模型
  - Hardware: 多 GPU 训练配置
  - Dataset: Libero
  - System: LingBot-VLA 代码库与 StarVLA、Dexbotic、OpenPI 代码库对比
- **Procedure**:
  1. 在各代码库中采用标准化 π-like 模型架构。
  2. 统一 local batch size。
  3. 在不同 GPU 配置下记录 sample throughput。
  4. 与理论线性扩展趋势和开源代码库基线对比。
- **Metrics**: ['samples/s', 'scaling efficiency']
- **Expected outcome**: LingBot-VLA 代码库应达到更快训练速度，并随 GPU 增加保持良好扩展趋势。
- **Baselines**: ['StarVLA', 'Dexbotic', 'OpenPI']
- **Dependencies**: ['Figure 4']

## E5: 后训练数据效率分析
- **Verifies**: C1, C4
- **Setup**:
  - Model: LingBot-VLA、π0.5
  - Hardware: Agibot G1
  - Dataset: GM-100 代表性任务后训练数据
  - System: 沿用大规模真实世界基准协议，改变每任务 demonstrations 预算
- **Procedure**:
  1. 选取代表性真实世界任务。
  2. 控制每任务后训练数据预算。
  3. 比较 LingBot-VLA 与 π0.5 在 Progress Rate 和 Success Rate 上的变化趋势。
- **Metrics**: ['Progress Rate', 'Success Rate']
- **Expected outcome**: LingBot-VLA 应在较少后训练数据下达到更好的方向性表现，并随数据增加扩大优势。
- **Baselines**: ['π0.5']
- **Dependencies**: ['Figure 6']
