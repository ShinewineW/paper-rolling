# Heuristics

## H1: 用 DeepSeek-R1 为 SFT 数据批量生成长链式思维推理轨迹(知识蒸馏)
- **Rationale**: R1 具备强推理能力,可为物理常识和具身推理问题生成高质量 CoT 轨迹,大幅降低人工标注成本
- **Sensitivity**: 高——问题设计必须确保答案无法直接从 caption 中检索,否则 R1 产生平凡轨迹,导致 SFT 样本无效
- **Bounds**: R1 不具备视觉能力,视觉信息须先由 VLM 转换为文字 caption 后才可送入;对象永久性任务中该方案效果欠佳,需改用中间版 Cosmos-Reason1-7B 提取轨迹
- **Code ref**: [—]
- **Source**: Sec. 5.1.1, 5.1.2

## H2: SFT 阶段对各数据域进行均衡采样,RL 阶段以等概率从各 RL 数据集采样
- **Rationale**: 防止特定领域数据过度代表导致模型偏斜,保证物理常识、具身推理、直觉物理各子任务均衡学习
- **Sensitivity**: 中——均衡策略可能牺牲各子任务的极致性能以换取整体覆盖
- **Bounds**: SFT 均衡采样仅在本文报告的多域联合训练场景下有明确描述
- **Code ref**: [—]
- **Source**: Sec. 7.1, 7.2.1

## H3: RL 训练时对多选题选项进行即时随机打乱(on-the-fly shuffle)
- **Rationale**: 防止模型产生位置偏见(如固定偏好选 A),强迫模型基于内容推理而非选项位置
- **Sensitivity**: 高——不打乱易产生虚假奖励提升,影响 RL 训练有效性
- **Bounds**: 仅适用于 MCQ 格式;选项打乱需保持正确答案映射的一致性
- **Code ref**: [shuffle_choices]
- **Source**: Sec. 7.2.1

## H4: 利用三类自监督直觉物理任务(时间箭头/空间拼图/客体恒常性)构造可大规模扩展的 RL 数据,无需人工标注
- **Rationale**: 时间箭头只需视频反转、空间拼图可应用于任意图像、客体恒常性可在任意仿真环境中实现,数据生成成本极低且天然具有可验证答案
- **Sensitivity**: 低——自动化生成流水线简单;但需避免 SFT 与 RL 数据集的片段重叠以防止提前饱和
- **Bounds**: 仅覆盖直觉物理三个子能力,不涵盖完整的物理常识本体
- **Code ref**: [IntuitionPhysicsRL]
- **Source**: Sec. 5.1.3, 5.2, 7.2.3

## H5: 策略训练节点与演员 rollout 节点异步解耦部署,由统一调度器分发训练提示,相较 colocated 框架训练效率提升约 160%
- **Rationale**: 主流 colocated 框架中策略训练与 rollout 串行等待导致资源利用率低;异步并行消除同步开销
- **Sensitivity**: 高——依赖定制化 NCCL 通信器与训练网格管理逻辑;节点故障时框架可自动重配置并继续当前训练步
- **Bounds**: 工程复杂度较高;动态扩缩容支持依赖调度器冗余机制
- **Code ref**: [AsyncRLDispatcher]
- **Source**: Sec. 4.2
