显式训练目标(论文公式4):
$$\mathcal { L } = \mathcal { L } _ { a c t i o n } + \alpha \mathcal { L } _ { w o r l d }$$
其中 $\mathcal { L } _ { a c t i o n }$ 为动作模型数据上动作token的交叉熵损失,$\mathcal { L } _ { w o r l d }$ 为世界模型数据上生成图像token的交叉熵损失,$\alpha$ 为平衡系数(用于补偿图像token数量远多于动作token数量的失衡,论文固定为0.04)。

统一模型目标(论文公式3):
$$M _ { \psi } : \left\{ \begin{array} { l } { { a _ { t } = M _ { \psi } ^ { \mathrm { p o l i c y } } ( a _ { t } | \ o _ { t - h : t } , l ) , } } \\ { { o _ { t } = M _ { \psi } ^ { \mathrm { w o r l d } } ( o _ { t } | \ o _ { t - h : t - 1 } , a _ { t - h : t - 1 } ) , } } \end{array} \right.$$

策略分支形式化(论文公式1):
$$a _ { t } = \pi _ { \theta } ( a _ { t } \mid o _ { t - h : t } , l )$$

世界模型分支形式化(论文公式2):
$$o _ { t } = f _ { \phi } \big ( o _ { t } \ \big | \ o _ { t - h : t - 1 } , a _ { t - h : t - 1 } \big )$$

推理期:根据任务目标选择策略分支或世界模型分支单独运行,两分支共享LLM骨干参数;两分支使用不同注意力掩码模式,此为推理期独有设置,不写入训练损失公式。
