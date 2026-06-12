# Experiments

## E1: 子系统定义核对
- **Verifies**: C1
- **Setup**:
  - Model: 论文中的 true world model 形式化定义
  - Hardware: 未指定
  - Dataset: 冻结论文 markdown
  - System: 生成核心、交互闭环、记忆系统的概念框架
- **Procedure**:
  1. 读取论文关于 true world model 的定义段落。
  2. 核对生成核心是否覆盖状态转移、观测、奖励和终止。
  3. 核对交互闭环是否包含状态推断、策略和值函数。
  4. 核对记忆系统是否以历史状态更新支撑长时域一致性。
- **Metrics**: ['子系统覆盖完整性', '属性与子系统对应关系', '是否区分统一模型前体与真世界模型']
- **Expected outcome**: 若论文定义成立，完整系统应比仅有统一生成能力的系统更接近持久、能动和涌现的世界。
- **Baselines**: ['仅具备生成核心的 Unified Model', '传统控制导向 world model']
- **Dependencies**: []

## E2: 阶段路线图归纳核对
- **Verifies**: C2
- **Setup**:
  - Model: 论文提出的五阶段路线图
  - Hardware: 未指定
  - Dataset: 冻结论文 markdown 与代表方法表
  - System: 从 Mask-based Models 到 True World Models 的文献组织
- **Procedure**:
  1. 抽取摘要、引言和阶段小结中的能力递进描述。
  2. 对照代表方法表，检查各阶段是否对应不同能力中心。
  3. 核对论文是否把 Stage V 表述为前序阶段的综合而非新增单一组件。
- **Metrics**: ['阶段边界清晰度', '代表方法与阶段能力的一致性', '能力缺口是否推动下一阶段']
- **Expected outcome**: 若路线图成立，后续阶段应逐步补足前一阶段缺少的统一、交互和记忆能力。
- **Baselines**: ['宽泛罗列式 survey', '只按应用领域划分的 world model 分类']
- **Dependencies**: ['E1']

## E3: 长时域一致性瓶颈核对
- **Verifies**: C3
- **Setup**:
  - Model: 论文中的交互生成模型与记忆一致性系统分析
  - Hardware: 未指定
  - Dataset: 冻结论文 markdown
  - System: 隐式视频生成、显式空间表示、外部化记忆和一致性策略
- **Procedure**:
  1. 读取 Stage III 对实时交互生成的能力与局限描述。
  2. 读取 Stage IV 对外部化记忆、容量扩展和一致性调控的描述。
  3. 核对论文是否将遗忘、漂移和动态状态维护列为从交互到持久世界的关键问题。
- **Metrics**: ['遗忘与漂移问题覆盖度', '显式空间表示与隐式视频表示的局限对比', '记忆策略与一致性目标的对应关系']
- **Expected outcome**: 若论文论证成立，加入记忆和一致性策略的系统应比单纯实时交互系统更能维持长期连贯世界。
- **Baselines**: ['单次生成模型', '无显式记忆管理的实时交互生成模型', '仅依赖显式静态空间表示的场景生成系统']
- **Dependencies**: ['E2']
