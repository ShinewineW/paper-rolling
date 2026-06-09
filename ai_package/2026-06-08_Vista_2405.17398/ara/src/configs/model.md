## 模型总参数量
- **Value**: 2.5B
- **Rationale**: 基于SVD框架的完整模型参数规模，包含UNet、图像编码器及视频感知解码器
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Appendix C.1

## UNet参数量
- **Value**: 1.6B
- **Rationale**: UNet去噪网络的参数量，与SVD框架架构保持一致
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Appendix C.1

## 单次生成帧数K
- **Value**: 25
- **Rationale**: 每次前向预测生成25帧视频；在10 Hz下对应2.5秒
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 2, Appendix C.2

## 推理分辨率
- **Value**: 576×1024
- **Rationale**: 最终推理时的空间分辨率，高于所有已知对比基线方法
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Table 1, Sec 3.2

## 视频帧率
- **Value**: 10 Hz
- **Rationale**: 时序分辨率，高于大多数现有驾驶世界模型
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Table 1, Sec 1

## 动作Fourier嵌入通道数
- **Value**: 128
- **Rationale**: 所有异构动作序列统一编码为128通道的Fourier嵌入，构成统一条件接口
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Appendix C.1

## LoRA秩
- **Value**: 16
- **Rationale**: 阶段二所有注意力块中LoRA低秩适配器的秩，在参数效率与适配能力间取得平衡
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## DDIM采样步数
- **Value**: 50
- **Rationale**: 推理时DDIM去噪器的采样步数
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.4

## 采样起始噪声σmax
- **Value**: 700.0
- **Rationale**: DDIM采样从σmax=700.0处开始向σ0=0去噪
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.4

## 三角CFG时序最小引导尺度smin
- **Value**: 1.0
- **Rationale**: 三角形无分类器引导方案中时序方向的最小引导尺度
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.4

## 三角CFG时序最大引导尺度smax
- **Value**: 2.5
- **Rationale**: 三角形无分类器引导方案的时序最大引导尺度，过高会导致自回归预测过饱和漂移
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.4

## 自回归预测重叠帧数
- **Value**: 3
- **Rationale**: 相邻预测片段重叠3帧以保证内容连续性；重叠帧像素级均值后输入视频感知解码器
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Appendix C.4

## 奖励估计集成大小M
- **Value**: 5
- **Rationale**: 每次奖励估计从M=5个独立噪声出发去噪，以可靠地近似条件方差
- **Search range**: 论文测试了M=5和M=10两种设置
- **Sensitivity**: 低
- **Source**: Appendix C.6, D.1

## 奖励估计去噪步数
- **Value**: 10
- **Rationale**: 奖励估计无需完整高质量生成；10步去噪已足够有效估计不确定性
- **Search range**: 论文测试了5步和10步两种设置
- **Sensitivity**: 中
- **Source**: Appendix C.6, D.1

## 奖励估计轨迹扰动关联策略系数β
- **Value**: 0.5
- **Rationale**: 关联采样策略中控制轨迹扰动方向一致性的系数
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.6
