# Experiments

## E1: NAVSIM navtest split闭环规划性能对比实验
- **Verifies**: C2
- **Setup**:
  - Model: DiffusionDrive(ResNet-34主干,20个K-Means聚类锚点,2个级联解码器层,2步去噪)
  - Hardware: 8台NVIDIA 4090 GPU训练,单台NVIDIA 4090推理
  - Dataset: NAVSIM navtest split
  - System: AdamW优化器,学习率6×10^-4,总批次大小512,训练100轮,无测试时数据增强,无后处理
- **Procedure**:
  1. 以与Transfuser相同的ResNet-34主干和感知模块设置训练DiffusionDrive
  2. 在navtest split上执行非反应式仿真闭环评估
  3. 以PDM得分(PDMS)及其子分项NC、DAC、TTC、Comf.、EP进行评估
  4. 与UniAD、PARA-Drive、LTF、Transfuser、DRAMA、VADv2-V8192、Hydra-MDP-V8192及Hydra-MDP-V8192-W-EP对比
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP', 'FPS']
- **Expected outcome**: DiffusionDrive在PDMS及多数子指标上均优于所有先前方法,以远少于大词汇表方法的锚点数取得最高PDMS
- **Baselines**: ['UniAD', 'PARA-Drive', 'LTF', 'Transfuser', 'DRAMA', 'VADv2-V8192', 'Hydra-MDP-V8192', 'Hydra-MDP-V8192-W-EP']
- **Dependencies**: []

## E2: 从Transfuser到DiffusionDrive的演进路线图实验
- **Verifies**: C1
- **Setup**:
  - Model: Transfuser / Transfuser_DP / Transfuser_TD / DiffusionDrive四个变体
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 以Transfuser为起点,逐步引入原始DDIM扩散策略(DP)、截断扩散策略(TD)、级联扩散解码器
- **Procedure**:
  1. Transfuser:确定性MLP规划头基准
  2. Transfuser_DP:将MLP头替换为条件扩散模型UNet,使用20步DDIM推理
  3. Transfuser_TD:在Transfuser_DP基础上应用截断扩散策略,将推理步数降至2步
  4. DiffusionDrive:进一步引入级联扩散解码器替换UNet
  5. 评估每个变体的PDMS、模态多样性得分D、FPS、每步时延及总时延
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP', '模态多样性得分D', 'FPS', '每步时间', '总时延', '参数量']
- **Expected outcome**: 每步改进均带来规划质量或推理效率的提升;截断扩散策略大幅减少去噪步数并显著提升多样性得分;最终DiffusionDrive在PDMS和多样性上均最优
- **Baselines**: ['Transfuser', 'Transfuser_DP', 'Transfuser_TD']
- **Dependencies**: []

## E3: 扩散解码器设计组件消融实验
- **Verifies**: C3
- **Setup**:
  - Model: DiffusionDrive六种消融变体(ID 1-6)
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 基于截断扩散策略,逐步启用/禁用各解码器组件
- **Procedure**:
  1. ID-1:UNet解码器+自我查询交互(即Transfuser_TD)
  2. ID-2:仅自我查询交互,无空间交叉注意力和智能体/地图交叉注意力
  3. ID-3:自我查询交互+空间交叉注意力
  4. ID-4:自我查询交互+智能体/地图交叉注意力
  5. ID-5:自我查询交互+空间交叉注意力+智能体/地图交叉注意力
  6. ID-6(完整DiffusionDrive):ID-5基础上添加级联解码器(堆叠2层)
  7. 评估各变体PDMS、子指标及参数量
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP', '参数量(M)']
- **Expected outcome**: 完整解码器ID-6取得最高规划质量;空间交叉注意力对准确规划至关重要;级联机制进一步提升性能;完整解码器比UNet基准参数更少而性能更高
- **Baselines**: ['ID-1(Transfuser_TD)', 'ID-2', 'ID-3', 'ID-4', 'ID-5']
- **Dependencies**: ['E2']

## E4: 推理去噪步数消融实验
- **Verifies**: C1
- **Setup**:
  - Model: DiffusionDrive(60M参数,固定训练权重)
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 固定模型权重,仅改变推理时的DDIM去噪步数
- **Procedure**:
  1. 分别使用1步、2步、3步去噪进行推理
  2. 评估每个设置下的PDMS及子指标
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP']
- **Expected outcome**: 即使仅1步去噪也能取得较好规划质量;增加步数带来边际性能提升并趋于饱和
- **Baselines**: ['1步', '2步(默认配置)', '3步']
- **Dependencies**: []

