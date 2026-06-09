## 图像tokenizer参数量
- **Value**: 0.3B
- **Rationale**: 全卷积2D U-Net离散图像自编码器
- **Search range**: [0.1B, 1B]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像输入分辨率
- **Value**: 288×512
- **Rationale**: 9/16宽高比，接近标准驾驶相机输出
- **Search range**: N/A（固定）
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像空间下采样因子D
- **Value**: 16
- **Rationale**: tokenizer在高度和宽度方向各下采样16倍，决定token序列长度
- **Search range**: [8, 32]
- **Sensitivity**: high
- **Source**: Sec 4.1

## 图像codebook词汇量K
- **Value**: 8192
- **Rationale**: 离散token词汇表大小，平衡序列长度与语义表达容量
- **Search range**: [4096, 32768]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 每帧图像token数n
- **Value**: 576
- **Rationale**: 18×32=576，由分辨率288×512除以下采样因子16得到
- **Search range**: 由D和分辨率决定
- **Sensitivity**: high
- **Source**: Sec 2.1

## 每时间步文本token数m
- **Value**: 32
- **Rationale**: T5-large编码后映射至32个文本token，通过线性层投影至d维空间
- **Search range**: [16, 64]
- **Sensitivity**: medium
- **Source**: Sec 2.1

## 每时间步动作token数l
- **Value**: 2
- **Rationale**: 速度与曲率各1个标量token，通过线性层独立映射至d维空间
- **Search range**: 固定为2（速度+曲率）
- **Sensitivity**: N/A
- **Source**: Sec 2.1

## 世界模型共享嵌入维度d
- **Value**: 4096
- **Rationale**: 所有模态token的公共嵌入空间维度，同时也是空间位置嵌入的维度
- **Search range**: [1024, 8192]
- **Sensitivity**: high
- **Source**: Sec 2.1

## 每时间步空间位置数（m+n+l）
- **Value**: 610
- **Rationale**: 32+576+2=610，为每时间步文本、图像、动作token的总槽位数
- **Search range**: 由m、n、l决定
- **Sensitivity**: N/A
- **Source**: Sec 2.1

## 世界模型参数量
- **Value**: 6.5B
- **Rationale**: 因果掩码autoregressive transformer，为当前三个可训练组件中参数量最大的
- **Search range**: 缩放实验代理模型：0.65M 至 650M
- **Sensitivity**: high
- **Source**: Sec 4.2

## 世界模型训练序列帧数T
- **Value**: 26
- **Rationale**: 每训练样本包含26帧，在6.25Hz下对应约4秒视频
- **Search range**: [8, 64]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型视频降采样频率
- **Value**: 6.25 Hz
- **Rationale**: 从25Hz时序降采样至6.25Hz以控制序列长度，视频解码器负责恢复至25Hz
- **Search range**: N/A（固定）
- **Sensitivity**: medium
- **Source**: Sec 2.3

## 世界模型总序列长度
- **Value**: 15860
- **Rationale**: T×(m+n+l)=26×(32+576+2)=15860
- **Search range**: 由T、m、n、l决定
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 视频解码器参数量
- **Value**: 2.6B
- **Rationale**: 3D U-Net扩散解码器，含分解式时空注意力层
- **Search range**: [1B, 5B]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器训练窗口长度T'
- **Value**: 7
- **Rationale**: 每次扩散解码处理7帧，支持6.25Hz、12.5Hz和25Hz三种采样率
- **Search range**: [4, 16]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 推理时DDIM扩散步数
- **Value**: 50
- **Rationale**: 平衡视频解码质量与推理速度
- **Search range**: [20, 100]
- **Sensitivity**: medium
- **Source**: Sec 5.2

## 推理时top-k采样参数k
- **Value**: 50
- **Rationale**: 从概率最高的50个token中采样，其perplexity分布与真实token最接近
- **Search range**: [10, 200]
- **Sensitivity**: high
- **Source**: Sec 5.1

## 视频解码器推理时图像/视频混合解码权重w
- **Value**: 0.5
- **Rationale**: 以0.5权重融合单帧图像解码与序列联合解码，平衡token信息保真度与时序一致性
- **Search range**: [0.3, 0.7]
- **Sensitivity**: medium
- **Source**: Sec 5.2

## 视频解码器推理时混合解码应用概率p
- **Value**: 0.25
- **Rationale**: 每个扩散步以0.25概率随机应用加权平均解码策略
- **Search range**: [0.1, 0.5]
- **Sensitivity**: medium
- **Source**: Sec 5.2

## 文本编码器
- **Value**: T5-large
- **Rationale**: 预训练文本编码器，权重固定，通过可训练线性层将编码映射至d维嵌入空间
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 2.1
