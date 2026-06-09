# Experiments

## E1: Cosmos Tokenizer在图像和视频基准上的重建质量与推理速度评估
- **Verifies**: C2
- **Setup**:
  - Model: Cosmos Tokenizer系列（CI/DI 8×8/16×16，CV/DV 4×8×8/8×8×8/8×16×16，Cosmos-Tokenize1系列）
  - Hardware: 单张NVIDIA A100 80GB GPU（推理速度测试）
  - Dataset: DAVIS (1080p视频)，TokenBench（500个多领域视频），MS-COCO 2017（5000图像验证集），ImageNet-1K（50000图像验证集）
  - System: PyTorch；连续tokenizer使用AE公式，离散tokenizer使用FSQ量化；对比方法包括FLUX-Tokenizer、Open-MAGVIT2-Tokenizer、LlamaGen-Tokenizer、VideoGPT-Tokenizer、Omni-Tokenizer、CogVideoX-Tokenizer
- **Procedure**:
  1. 在DAVIS和TokenBench上评估连续/离散视频tokenizer的PSNR、SSIM、rFVD指标
  2. 在MS-COCO 2017和ImageNet-1K上评估图像tokenizer的PSNR、SSIM、rFID指标
  3. 在A100 80GB GPU上测量各tokenizer每帧平均编解码时间
- **Metrics**: ['PSNR (dB)', 'SSIM', 'rFVD', 'rFID', '编解码时间(ms/帧)', '参数量(M)']
- **Expected outcome**: Cosmos Tokenizer在各重建指标上高于同类基线，推理速度显著快于基线，参数量更小
- **Baselines**: ['FLUX-Tokenizer8×8', 'Open-MAGVIT2-Tokenizer16×16', 'LlamaGen-Tokenizer8×8', 'VideoGPT-Tokenizer4×4×4', 'Omni-Tokenizer4×8×8', 'CogVideoX-Tokenizer4×8×8']
- **Dependencies**: []

## E2: 预训练WFM在RealEstate10K上的3D一致性评估
- **Verifies**: C3
- **Setup**:
  - Model: Cosmos-Predict1-7B-Text2World, Cosmos-Predict1-7B-Video2World, Cosmos-Predict1-4B, Cosmos-Predict1-5B-Video2World
  - Hardware: 未明确指定
  - Dataset: RealEstate10K测试集随机抽取500个静态场景视频，使用专有VLM生成文本提示
  - System: SuperPoint+LightGlue特征匹配，OpenCV RANSAC基础矩阵估计，3D Gaussian Splatting（Nerfstudio默认配置）
- **Procedure**:
  1. 对生成视频提取特征点对，计算Sampson几何误差
  2. 运行SfM算法评估相机位姿估计成功率
  3. 每隔8帧留出测试帧，用其余帧拟合3D高斯泼溅模型，评估保留帧的PSNR/SSIM/LPIPS
  4. 与VideoLDM基线和真实视频参考对比
- **Metrics**: ['Sampson误差↓', '相机位姿估计成功率(%)↑', 'PSNR↑', 'SSIM↑', 'LPIPS↓']
- **Expected outcome**: Cosmos WFM的几何一致性指标和新视角合成质量均高于VideoLDM基线，部分指标接近真实视频水平
- **Baselines**: ['VideoLDM']
- **Dependencies**: []

## E3: 预训练WFM在PhysX/Isaac Sim仿真基准上的物理对齐评估
- **Verifies**: C3
- **Setup**:
  - Model: Cosmos-Predict1-7B/14B-Video2World, Cosmos-Predict1-4B/5B/12B/13B-Video2World
  - Hardware: 未明确指定
  - Dataset: 使用PhysX和Isaac Sim生成的800个1080p物理仿真视频，覆盖8种牛顿力学场景（自由落体、倾斜坡道、U形坡、稳定堆叠、不稳定堆叠、多米诺、跷跷板、陀螺仪），随机化物体数量/纹理/背景，4个随机种子
  - System: SAMURAI实例追踪，DreamSim特征相似度模型