## E5: 级联解码器阶段数消融实验
- **Verifies**: C3
- **Setup**:
  - Model: DiffusionDrive系列变体
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 改变级联扩散解码器的堆叠层数,分别训练并评估
- **Procedure**:
  1. 分别使用1个、2个、4个级联阶段训练和评估模型
  2. 对比各设置下的PDMS、参数量
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP', '参数量(M)']
- **Expected outcome**: 增加级联阶段数可提升规划质量但在一定阶段数后趋于饱和,且伴随参数量增大
- **Baselines**: ['1阶段', '2阶段(默认配置)', '4阶段']
- **Dependencies**: []

## E6: 推理时采样噪声数量N_infer消融实验
- **Verifies**: C2
- **Setup**:
  - Model: DiffusionDrive(60M参数,固定训练权重)
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 固定模型权重,仅改变推理时从锚定高斯分布采样的轨迹数量N_infer
- **Procedure**:
  1. 分别使用N_infer为10、20、40进行推理
  2. 评估每个设置下的PDMS及子指标
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP']
- **Expected outcome**: 更多采样数量能更好地覆盖潜在动作空间,带来更好的规划质量,且模型训练与推理采样数解耦
- **Baselines**: ['N_infer=10', 'N_infer=20(默认配置)', 'N_infer=40']
- **Dependencies**: []

## E7: nuScenes数据集开环规划性能对比实验
- **Verifies**: C4
- **Setup**:
  - Model: DiffusionDrive(ResNet-50主干,基于SparseDrive,18个K-Means聚类锚点,2个级联解码器层)
  - Hardware: 单台NVIDIA 4090 GPU推理
  - Dataset: nuScenes
  - System: 遵循SparseDrive两阶段训练协议,第二阶段在nuScenes上训练10轮,使用阶段1感知预训练权重初始化
- **Procedure**:
  1. 在SparseDrive基础上用截断扩散机制和扩散解码器替换规划模块
  2. 按ST-P3评估协议计算1s/2s/3s的L2误差和碰撞率
  3. 与ST-P3、UniAD、OccNet、VAD、SparseDrive对比
- **Metrics**: ['L2误差(1s/2s/3s/平均, 单位m)', '碰撞率(1s/2s/3s/平均, 单位%)', 'FPS']
- **Expected outcome**: DiffusionDrive在平均L2误差上优于或持平SparseDrive,并在运行速度上快于VAD
- **Baselines**: ['ST-P3', 'UniAD', 'OccNet', 'VAD', 'SparseDrive']
- **Dependencies**: []

## E8: 驾驶先验类型对比实验
- **Verifies**: C5
- **Setup**:
  - Model: DiffusionDrive系列变体
  - Hardware: NVIDIA 4090 GPU
  - Dataset: NAVSIM navtest split
  - System: 对比多模式锚定高斯分布先验与基于当前行驶状态外推轨迹先验,涵盖不同训练与推理先验组合
- **Procedure**:
  1. Row-1(DiffusionDrive基准):训练和推理均使用锚定高斯分布
  2. Row-2:使用DiffusionDrive基准模型但推理时改用外推轨迹作为起点
  3. Row-3:训练时仅使用单个锚点(外推轨迹)并围绕其采样推理
  4. 评估各设置下的PDMS及子指标
- **Metrics**: ['PDMS', 'NC', 'DAC', 'TTC', 'Comf.', 'EP']
- **Expected outcome**: 锚定高斯分布(Row-1)在PDMS及所有子指标上均优于外推轨迹先验
- **Baselines**: ['锚定分布推理+外推轨迹推理(Row-2)', '外推轨迹训练+推理(Row-3)']
- **Dependencies**: ['E2']

## E9: 锚点来源跨域泛化性实验(CARLA Longest6)
- **Verifies**: C6
- **Setup**:
  - Model: DiffusionDrive(在CARLA数据集上训练,使用NAVSIM聚类锚点)
  - Hardware: 论文未明确说明
  - Dataset: CARLA Longest6基准
  - System: 以NAVSIM数据集K-Means聚类锚点构建锚定高斯分布,在与NAVSIM完全不同的CARLA驾驶数据集上训练
- **Procedure**:
  1. 从NAVSIM数据集聚类得到锚点并构建锚定高斯分布
  2. 在CARLA数据集上训练DiffusionDrive
  3. 在CARLA Longest6基准上评估DS(驾驶得分)、RC(路线完成率)、IS(闯红灯得分)
  4. 与Transfuser在CARLA上的结果对比
- **Metrics**: ['DS(驾驶得分)', 'RC(路线完成率)', 'IS(基础设施评分)']
- **Expected outcome**: 使用跨域NAVSIM锚点的DiffusionDrive在CARLA上取得显著优于Transfuser基准的结果
- **Baselines**: ['Transfuser']
- **Dependencies**: []
