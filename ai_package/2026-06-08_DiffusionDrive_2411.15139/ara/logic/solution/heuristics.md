# Heuristics

## H1: K-Means锚点数量 $N_{\mathrm{anchor}}$: NAVSIM上使用20个聚类锚点,nuScenes上使用18个
- **Rationale**: 锚点覆盖训练集中多模式驾驶动作空间,使初始噪声分布更接近目标分布; 相比VADv2的8192个锚点,仅需极少数量即可获得更优性能,大幅降低计算开销
- **Sensitivity**: 论文表8显示将锚点替换为单个外推轨迹时性能显著下降,表明锚点覆盖多样性至关重要; 论文表6显示推理采样数 $N_{\mathrm{infer}}$ 从10增至40时性能存在饱和,间接反映锚点数量的影响
- **Bounds**: NAVSIM主实验: $N_{\mathrm{anchor}}=20$; nuScenes实验: $N_{\mathrm{anchor}}=18$
- **Code ref**: [KMeans, N_anchor]
- **Source**: 论文第3.3节训练部分及第4.2节实现细节

## H2: 扩散计划截断比例: 训练时将1000步扩散计划截断为50步(50/1000)
- **Rationale**: 截断使模型从锚定高斯分布(而非纯高斯噪声)出发去噪,大幅减少推理所需步数,同时保留多模式生成多样性
- **Sensitivity**: 截断比例决定锚点附近噪声量大小; 若截断过小则初始分布几乎无噪声,模型泛化性差; 若截断过大则退化为标准扩散策略,推理步数增加
- **Bounds**: 论文明确使用50/1000截断; 推理时仅需2步去噪即达最优
- **Code ref**: [T_trunc, noise_schedule]
- **Source**: 论文第3.3节截断扩散部分及第4.2节实现细节

## H3: 推理去噪步数: 默认使用2步
- **Rationale**: 截断扩散策略使初始样本已接近目标分布,因此2步即可获得高质量轨迹; 这是实现45 FPS实时性的核心优化手段
- **Sensitivity**: 论文表4显示1步已达可用质量,2步与3步效果基本相同(PDMS均为88.1),边际收益递减
- **Bounds**: 消融实验探索1/2/3步; 主实验选2步
- **Code ref**: [denoising_steps, N_steps]
- **Source**: 论文表4及第4.5节消融研究

## H4: 级联扩散解码器层数(Cascade Stages): 默认使用2层
- **Rationale**: 级联机制使每个去噪步内轨迹特征被迭代精炼,提升轨迹重建质量; 参数在层间共享以控制参数量增长
- **Sensitivity**: 论文表5显示从1层增至2层有明显PDMS提升,增至4层时边际收益饱和且参数量增至65M
- **Bounds**: 消融实验探索1/2/4层; 主实验使用2层(60M参数)
- **Code ref**: [cascade_stages, CascadeDiffusionDecoder]
- **Source**: 论文表5及第4.5节消融研究

## H5: 推理采样数 $N_{\mathrm{infer}}$: 默认使用20
- **Rationale**: 更多采样覆盖更宽的驾驶动作空间; 训练时固定 $N_{\mathrm{anchor}}$ 个轨迹,推理时 $N_{\mathrm{infer}}$ 可灵活调整以适应不同计算资源和场景复杂度
- **Sensitivity**: 论文表6显示 $N_{\mathrm{infer}}=10$ 已达可接受质量(PDMS 84.9), $N_{\mathrm{infer}}=20$ 为主实验设置(PDMS 88.1), $N_{\mathrm{infer}}=40$ 时性能略有提升(PDMS 88.2)但边际递减
- **Bounds**: 消融实验探索10/20/40; 主实验使用20
- **Code ref**: [N_infer]
- **Source**: 论文表6及第3.3节推理灵活性说明
