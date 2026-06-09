训练期显式目标公式(Eq.1-6, 均为训练期使用):

潜变量替换构造输入: $$\pmb { \hat { n } } = \pmb { m } \cdot \pmb { z } + ( 1 - \pmb { m } ) \cdot \pmb { n }$$

标准扩散损失 (Eq.1): $$\mathcal { L } _ { \mathrm { d i f f u s i o n } } = \mathbb { E } _ { z , \sigma , \hat { n } } \Big [ \sum _ { i = 1 } ^ { K } ( 1 - m _ { i } ) \odot \| D _ { \theta } ( \hat { n } _ { i } ; \sigma ) - z _ { i } \| ^ { 2 } \Big ]$$

动态感知权重 (Eq.2, 训练期辅助量, sg(·) 截断梯度后用作自适应重加权): $$w _ { i } = \| ( D _ { \theta } ( \hat { n } _ { i } ; \sigma ) - D _ { \theta } ( \hat { n } _ { i - 1 } ; \sigma ) ) - ( z _ { i } - z _ { i - 1 } ) \| ^ { 2 }$$

动态增强损失 (Eq.3): $$\mathcal { L } _ { \mathrm { d y n a m i c s } } = \mathbb { E } _ { z , \sigma , \hat { n } } \Big [ \sum _ { i = 2 } ^ { K } \mathrm { s g } ( w _ { i } ) \odot ( 1 - m _ { i } ) \odot \| D _ { \theta } ( \hat { n } _ { i } ; \sigma ) - z _ { i } \| ^ { 2 } \Big ]$$

频域高通滤波提取结构特征 (Eq.4, 训练期辅助操作): $$z _ { i } ^ { \prime } = \mathcal { F } ( z _ { i } ) = \mathrm { I F F T } \big ( \mathcal { H } \odot \mathrm { F F T } ( z _ { i } ) \big )$$

结构保留损失 (Eq.5): $$\mathcal { L } _ { \mathrm { s t r u c t u r e } } = \mathbb { E } _ { z , \sigma , \hat { n } } \Big [ \sum _ { i = 1 } ^ { K } ( 1 - m _ { i } ) \odot \| \mathcal { F } ( D _ { \theta } ( \hat { n } _ { i } ; \sigma ) ) - \mathcal { F } ( z _ { i } ) \| ^ { 2 } \Big ]$$

最终训练目标 (Eq.6): $$\mathcal { L } _ { \mathrm { f i n a l } } = \mathcal { L } _ { \mathrm { d i f f u s i o n } } + \lambda _ { 1 } \mathcal { L } _ { \mathrm { d y n a m i c s } } + \lambda _ { 2 } \mathcal { L } _ { \mathrm { s t r u c t u r e } }$$

第二阶段动作可控性学习沿用相同 Eq.6 损失, 仅更新 LoRA 与投影层参数。奖励函数(Eq.7-8)和三角形 CFG 引导方案(Eq.9)仅在推理期使用, 不属于训练目标。
