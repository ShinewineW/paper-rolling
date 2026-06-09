# Experiments

## E1: nuScenes 验证集定量保真度比较（FID 与 FVD）
- **Verifies**: C1
- **Setup**:
  - Model: Vista（基于 SVD，2.5B 参数）
  - Hardware: 128 块 A100 GPU（第一阶段训练）
  - Dataset: nuScenes 验证集（筛选 5369 个有效样本）
  - System: FID 评估：裁剪并缩放预测帧至 256×448；FVD 评估：使用每个视频片段全部 25 帧，下采样至 224×224（参照 LVDM）
- **Procedure**:
  1. 从 nuScenes 验证集筛选 5369 个有效样本
  2. 各方法在相同样本上生成预测视频
  3. FID：裁剪缩放至 256×448 后计算
  4. FVD：全 25 帧下采样至 224×224 后计算
  5. 与 DriveGAN、DriveDreamer、WoVoGen、Drive-WM、GenAD 比较官方报告的定量结果
- **Metrics**: ['FID（越低越好）', 'FVD（越低越好）']
- **Expected outcome**: Vista 的 FID 和 FVD 均低于所有对比驾驶世界模型
- **Baselines**: ['DriveGAN', 'DriveDreamer', 'WoVoGen', 'Drive-WM', 'GenAD']
- **Dependencies**: []

## E2: 跨数据集泛化能力人类评估（视觉质量与运动合理性）
- **Verifies**: C2
- **Setup**:
  - Model: Vista 对比 SVD、DynamiCrafter、I2VGen-XL 等通用视频生成器
  - Hardware: 人类评估（共 33 名参与者，收集 2640 个回答）
  - Dataset: OpenDV-YouTube-val、nuScenes、Waymo、CODA（各均匀采样，共 60 个场景）
  - System: 双选强制选择协议（Two-Alternative Forced Choice），视频对裁剪至统一宽高比并下采样至相同分辨率，超出 Vista 时长的部分被裁剪
- **Procedure**:
  1. 从四个代表性数据集各均匀采样场景组成 60 个评估场景
  2. 按视觉质量和运动合理性两个维度分别进行侧边评估
  3. 参与者在视频对中选择更优者
  4. 统计 Vista 被偏好的百分比
  5. 所有对比模型使用官方权重和默认配置进行推理
- **Metrics**: ['Vista 被偏好的百分比（视觉质量）', 'Vista 被偏好的百分比（运动合理性）']
- **Expected outcome**: Vista 在两个维度均以超过 70% 的优势高于各通用视频生成器基线
- **Baselines**: ['SVD', 'DynamiCrafter', 'I2VGen-XL']
- **Dependencies**: []

## E3: 行动控制一致性定量评估（轨迹差异指标，nuScenes 与 Waymo）
- **Verifies**: C6
- **Setup**:
  - Model: Vista（分别加入目标点、命令、角度与速度、轨迹等行动条件，对比无条件基线）
  - Hardware: 论文未单独说明评估硬件
  - Dataset: nuScenes 验证集子集（537 个样本）、Waymo 验证集子集（537 个样本）
  - System: 逆动力学模型（IDM）从视频片段推断对应轨迹；计算真值轨迹与估算轨迹的 L2 差异（2 秒窗口）
- **Procedure**:
  1. 将 nuScenes 和 Waymo 验证集分别划分含 537 个样本的子集
  2. 以真值行动条件（目标点、命令、角度与速度、轨迹）分别驱动 Vista 生成预测
  3. 用 IDM 从预测视频推断轨迹
  4. 计算各行动模式与真值轨迹的平均轨迹差异
  5. 同时统计不同动态先验帧数（1/2/3 帧）的结果
- **Metrics**: ['平均轨迹差异↓（越低代表控制一致性越强）']
- **Expected outcome**: 加入行动条件后轨迹差异显著低于无条件基线，在未见的 Waymo 数据集上同样有效
- **Baselines**: ['无行动条件（action-free）', '真值视频（GT video）']
- **Dependencies**: ['E6']

## E4: 奖励函数泛化验证（Waymo 数据集，不同 L2 误差轨迹的平均奖励相关性）
- **Verifies**: C7
- **Setup**:
  - Model: Vista 奖励函数（集成大小 M=5，去噪步数 10）
  - Hardware: 论文未单独说明评估硬件
  - Dataset: Waymo 验证集（按命令类别均匀采样，共 1500 个案例）
  - System: 对真值轨迹施加不同幅度扰动生成具有不同 L2 误差的劣质轨迹；采用显式相关采样策略（系数 β=0.5）保证轨迹合理性
- **Procedure**:
  1. 从 Waymo 验证集按命令类别均匀采样 1500 个案例
  2. 计算 nuScenes 训练集各路点的标准差作为先验分布
  3. 以不同比例缩放扰动，生成具有不同 L2 误差的劣质轨迹
  4. 对每个条件帧-行动对运行 M=5 轮去噪，估算条件方差
  5. 计算平均奖励并与 L2 误差进行相关性分析
- **Metrics**: ['平均奖励（越高代表轨迹越优）', '奖励与 L2 误差的相关性']
- **Expected outcome**: 随轨迹 L2 误差增大，Vista 估算的平均奖励单调下降
- **Baselines**: ['真值轨迹']
- **Dependencies**: []

## E5: 辅助损失函数消融研究（动态增强损失与结构保留损失）
- **Verifies**: C3, C4
- **Setup**:
  - Model: Vista 消融变体（分别去除动态增强损失或结构保留损失）
  - Hardware: 8 块 A100 GPU
  - Dataset: OpenDV-YouTube
  - System: 各变体从 SVD 预训练权重初始化，在 576×1024 分辨率下训练 10K 步
- **Procedure**:
  1. 构建包含两种辅助损失的完整变体
  2. 分别训练去除动态增强损失的变体和去除结构保留损失的变体
  3. 在相同条件帧上定性比较各变体的预测输出
  4. 观察移动物体的运动真实性和物体边缘的结构清晰度
- **Metrics**: ['定性视觉对比（运动真实性、结构细节）']
- **Expected outcome**: 去除动态增强损失后移动前景物体的运动预测退化；去除结构保留损失后运动物体轮廓出现模糊或崩溃
- **Baselines**: ['仅使用标准扩散损失的变体']
- **Dependencies**: []

## E6: 动态先验帧数消融研究（不同阶先验对轨迹一致性的影响）
- **Verifies**: C5
- **Setup**:
  - Model: Vista（分别使用 1/2/3 帧动态先验）
  - Hardware: 论文未单独说明评估硬件
  - Dataset: nuScenes 验证集子集（537 个样本）、Waymo 验证集子集（537 个样本）
  - System: 使用 IDM 从预测视频推断轨迹，计算与真值轨迹的 L2 差异
- **Procedure**:
  1. 分别以 1 帧、2 帧、3 帧历史帧作为动态先验驱动 Vista 生成预测
  2. 用 IDM 推断各预测视频对应的轨迹
  3. 计算不同先验阶数下的平均轨迹差异
  4. 对比无行动条件和有行动条件两种设置下先验帧数的边际贡献
- **Metrics**: ['平均轨迹差异↓（1/2/3 帧先验）']
- **Expected outcome**: 引入更多动态先验帧持续降低轨迹差异，验证先验阶数对长时域一致性的正向贡献
- **Baselines**: ['单帧先验（1 prior）']
- **Dependencies**: []