- **Procedure**:
  1. 给定前1帧或9帧物理仿真视频作为条件，让各WFM预测未来帧
  2. 计算预测帧与参考仿真帧的PSNR/SSIM（像素级）、DreamSim（特征级）和平均IoU（物体级）
  3. 对比扩散型和自回归型WFM在不同帧数条件下的物理对齐表现
- **Metrics**: ['PSNR↑', 'SSIM↑', 'DreamSim↑', '平均IoU (Avg.IoU)↑']
- **Expected outcome**: 扩散型WFM在多帧条件下像素级指标高于自回归型；所有模型在物理对齐方面均有较大改进空间
- **Baselines**: []
- **Dependencies**: []

## E4: 相机控制后训练WFM与CamCo的轨迹对齐和视频质量定量对比
- **Verifies**: C1, C4
- **Setup**:
  - Model: Cosmos-Predict1-7B-Video2World-Sample-CameraCond（在DL3DV-10K上微调），CamCo（同样在DL3DV-10K上微调）
  - Hardware: 训练使用包含10,000台H100 GPU的集群
  - Dataset: 训练集：DL3DV-10K；测试集：RealEstate10K测试集500个样本（训练→测试存在显著分布偏移）
  - System: Plücker坐标相机条件注入，GLOMAP结构运动估计，Procrustes对齐
- **Procedure**:
  1. 在DL3DV-10K上微调Cosmos-Predict1-7B-Video2World，添加Plücker嵌入作为相机控制条件，训练57帧视频
  2. 以RealEstate10K测试集首帧为参考图像，使用数据集相机轨迹作为控制输入
  3. 评估相机位姿估计成功率、旋转误差、平移误差（轨迹对齐），以及FID/FVD（视频质量）
- **Metrics**: ['相机位姿估计成功率(%)↑', '旋转误差(°)↓', '平移误差↓', 'FID↓', 'FVD↓']
- **Expected outcome**: Cosmos相机控制模型的轨迹对齐误差低于CamCo，FID/FVD低于CamCo
- **Baselines**: ['CamCo (Xu et al., 2024)']
- **Dependencies**: ['E2']

## E5: 后训练机器人操控WFM的指令跟随人类评估和动作预测定量评估
- **Verifies**: C1, C5
- **Setup**:
  - Model: Cosmos-Predict1-7B/5B-Video2World-Sample-Instruction（指令任务），Cosmos-Predict1-7B/5B-Video2World-Sample-ActionCond（动作任务）
  - Hardware: 训练使用H100 GPU集群
  - Dataset: 指令任务：Cosmos-1X内部数据集（约200小时EVE人形机器人视频，约12000个场景，23个测试场景）；动作任务：Bridge公开数据集（约20000个场景，随机抽取100个测试场景）
  - System: 指令任务：10名人类评估员双盲A/B评估；动作任务：自回归次帧预测，与IRASim-Action对比
- **Procedure**:
  1. 指令任务：与VideoLDM-Instruction对比，人类评估指令跟随、物体持久性、真实性、整体性四个维度
  2. 动作任务：微调后在Bridge测试集自回归生成视频，与IRASim-Action对比PSNR/SSIM/Latent L2/FVD
- **Metrics**: ['整体偏好率(%)↑（指令任务，人类评估）', 'PSNR↑', 'SSIM↑', 'Latent L2↓', 'FVD↓（动作任务）']
- **Expected outcome**: Cosmos后训练模型在人类评估各维度偏好率均高于VideoLDM-Instruction；在动作预测指标上优于IRASim-Action
- **Baselines**: ['VideoLDM-Instruction', 'IRASim-Action']
- **Dependencies**: []

