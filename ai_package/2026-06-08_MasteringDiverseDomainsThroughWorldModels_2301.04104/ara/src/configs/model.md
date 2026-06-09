## 默认模型规模
- **Value**: 200M参数
- **Rationale**: 在大多数基准中作为默认选择;小型控制任务(Proprio/Visual Control)使用12M即可达到相同性能
- **Search range**: 12M ~ 400M
- **Sensitivity**: 性能随模型规模单调递增,且更大模型需要更少环境交互步数
- **Source**: Methods节 Computational choices部分, Table 3

## 模型维度(d, 200M默认)
- **Value**: 1024
- **Rationale**: 作为所有网络组件宽度的基准;选为8的倍数以保证硬件张量计算效率
- **Search range**: 256(12M) ~ 1536(400M)
- **Sensitivity**: 所有超参数(含学习率和批次大小)在不同模型规模下保持固定不变
- **Source**: Table 3

## 循环单元数(GRU, 200M默认)
- **Value**: 8192(=8×1024)
- **Rationale**: 块对角GRU分为8块;在保持大记忆容量的同时避免参数量和FLOPs的平方级增长
- **Search range**: 1024(12M) ~ 12288(400M)
- **Sensitivity**: 论文未单独消融块数选择
- **Source**: Table 3, Methods节 Networks部分

## CNN基础通道数(200M默认)
- **Value**: 64(=d/16)
- **Rationale**: 图像编/解码器最靠近数据的层通道数为模型维度的1/16,与整体规模同比例缩放
- **Search range**: 16(12M) ~ 96(400M)
- **Sensitivity**: 论文未单独消融
- **Source**: Table 3

## 每个潜态的编码数(200M默认)
- **Value**: 64(=d/16)
- **Rationale**: 离散潜态表示的类别数与模型维度同比例缩放;层数和潜态数量在不同规模下保持固定
- **Search range**: 16(12M) ~ 96(400M)
- **Sensitivity**: 论文未单独消融
- **Source**: Table 3

## 序列模型架构
- **Value**: 块对角GRU(8块);每步输入为z_t、a_t和h_t的线性嵌入拼接
- **Rationale**: 块对角权重矩阵允许块间隔离与混合;线性嵌入拼接输入允许块间信息流动
- **Search range**: 论文未提供其他架构对比
- **Sensitivity**: DreamerV3相对前代引入的架构改进之一
- **Source**: Methods节 Networks部分, Section Previous Dreamer generations

## 编/解码器架构
- **Value**: 图像:步长2 CNN(至6×6或4×4分辨率,解码用转置卷积加sigmoid输出);向量:3层MLP(先经symlog变换)
- **Rationale**: CNN处理高维图像,MLP处理低维向量;symlog变换防止大输入导致重建梯度过大,进一步稳定表示损失的权衡
- **Search range**: 论文未对比其他架构
- **Sensitivity**: 论文未单独消融
- **Source**: Methods节 Networks部分

## 行为者/评论家网络
- **Value**: 3层MLP
- **Rationale**: 在世界模型的抽象表示上训练轻量策略和价值网络
- **Search range**: 论文未对比其他架构
- **Sensitivity**: 论文未单独消融
- **Source**: Methods节 Networks部分

## 奖励与continue预测器
- **Value**: 1层MLP
- **Rationale**: 单层MLP足以从已压缩的模型状态预测标量信号
- **Search range**: 论文未对比其他架构
- **Sensitivity**: 论文未单独消融
- **Source**: Methods节 Networks部分

## 激活函数
- **Value**: RMSNorm + SiLU
- **Rationale**: RMSNorm归一化稳定跨域训练,SiLU提供平滑非线性;相对DreamerV1/V2的架构升级
- **Search range**: 论文未对比其他激活
- **Sensitivity**: 消融实验表明归一化技术对整体性能有贡献
- **Source**: Table 4, Section Previous Dreamer generations

## 潜态分布与unimix
- **Value**: softmax离散类别分布向量,混入1%均匀分布;采用直通梯度
- **Rationale**: 混入1%均匀分布防止零概率和无限对数概率,确保KL散度行为良好;直通梯度允许策略梯度反向传播
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 消融实验表明latent unimix对整体性能有贡献
- **Source**: Section World model learning, Table 4

## 奖励/价值输出分布
- **Value**: 指数间隔bin上的softmax分布(bin范围symexp([-20,+20])),使用twohot目标训练
- **Rationale**: 梯度尺度与预测目标量级解耦;可表示多模态分布;正负bin分开从小到大求和以避免数值精度问题
- **Search range**: bin范围[-20,+20]经symexp变换
- **Sensitivity**: 消融实验表明symexp twohot损失对性能有显著贡献
- **Source**: Section Robust predictions, 式(10)(11)

## 输出层权重初始化
- **Value**: 奖励预测器和评论家的输出权重矩阵初始化为零
- **Rationale**: 防止随机初始化网络在训练初期产生异常大的奖励和价值预测,加速早期学习起步
- **Search range**: N/A
- **Sensitivity**: 论文提到此设计能加速早期学习
- **Source**: Section Critic learning
