## Cosmos-Reason1-7B 视觉编码器
- **Value**: ViT-676M，32 层，模型维度 1280，FFN 隐层维度 3456，patch 尺寸 14×14，动态分辨率输入
- **Rationale**: 较大的 ViT 提供更强视觉特征提取，动态分辨率兼顾不同输入图像
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Tab. 3

## Cosmos-Reason1-56B 视觉编码器
- **Value**: InternViT-300M-V2.5（ViT-300M），24 层，模型维度 1024，FFN 隐层维度 4096，patch 尺寸 14×14，固定输入 448×448
- **Rationale**: 与 Nemotron-H 主干配合，采用固定分辨率输入以统一处理流程
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 3.1, Tab. 3

## 投影器（Projector）结构
- **Value**: 两层 MLP；7B 下采样率 2×2×2（高×宽×时间），56B 下采样率 2×2×1（高×宽，不压缩时间）；7B 输入维度 1280、隐层 5120、输出 3584；56B 输入维度 4096、隐层 32768、输出 8192
- **Rationale**: 通过空间下采样减少 LLM 输入 token 数，降低计算量；时间维度处理策略因模型大小而异
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Tab. 3

## Cosmos-Reason1-7B LLM 主干
- **Value**: 密集 Transformer，28 层，模型维度 3584，FFN 隐层维度 18944，注意力头数 28，基于 Qwen2.5-VL 预训练权重
- **Rationale**: 密集 Transformer 在推理任务中性能稳定；从 Qwen2.5-VL 出发降低训练成本
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 3.1, Tab. 3

## Cosmos-Reason1-56B LLM 主干
- **Value**: 混合 Mamba-MLP-Transformer（Nemotron-H），118 层，模型维度 8192，FFN 隐层维度 32768，注意力头数 64
- **Rationale**: Mamba 提供线性时间序列建模效率，少量 Transformer 层补偿长上下文细节捕捉能力
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 3.2, Tab. 3

## 多模态架构类型
- **Value**: 仅解码器架构（decoder-only），类似 LLaVA 与 NVLM-D；视觉 token 对齐到文本 token 嵌入空间后拼接输入 LLM
- **Rationale**: 仅解码器架构统一处理所有模态，在多模态推理任务中优于交叉注意力架构
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 3.1

## 视频帧采样配置（Cosmos-Reason1-56B）
- **Value**: 均匀采样最多 32 帧，最大帧率 2fps，每帧缩放至 448×448 像素
- **Rationale**: 限制帧数控制 token 总量；2fps 足以覆盖动作级别时序信息
- **Search range**: 最多 32 帧
- **Sensitivity**: medium
- **Source**: Sec 3.1

## 视觉 token 数量（Cosmos-Reason1-56B 每帧）
- **Value**: ViT 输出 1024 个 token，经 PixelShuffle 2×2 下采样后压缩为 256 个 token
- **Rationale**: PixelShuffle 将空间维度折叠至通道维度，在减少 token 数的同时保留空间信息
- **Search range**: 输出 256 tokens/帧
- **Sensitivity**: medium
- **Source**: Sec 3.1

## 图像分块策略（Cosmos-Reason1-56B）
- **Value**: 根据分辨率动态分割为 1 至 12 个瓦片，每块 448×448 像素；额外生成 1 个缩略图保留全局上下文；多瓦片 token 通过交错瓦片 ID 标签拼接
- **Rationale**: 动态分块兼顾不同分辨率图像；缩略图保留宏观语义信息
- **Search range**: 1~12 tiles
- **Sensitivity**: medium
- **Source**: Sec 3.1

## RL 训练框架架构
- **Value**: 全异步三组件框架：Dispatcher（调度分发）、Actor Rollout（响应生成与奖励计算）、Policy Training（策略优化）；策略训练节点支持 5D 并行（DP、PP、CP、FSDP、TP）；rollout 节点支持 DP、PP、TP；采用定制 NCCL 通信器
- **Rationale**: 异构部署策略解耦训练与推理节点，消除同步开销；相较于同址框架训练效率提升约 160%
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 4.2

## RL 训练框架容错设计
- **Value**: 训练网格管理逻辑支持节点失效时快速重构并继续当前训练步；Dispatcher 冗余机制提升鲁棒性；原生支持动态扩缩容
- **Rationale**: 大规模 RL 训练时节点失效不可避免，容错设计避免代价高昂的重启恢复
- **Search range**: N/A
- **Sensitivity**: low
- **Source**: Sec 4.2
