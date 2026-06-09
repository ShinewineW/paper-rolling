# Related Work

## R1: Kingma & Welling, 2013
- **DOI**: arXiv:1312.6114
- **Type**: 方法基础
- **Delta**:
  - What changed: 直接采用VAE作为V模型将高维像素帧压缩为低维潜向量z；在RL流水线中引入高斯先验以提升世界模型对MDN-RNN生成的异常z向量的鲁棒性，其余结构未改动
  - Why: VAE提供了有效的高维图像压缩表示，为MDN-RNN和控制器提供低维输入，是V-M-C架构的视觉基础
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['ConvVAE作为视觉模块V', '高斯先验增强世界模型鲁棒性']

## R2: Graves, 2013
- **DOI**: arXiv:1308.0850
- **Type**: 方法基础
- **Delta**:
  - What changed: 将MDN-RNN从建模笔画序列转为建模潜空间序列z；在VizDoom任务中增加done状态预测；取消协方差ρ参数，仅输出对角协方差矩阵的分解高斯混合分布
  - Why: MDN-RNN是本文M模型的核心，为智能体提供时序预测与概率不确定性建模能力，支撑梦境环境构建和策略迁移
- **Claims affected**: ['C1', 'C3', 'C4']
- **Adopted elements**: ['LSTM与混合密度网络（MDN）输出层的组合', '以高斯混合分布建模下一潜向量概率分布']

## R3: Hansen, 2016
- **DOI**: arXiv:1604.00772
- **Type**: 优化算法
- **Delta**:
  - What changed: 直接应用CMA-ES优化控制器C的权重，无算法改动；针对小参数量（867~1088个参数）线性控制器场景，利用多CPU并行评估多个候选策略
  - Why: CMA-ES适合数千参数以内的优化问题并易于并行化，配合参数极少的线性控制器可高效搜索策略空间，无需可微目标函数
- **Claims affected**: ['C1']
- **Adopted elements**: ['CMA-ES作为Controller C的优化算法', '种群大小64，每代每个个体16次随机种子评估']

## R4: Deisenroth & Rasmussen, 2011
- **DOI**: http://mlg.eng.cam.ac.uk/pub/pdf/DeiRas11.pdf
- **Type**: 对比方法
- **Delta**:
  - What changed: 本文以MDN-RNN替代高斯过程动力学模型以应对高维像素输入；PILCO用贝叶斯不确定性缓解模型不完美问题但难以扩展至高维视觉输入，本文通过温度τ在近似概率模型中引入随机性部分实现类似效果
  - Why: PILCO是概率模型方法的代表性基线，论文借其说明基于不确定性缓解对抗性策略的局限性，为温度参数设计提供了对比背景
- **Claims affected**: ['C4']
- **Adopted elements**: []

## R5: Schmidhuber, 2015a
- **DOI**: arXiv:1511.09249
- **Type**: 理论框架
- **Delta**:
  - What changed: 本文是对Learning to Think框架的简化实验性实现；采用进化策略优化C而非框架中更通用的方案；M仍逐步预测（step-by-step），未实现框架中C利用M子程序进行层级规划的更通用机制
  - Why: Learning to Think提供了RNN世界模型加控制器组合的统一理论框架，是本文方法论、术语体系和迭代训练流程的主要参考来源
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['V-M-C命名体系', '迭代训练流程（Iterative Training Procedure）']

## R6: Schmidhuber, 1990a/b/1991a
- **DOI**: http://people.idsia.ch/~juergen/FKI-126-90_(revised)bw_ocr.pdf
- **Type**: 历史奠基工作
- **Delta**:
  - What changed: 早期系统为确定性RNN动力学模型，易被控制器利用；本文以MDN-RNN引入概率建模并用温度τ控制随机性，以CMA-ES替代传统RL对控制器进行优化，部分缓解了确定性模型的可利用性问题
  - Why: 1990年代的C-M系统是本文方法的直接前身，论文在多处明确对齐与该系列工作的异同，并指出本文与Learning to Think相比更接近这些早期系统
- **Claims affected**: ['C1', 'C4']
- **Adopted elements**: ['RNN世界模型与分离控制器的C-M范式']
