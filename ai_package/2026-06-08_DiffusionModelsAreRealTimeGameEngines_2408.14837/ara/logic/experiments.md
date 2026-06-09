# Experiments

## E1: 教师强制设置下的单帧图像质量评估
- **Verifies**: C1, C4
- **Setup**:
  - Model: GameNGen（Stable Diffusion v1.4 微调，含解码器微调，训练 700k 步）
  - Hardware: 128 个 TPU-v5e 训练，单个 TPU-v5 推理
  - Dataset: 5 个关卡的随机保留集，共 2048 条轨迹
  - System: DOOM 游戏环境，VizDoom，分辨率 320x240 填充至 320x256
- **Procedure**:
  1. 从保留集采样初始状态
  2. 基于真实历史帧和动作序列（上下文长度 64）预测单帧
  3. 计算预测帧与真实帧之间的 PSNR 和 LPIPS 指标
  4. 将 PSNR 值与有损 JPEG 压缩质量设置 20-30 的结果进行对比
- **Metrics**: ['PSNR（越高越好）', 'LPIPS（越低越好）']
- **Expected outcome**: PSNR 达到与有损 JPEG 压缩相当的质量水平，LPIPS 保持较低
- **Baselines**: ['有损 JPEG 压缩（质量设置 20-30）']
- **Dependencies**: ['RL 智能体数据采集完成（50M 环境步）', '解码器微调完成']

## E2: 自回归设置下的视频质量评估（FVD）
- **Verifies**: C1
- **Setup**:
  - Model: GameNGen（完整模型，700k 训练步）
  - Hardware: 单个 TPU-v5
  - Dataset: 512 条随机保留轨迹
  - System: DOOM 游戏环境，自回归帧生成，16 帧（0.8 秒）和 32 帧（1.6 秒）片段
- **Procedure**:
  1. 按真实轨迹动作序列迭代采样帧
  2. 以模型自身的过去预测作为条件（自回归）
  3. 分别对 16 帧和 32 帧片段计算 FVD
  4. 测量预测轨迹分布与真实轨迹分布之间的距离
- **Metrics**: ['FVD（越低越好）']
- **Expected outcome**: FVD 值在合理范围内，预测轨迹分布与真实游戏轨迹分布接近
- **Baselines**: []
- **Dependencies**: ['E1 中验证的完整模型']

## E3: 人工评估：区分仿真与真实游戏短片
- **Verifies**: C1, C6
- **Setup**:
  - Model: GameNGen（完整模型）
  - Hardware: 单个 TPU-v5
  - Dataset: 130 个随机短片段（1.6 秒和 3.2 秒），以及额外 150 个 3 秒片段（在 5-10 分钟游戏后生成）
  - System: DOOM 仿真 vs 真实游戏，10 位人工评估者，并排展示工具（见 Appendix A.8）
- **Procedure**:
  1. 向 10 位评估者并排展示仿真片段与真实游戏片段
  2. 评估者识别哪个视频是真实游戏
  3. 分别对 1.6 秒、3.2 秒短片段进行评估
  4. 额外对 5-10 分钟游戏后的 3 秒长片段进行评估，测量长期自回归误差累积的影响
- **Metrics**: ['评估者选择真实游戏的比例（越接近 50% 表示仿真越逼真）']
- **Expected outcome**: 评估者选择准确率仅略高于随机水平（约 50-60%），长片段下接近随机
- **Baselines**: ['随机猜测基准（50%）']
- **Dependencies**: ['E1 中验证的完整模型']

## E4: 不同 DDIM 采样步数的生成质量消融实验
- **Verifies**: C1, C3
- **Setup**:
  - Model: GameNGen（多种采样步数变体：1、2、4、8、16、32、64 步；以及单步蒸馏变体 D）
  - Hardware: 单个 TPU-v5
  - Dataset: 教师强制轨迹，35FPS 数据，2048 帧
  - System: DOOM 游戏环境，VizDoom
