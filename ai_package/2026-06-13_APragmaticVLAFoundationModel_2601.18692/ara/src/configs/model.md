## 基础视觉语言模型
- **Value**: Qwen2.5-VL
- **Rationale**: LingBot-VLA集成预训练VLM以利用已训练的视觉语言表征，为动作生成提供多模态条件。
- **Search range**: 论文还在吞吐对比中复现Qwen2.5-VL-3B-π和PaliGemma-3B-pt-224-π模型；主架构处显式写Qwen2.5-VL。
- **Sensitivity**: 不同VLM base model会影响吞吐加速倍数；论文未在主文给出模型能力侧的VLM替换消融。
- **Source**: <!--ref:Sec 4.1--> <!--ref:Sec 5.4--> <!--ref:Figure 4-->

## 动作生成模块
- **Value**: initialized action generation module called ‘action expert’
- **Rationale**: action expert接收机器人proprioceptive sequences、initial states和action chunks，用于动作生成预测。
- **Search range**: 论文未给出action expert层数、宽度或参数规模。
- **Sensitivity**: action expert是动作建模路径的核心模块；论文没有单独移除或缩放action expert的实验。
- **Source**: <!--ref:Sec 4.1-->

## 总体架构
- **Value**: Mixture-of-Transformers (MoT) architecture like BAGEL
- **Rationale**: vision-language与action modalities通过不同transformer pathways处理，并由shared self-attention做layer-wise unified sequence modeling。
- **Search range**: 论文描述MoT结构选择，但未给出替代架构网格。
- **Sensitivity**: MoT用于保持模态专用处理并降低cross-modal interference；论文未直接报告MoT对比消融。
- **Source**: <!--ref:Sec 4.1-->

## 输入观测
- **Value**: three-view operational images、task instruction、robot state
- **Rationale**: 观测条件O_t包含三视角图像tokens、任务指令和机器人状态，作为动作chunk条件。
- **Search range**: 论文显式采用三视角operational images；未报告减少或增加视角数量的模型实验。
- **Sensitivity**: 多视角输入支撑环境感知；视角数量敏感性论文未报告。
- **Source**: <!--ref:Sec 4.1 Eq 1-->

## 动作序列表示
- **Value**: A_t=[a_t, a_{t+1}, ..., a_{t+T-1}]
- **Rationale**: 模型把未来动作写成action chunk，以条件分布p(A_t | O_t)进行建模。
- **Search range**: 预训练阶段T=50；论文未给其他T取值。
- **Sensitivity**: T决定预测轨迹时间范围；论文未做T消融。
- **Source**: <!--ref:Sec 4.1 Eq 2-->

## 注意力掩码
- **Value**: blockwise causal attention
- **Rationale**: 联合序列被划分为图像与文本块、状态块和动作块；块间因果，块内双向，防止未来动作信息泄漏到当前观测表示。
- **Search range**: 论文没有给出全因果或全双向attention的对照实验。
- **Sensitivity**: 该设计直接服务于信息泄漏控制；经验敏感性论文未量化。
- **Source**: <!--ref:Sec 4.1-->

## 空间增强模块
- **Value**: learnable queries对齐LingBot-Depth tokens，Proj使用cross-attention做维度对齐
- **Rationale**: 通过深度token对齐向LingBot-VLA注入几何信息，以改善复杂操作任务中的空间感知。
- **Search range**: 论文描述三视角queries和depth tokens；未提供depth encoder替换或projection结构网格。
- **Sensitivity**: w/ depth变体整体优于相关基线和w/o depth若干设置；单独模块敏感性未展开。
- **Source**: <!--ref:Sec 4.1--> <!--ref:Sec 5.2--> <!--ref:Sec 5.3-->

## 语言标注模型
- **Value**: Qwen3-VL-235B-A22B用于task and sub-task instructions annotation
- **Rationale**: 论文用该模型对任务与子任务指令做精确标注，形成训练语言条件。
- **Search range**: 论文未比较其他标注模型。
- **Sensitivity**: 标注质量对语言条件可能重要；这是分析推断,论文未显式声明。
- **Source**: <!--ref:Sec 3.2-->
