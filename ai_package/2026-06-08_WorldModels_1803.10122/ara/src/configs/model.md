## VAE潜在向量维度Nz（CarRacing）
- **Value**: 32
- **Rationale**: 对赛车场景帧内容进行压缩表示，32维在表达能力与压缩率之间取得平衡
- **Search range**: CarRacing=32，VizDoom=64
- **Sensitivity**: 中等；维度过小会丢失关键视觉信息，影响控制器决策质量
- **Source**: Appendix A.1, Sec 3.2

## VAE潜在向量维度Nz（VizDoom）
- **Value**: 64
- **Rationale**: Doom环境视觉场景更复杂（3D渲染、多个怪物），需要更大的潜在空间来捕捉关键信息
- **Search range**: CarRacing=32，VizDoom=64
- **Sensitivity**: 中等
- **Source**: Appendix A.1, Sec 4.2

## ConvVAE卷积和反卷积层数
- **Value**: 各4层
- **Rationale**: 对64×64×3输入进行逐步下采样/上采样，提取层次化空间特征
- **Search range**: 两个任务均使用4层
- **Sensitivity**: 中等
- **Source**: Appendix A.1

## 卷积步长
- **Value**: 2（所有卷积和反卷积层）
- **Rationale**: 使用步长代替池化层实现降采样，保留空间信息的同时减少参数量
- **Search range**: 论文所有层均使用步长2
- **Sensitivity**: 低；标准做法
- **Source**: Appendix A.1

## MDN高斯混合成分数
- **Value**: 5
- **Rationale**: 混合高斯允许建模多模态分布，对包含随机离散事件（如怪物是否射出火球）的环境尤为重要；单高斯无法捕捉此类离散模态
- **Search range**: 两个任务均使用5个混合成分
- **Sensitivity**: 中等；成分数过少无法捕捉多模态动态，过多则增加计算负担
- **Source**: Appendix A.2, Sec 4.5

## LSTM隐藏单元数（CarRacing）
- **Value**: 256
- **Rationale**: 足够捕捉赛车任务的时序动态（速度、方向、赛道形状预测），保持MDN-RNN参数量在合理范围
- **Search range**: CarRacing=256，VizDoom=512
- **Sensitivity**: 中等；隐藏单元过少会降低时序建模能力
- **Source**: Appendix A.2

## LSTM隐藏单元数（VizDoom）
- **Value**: 512
- **Rationale**: Doom任务需要同时跟踪多个火球轨迹、游戏逻辑和3D渲染状态，需要更大的记忆容量
- **Search range**: CarRacing=256，VizDoom=512
- **Sensitivity**: 中等
- **Source**: Appendix A.2

## 控制器参数量（CarRacing）
- **Value**: 867
- **Rationale**: 线性控制器 $a_t = W_c [z_t\ h_t] + b_c$ 参数量极少，使CMA-ES在数百参数量级的解空间中高效优化成为可能
- **Search range**: CarRacing=867，VizDoom=1088
- **Sensitivity**: 极高；参数量小是使用进化策略优化控制器的前提条件，若参数过多则CMA-ES无法扩展
- **Source**: Sec 2.3, Sec 3.2

## 控制器参数量（VizDoom）
- **Value**: 1088
- **Rationale**: VizDoom任务中控制器输入同时包含LSTM的隐藏向量h和细胞向量c，导致输入维度更大
- **Search range**: CarRacing=867，VizDoom=1088
- **Sensitivity**: 极高
- **Source**: Sec 4.2, Appendix A.3

## 输入图像分辨率
- **Value**: 64×64×3（RGB，像素值归一化至[0,1]）
- **Rationale**: 将原始帧下采样至64×64以减少VAE计算量，RGB三通道浮点表示
- **Search range**: 两个任务均使用64×64
- **Sensitivity**: 中等；更高分辨率可捕捉更多细节但显著增加VAE训练成本
- **Source**: Appendix A.1

## 温度参数τ（MDN-RNN采样）
- **Value**: 可调；VizDoom梦境训练使用1.15
- **Rationale**: 控制MDN-RNN输出分布的随机程度；较高的τ使环境更难以被控制器利用，防止对抗性策略的产生
- **Search range**: 论文实验范围0.10至1.30
- **Sensitivity**: 极高；τ=0.10时模式崩溃，真实迁移完全失败；τ=1.15时迁移效果最优
- **Source**: Sec 2.2, Sec 4.5, Table 2