- **Procedure**:
  1. 评估采样步数从 1 到 64 逐步增加时的生成质量
  2. 单独训练蒸馏模型（3 个 U-Net：生成器、教师、伪分值模型，训练 1000 步）
  3. 计算各配置的 PSNR 和 LPIPS 指标
- **Metrics**: ['PSNR（越高越好）', 'LPIPS（越低越好）']
- **Expected outcome**: 4 步采样质量与 20+ 步相当，但单步非蒸馏模型质量明显下降；蒸馏模型（D）在单步下显著优于非蒸馏单步
- **Baselines**: ['非蒸馏单步模型（1 步）', '64 步参考模型']
- **Dependencies**: ['GameNGen 完整训练完成（700k 步）']

## E5: 历史上下文帧数对生成质量影响的消融实验
- **Verifies**: C1
- **Setup**:
  - Model: GameNGen（7 种上下文长度：N ∈ {1,2,4,8,16,32,64}，解码器冻结，各训练 200k 步）
  - Hardware: 128 个 TPU-v5e
  - Dataset: 5 个关卡的测试集，共 8912 个样本
  - System: DOOM 游戏环境，教师强制单帧评估
- **Procedure**:
  1. 训练不同上下文长度的模型各 200,000 步
  2. 在测试集轨迹上评估 PSNR 和 LPIPS
  3. 分析质量随上下文长度变化的趋势，识别收益递减规律
- **Metrics**: ['PSNR（越高越好）', 'LPIPS（越低越好）']
- **Expected outcome**: 质量随上下文长度增加而提升，但增益迅速递减并趋近渐近线
- **Baselines**: ['单帧上下文（N=1）']
- **Dependencies**: ['GameNGen 训练框架']

## E6: 噪声增强对自回归稳定性影响的消融实验
- **Verifies**: C2
- **Setup**:
  - Model: GameNGen 有噪声增强版本（最大噪声级别 0.7，10 个嵌入桶）vs 无噪声增强版本（均训练 200k 步）
  - Hardware: 128 个 TPU-v5e
  - Dataset: 512 条随机保留轨迹
  - System: DOOM 游戏环境，自回归评估，共 64 步
- **Procedure**:
  1. 训练无噪声增强的对比模型（其余设置一致）
  2. 对两种模型进行 64 步自回归生成
  3. 逐自回归步骤计算平均 LPIPS 和 PSNR
  4. 对比两者随步骤推进的质量变化曲线
- **Metrics**: ['每自回归步骤的平均 LPIPS（越低越好）', '每自回归步骤的平均 PSNR（越高越好）']
- **Expected outcome**: 无噪声增强的模型在约 10-20 帧后质量迅速退化，而有噪声增强的模型质量保持稳定
- **Baselines**: ['无噪声增强模型']
- **Dependencies**: ['GameNGen 训练框架（200k 步）']

## E7: RL 智能体数据与随机策略数据训练效果对比
- **Verifies**: C5
- **Setup**:
  - Model: 两个 GameNGen 完整模型（含解码器微调，各训练 700k 步），分别使用智能体生成数据和随机策略数据
  - Hardware: 128 个 TPU-v5e
  - Dataset: 5 个关卡 2048 条人类游戏轨迹；456 个样本按距起始位置远近手动划分为简单（112 个）、中等（112 个）、困难（232 个）三组
  - System: DOOM 游戏环境，VizDoom；随机策略按均匀分类分布采样动作
- **Procedure**:
  1. 分别用智能体数据和随机策略数据训练两个完整模型
  2. 在 64 帧真实历史上下文条件下评估单帧生成质量
  3. 评估自回归生成 3 秒后的帧质量
  4. 按简单/中等/困难难度分组比较两个模型的 PSNR 和 LPIPS
- **Metrics**: ['PSNR（越高越好）', 'LPIPS（越低越好）']
- **Expected outcome**: 智能体数据整体优于随机数据，中等难度区域差异最大；简单和困难区域差异相对较小
- **Baselines**: ['随机策略数据训练的模型']
- **Dependencies**: ['RL 智能体训练完成（PPO，50M 环境步）']
