# Experiments

## E1: CarRacing-v0消融实验：V-only vs 完整世界模型及多基线对比
- **Verifies**: C1, C2, C5
- **Setup**:
  - Model: VAE（32维潜空间，4,348,547参数）、MDN-RNN（256单元LSTM，5个高斯混合，422,368参数）、Controller线性层（867参数）；消融变体：Controller仅用zₜ，或在zₜ后加40单元tanh隐藏层（1443参数）；CMA-ES种群64，每个智能体16次随机种子评估
  - Hardware: 单GPU，Google Cloud Platform Ubuntu虚拟机，每个模型训练不足一小时
  - Dataset: CarRacing-v0随机策略采集的10,000条轨迹，图像调整为64×64像素
  - System: OpenAI Gym CarRacing-v0（轨道随机生成，连续动作：转向/加速/刹车；解任务阈值：100次平均分900）
- **Procedure**:
  1. 以随机策略采集10,000条轨迹，记录动作aₜ与观测帧
  2. 训练VAE将帧压缩为z∈R^32，训练1个epoch
  3. 训练MDN-RNN建模P(z_{t+1}|aₜ, zₜ, hₜ)，训练20个epoch
  4. 消融组1：定义Controller为aₜ=Wc·zₜ+bc，用CMA-ES优化，运行至收敛
  5. 消融组2：在zₜ后增加40单元tanh隐藏层，用CMA-ES优化
  6. 完整模型：定义Controller为aₜ=Wc·[zₜ, hₜ]+bc，用CMA-ES优化
  7. 每1800代取最佳智能体，在100次随机轨迹上评估平均累积奖励
- **Metrics**: ['100次随机轨迹的平均累积奖励（Avg. Score）']
- **Expected outcome**: 完整世界模型（使用hₜ）得分高于仅使用zₜ的消融设置，且高于所有已报告的Deep RL基线，并达到解任务阈值
- **Baselines**: ['DQN（Prieur,2017）', 'A3C Continuous（Jang et al.,2017）', 'A3C Discrete（Khan & Elibol,2016）', 'CEOBILLIONAIRE（OpenAI Gym排行榜）']
- **Dependencies**: ['VAE训练先于MDN-RNN训练', 'MDN-RNN训练先于Controller CMA-ES优化']

## E2: VizDoom Take Cover梦境训练与策略迁移实验
- **Verifies**: C1, C3
- **Setup**:
  - Model: VAE（64维潜空间，4,446,915参数）、MDN-RNN（512单元LSTM，5个高斯混合，1,678,785参数；额外预测done状态）、Controller线性层（1,088参数，输入为[zₜ, cₜ, hₜ]）；CMA-ES种群64，每个智能体16次随机种子评估；梦境温度τ=1.15
  - Hardware: 多CPU核并行，Google Cloud Platform Ubuntu虚拟机
  - Dataset: VizDoom DoomTakeCover-v0随机策略采集的10,000条轨迹
  - System: DoomRNN虚拟环境（MDN-RNN包装为OpenAI Gym接口，仅在潜空间运行，无需渲染像素帧）；策略评估在真实VizDoom DoomTakeCover-v0中进行（最大2100步，解任务阈值750步）
- **Procedure**:
  1. 以随机策略在真实VizDoom中采集10,000条轨迹
  2. 训练VAE将帧压缩为z∈R^64
  3. 训练MDN-RNN建模P(z_{t+1}, d_{t+1}|aₜ, zₜ, hₜ)，done概率超50%则判定终止
  4. 将MDN-RNN包装为gym.Env接口构建DoomRNN虚拟环境，τ=1.15
  5. 在DoomRNN中使用CMA-ES训练控制器C，最大化虚拟环境中的存活时步
  6. 取在1024次虚拟轨迹上平均得分最高的智能体
  7. 将梦境习得策略直接部署到真实VizDoom，在100次连续随机轨迹上评估
- **Metrics**: ['虚拟环境平均存活时步', '真实VizDoom 100次轨迹平均存活时步']
- **Expected outcome**: 梦境训练得到的策略在真实环境中存活时步数高于解任务阈值，且优于OpenAI Gym排行榜最优成绩
- **Baselines**: ['OpenAI Gym排行榜最优（Paquette,2016）', '随机策略']
- **Dependencies**: ['须先完成VAE和MDN-RNN训练方可构建DoomRNN虚拟环境', '仅用随机策略数据训练，未在真实环境上训练控制器']

## E3: VizDoom梦境温度参数τ消融实验
- **Verifies**: C4
- **Setup**:
  - Model: 与E2相同的VAE和MDN-RNN权重；在不同τ值的DoomRNN虚拟环境中独立训练各自的Controller
  - Hardware: Google Cloud Platform Ubuntu虚拟机
  - Dataset: 与E2相同的VizDoom随机策略轨迹数据集（10,000条）
  - System: DoomRNN虚拟环境（τ分别取0.10, 0.50, 1.00, 1.15, 1.30）；评估在真实VizDoom DoomTakeCover-v0中进行
- **Procedure**:
  1. 固定已训练的VAE和MDN-RNN权重不变
  2. 分别以τ∈{0.10, 0.50, 1.00, 1.15, 1.30}配置DoomRNN虚拟环境
  3. 在每种τ设置下用CMA-ES独立训练控制器C
  4. 记录各τ设置下的虚拟环境平均得分（Virtual Score）
  5. 将各τ训练得到的策略分别部署到真实VizDoom，记录100次轨迹的平均真实得分（Actual Score）
  6. 与随机策略和Gym排行榜最优分进行对比
- **Metrics**: ['虚拟环境平均存活时步（Virtual Score）', '真实VizDoom 100次轨迹平均存活时步（Actual Score）']
- **Expected outcome**: 存在某中间τ值使真实环境得分最优；极低τ时虚拟得分极高但真实得分接近随机策略水平；τ过高时虚拟和真实得分均显著下降
- **Baselines**: ['随机策略', 'Gym排行榜最优（Paquette,2016）']
- **Dependencies**: ['需先完成E2中的VAE和MDN-RNN训练']