## E6: 后训练多视角自动驾驶WFM的生成质量、几何一致性和轨迹跟随评估
- **Verifies**: C1, C6
- **Setup**:
  - Model: Cosmos-Predict1-7B-Text2World-Sample-MultiView，Cosmos-Predict1-7B-Text2World-Sample-MultiView-TrajectoryCond
  - Hardware: 训练使用H100 GPU集群
  - Dataset: 训练集：RDS内部数据集（约360万个20秒环视视频片段，约20000小时，6相机视角）；生成质量评估：1000个样本；几何一致性评估：800个样本（4类轨迹各200个）
  - System: YOLOv11x目标检测追踪，多视角相机位姿估计（稠密束调整），Sampson误差计算
- **Procedure**:
  1. 在RDS数据集上微调Cosmos-Predict1-7B-Text2World，引入视角独立位置嵌入和视角相关交叉注意力，构建多视角世界模型
  2. 评估FID/FVD（生成质量），TSE/CSE（多视角几何一致性），TAE和TFE（轨迹跟随精度）
  3. 与VideoLDM-MultiView基线和真实视频参考对比
- **Metrics**: ['FID↓', 'FVD↓', 'TSE（时间Sampson误差）↓', 'CSE（跨视角Sampson误差）↓', 'TAE-ATE↓', 'TAE-RPE-R↓', 'TAE-RPE-t↓', 'TFE(cm)↓']
- **Expected outcome**: Cosmos多视角模型在FID/FVD和几何一致性误差上低于VideoLDM-MultiView，轨迹跟随误差接近真实视频水平
- **Baselines**: ['VideoLDM-MultiView']
- **Dependencies**: []

## E7: Medusa多头数量消融与低分辨率适配实时推理基准测试
- **Verifies**: C8
- **Setup**:
  - Model: Cosmos-Predict1-4B和Cosmos-Predict1-5B-Video2World（含不同数量Medusa头，0/3/6/9/12）
  - Hardware: 8×H100 80GB GPU
  - Dataset: 50个未见测试视频（640×1024分辨率）；低分辨率适配：10 FPS视频（320×512分辨率）
  - System: BF16精度，torch.compile max-autotune模式，key-value缓存，tensor并行
- **Procedure**:
  1. 对4B和5B模型分别测试0/3/6/9/12个Medusa头，测量token吞吐量和前向传播次数
  2. 将4B模型微调至320×512低分辨率后添加Medusa头，在8×H100上测量token吞吐量和视频帧生成速率
- **Metrics**: ['Token吞吐量(tokens/s)↑', '前向传播次数↓', '视频帧率(frames/s)↑']
- **Expected outcome**: Medusa头使token吞吐量显著高于无Medusa基线；低分辨率适配后可达到实时视频生成帧率
- **Baselines**: ['无Medusa头（0头）自回归基线']
- **Dependencies**: []

## E8: ShotBench分镜检测算法对比与视频转码配置消融
- **Verifies**: C7
- **Setup**:
  - Model: PySceneDetect, Panda70M, TransNetV2（置信阈值0.4）, AutoShot（置信阈值0.4）
  - Hardware: NVIDIA L40S（含NVDEC/NVENC加速器），NVIDIA H100（仅NVDEC）
  - Dataset: ShotBench（含BBC Planet Earth, RAI, ClipShots, SHOT四个子集）
  - System: h264_nvenc编码，PyNvideoCodec视频流处理对比ffmpeg多种配置（libx264/h264_nvenc，不同批大小和CPU核数）
- **Procedure**:
  1. 在ShotBench四个子集上评估四种分镜检测算法的Precision/Recall/F1
  2. 对比ffmpeg不同配置与pynvc+ffmpeg组合的转码吞吐量（videos/s）
- **Metrics**: ['Precision↑', 'Recall↑', 'F1↑（分镜检测）', '转码吞吐量(videos/s)↑']
- **Expected outcome**: TransNetV2在复杂镜头场景F1高于PySceneDetect；PyNvideoCodec组合实现更高转码吞吐量
- **Baselines**: ['PySceneDetect', 'Panda70M', 'ffmpeg + libx264']
- **Dependencies**: []
