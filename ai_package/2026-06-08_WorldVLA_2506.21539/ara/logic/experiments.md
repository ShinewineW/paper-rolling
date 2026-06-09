# Experiments

## E1: LIBERO 基准综合对比：WorldVLA 与各类动作模型基线的成功率对比
- **Verifies**: C1, C2
- **Setup**:
  - Model: WorldVLA（256×256 和 512×512 两种分辨率，基于 Chameleon 初始化）
  - Hardware: 论文未详细说明
  - Dataset: LIBERO-Spatial、LIBERO-Object、LIBERO-Goal、LIBERO-Long，使用全量数据训练以确保公平对比
  - System: 自回归离散 token 框架，VQ-GAN 图像分词器（压缩比 16，码本大小 8192），BPE 文本分词器（词表 65536），动作编码为 7 个 token
- **Procedure**:
  1. 在 LIBERO 全量数据集上训练 WorldVLA（256×256 和 512×512 两种分辨率版本）
  2. 与连续动作模型基线（Diffusion Policy、Octo、DiT Policy、Seer、OpenVLA-OFT、UVA）以及离散动作模型基线（OpenVLA）进行对比
  3. 在 LIBERO-Spatial、LIBERO-Object、LIBERO-Goal、LIBERO-Long 四个子集上各执行 50 次 rollout 评估成功率
- **Metrics**: ['各子任务成功率 SR (%)', '平均成功率 Average SR (%)']
- **Expected outcome**: WorldVLA 平均成功率高于同等离散动作模型基线 OpenVLA，且在无预训练设定下具有竞争力
- **Baselines**: ['Diffusion Policy', 'Octo', 'DiT Policy', 'Seer', 'OpenVLA-OFT', 'UVA', 'OpenVLA']
- **Dependencies**: []

## E2: 动作模型消融：逐步增加世界模型、动作块生成与新注意力遮蔽策略
- **Verifies**: C2, C4, C5, C7
- **Setup**:
  - Model: WorldVLA（256×256），基于 Chameleon 初始化
  - Hardware: 论文未详细说明
  - Dataset: LIBERO 训练集（90% 轨迹），α=0.04，M=2 历史帧，动作块大小 K：Long 任务为 10，其余为 5
  - System: 5 种组件配置：①仅动作模型；②+世界模型（无动作块）；③+动作块（默认遮蔽）；④+动作块（新遮蔽）；⑤+世界模型+动作块（新遮蔽）
- **Procedure**:
  1. 按 Table 3 所示 5 种配置分别训练模型
  2. 在 LIBERO 验证集各子任务上执行 50 次 rollout 评估
  3. 记录 Goal、Object、Spatial、Long 四个子任务及平均成功率
  4. 另对比世界模型与视频预测模型对动作模型性能的影响（Fig 7）
- **Metrics**: ['Goal SR (%)', 'Object SR (%)', 'Spatial SR (%)', 'Long SR (%)', 'Average SR (%)']
- **Expected outcome**: 加入世界模型后平均 SR 高于无世界模型基线；新注意力遮蔽的动作块生成性能明显高于默认遮蔽
- **Baselines**: ['行 1：仅动作模型（无世界模型、无动作块）', '行 3：动作块+默认因果注意力遮蔽']
- **Dependencies**: []

## E3: 世界模型消融：动作世界模型 vs 纯世界模型视频生成质量对比
- **Verifies**: C1, C3
- **Setup**:
  - Model: 纯世界模型 vs WorldVLA（动作世界模型），均基于 Chameleon 初始化
  - Hardware: 论文未详细说明
  - Dataset: LIBERO 验证集（10% 轨迹），世界模型单轮预测 N=1
  - System: 自回归图像生成，以图像+动作序列为条件预测下一帧
- **Procedure**:
  1. 分别训练纯世界模型（无动作模型联合训练）与 WorldVLA（动作+世界联合训练）
  2. 在 LIBERO 验证集上评估短序列（10 帧）和长序列（50 帧）视频生成质量
  3. 记录 FVD、PSNR、SSIM、LPIPS 四项指标
- **Metrics**: ['FVD（越低越好）', 'PSNR（越高越好）', 'SSIM（越高越好）', 'LPIPS（越低越好）']
- **Expected outcome**: WorldVLA 在长序列（50 帧）上的 FVD 低于纯世界模型，动作模型对视觉理解的增强在长序列生成上体现更明显
- **Baselines**: ['纯世界模型（无动作模型联合训练）']
- **Dependencies**: []

## E4: 动作块长度消融：不同块大小下新旧注意力遮蔽策略性能曲线对比
- **Verifies**: C4, C5
- **Setup**:
  - Model: WorldVLA（256×256），分别使用默认因果遮蔽和新提出的动作注意力遮蔽
  - Hardware: 论文未详细说明
  - Dataset: LIBERO 基准任务
  - System: 动作块长度从短到长逐步变化
- **Procedure**:
  1. 在不同动作块长度（chunk length）下分别评估默认遮蔽和新提出遮蔽的模型
  2. 记录各块长度下的抓取成功率（Fig 6）
  3. 观察随块长度增加两种策略的性能变化趋势
- **Metrics**: ['抓取成功率 SR (%)']
- **Expected outcome**: 随动作块长度增加，默认遮蔽性能持续下降，新遮蔽策略在较长块长度下仍保持更高成功率；但块长度过长时两种策略均出现性能下降
- **Baselines**: ['默认因果注意力遮蔽的动作块生成']
- **Dependencies**: ['E2']

## E5: 世界模型预训练消融：以世界模型权重初始化动作模型的效果
- **Verifies**: C6
- **Setup**:
  - Model: WorldVLA 动作模型，有/无世界模型预训练权重初始化
  - Hardware: 论文未详细说明
  - Dataset: LIBERO 训练集（90% 轨迹）
  - System: 先以世界模型数据训练，再以动作模型数据微调
- **Procedure**:
  1. 实验组：先以世界模型数据训练模型，再在动作数据上微调
  2. 对照组：直接在动作数据上训练（无世界模型预训练）
  3. 在 LIBERO 四个子任务上分别评估 50 次 rollout 成功率（Table 6）
- **Metrics**: ['Goal SR (%)', 'Object SR (%)', 'Spatial SR (%)', 'Long SR (%)', 'Average SR (%)']
- **Expected outcome**: 使用世界模型预训练的版本在各子任务及平均 SR 上均高于直接训练的版本
- **Baselines**: ['直接训练动作模型（无世界模型预训练）']
- **Dependencies**: []

## E6: 历史图像帧数消融：输入帧数对动作成功率与推理速度的影响
- **Verifies**: C1
- **Setup**:
  - Model: WorldVLA（256×256），分别测试带/不带动作块生成
  - Hardware: 论文未详细说明
  - Dataset: LIBERO 基准
  - System: 输入历史图像帧数分别设为 1、2、4 帧
- **Procedure**:
  1. 在 1 帧、2 帧、4 帧三种历史输入配置下分别训练和评估模型
  2. 对带动作块和不带动作块两种模式分别测试
  3. 记录成功率 SR 和推理帧率 FPS（Table 5）
- **Metrics**: ['SR (%)', 'FPS']
- **Expected outcome**: 增加历史帧数可提升 SR 但降低 FPS；2 帧在成功率与计算效率之间取得较好平衡，4 帧相比 2 帧增益有限
- **Baselines**: ['单帧输入配置']
- **Dependencies**: []
