# Concepts

## Drive-OccWorld
- **Notation**: 论文将其形式化为由生成式 world model $\mathcal { W }$ 与 planner $\mathcal { P }$ 组成的自回归框架，使用历史观测、历史与未来状态、action conditions 预测下一状态，并用 $f _ { o }$ 选择下一轨迹。
- **Definition**: 一种面向自动驾驶的 vision-centric 4D occupancy forecasting and planning world model，将历史多视角图像编码为 BEV embeddings，经 memory queue 聚合后由 world decoder 预测未来 semantic occupancy 和 flow，并与 occupancy-based planner 结合进行连续预测与规划。
- **Boundary conditions**: 它不是单纯的视频生成 world model，也不是只做预训练的 world model；本文强调未来 occupancy、flow forecasting 与 end-to-end planning 的结合。
- **Related concepts**: ['4D occupancy forecasting', 'Memory Queue', 'World Decoder', 'Action Conditions', 'Occupancy-based Planner']

## 4D occupancy forecasting
- **Notation**: 未来状态在预备部分写作 $\{ s _ { 1 } , \ldots , s _ { f } \}$；未来 occupancy 和 flow 预测头输出 $( S _ { + t } , \mathcal { F } _ { + t } ) \in \mathbb { R } ^ { h \times \hat { w } \times d }$。
- **Definition**: 根据历史和当前观测预测近未来占据状态，即周围环境如何随时间演化；本文包含 inflated GMO、fine-grained GMO、fine-grained GMO and GSO 等占据格式，并同时预测 flow。
- **Boundary conditions**: 它不同于只恢复当前 occupancy 的 occupancy prediction；本文关心的是 future timestamps 的语义占据和动态流。
- **Related concepts**: ['Drive-OccWorld', 'World Decoder', '3D backward centripetal flow', 'GMO', 'GSO']

## Memory Queue
- **Notation**: 文中记为 $w _ { \mathscr { M } }$，world decoder 基于其中的 historical BEV features 和 expected action condition $a _ { + t }$ 预测未来 BEV embeddings。
- **Definition**: Drive-OccWorld 中积累历史信息的模块，存储历史 BEV features，并通过 semantic- and motion-conditional normalization 聚合语义信息和补偿动态运动，从而形成更有代表性的历史 BEV features。
- **Boundary conditions**: 它不是最终规划器，也不直接输出轨迹；其输出作为 world decoder 的历史上下文。
- **Related concepts**: ['Semantic- and Motion-Conditional Normalization', 'BEV embeddings', 'World Decoder']

## Semantic- and Motion-Conditional Normalization
- **Notation**: $$\tilde { F } ^ { b e v } = \gamma ^ { * } \cdot L a y e r N o r m ( F ^ { b e v } ) + \beta ^ { * }\tag{5}$$
- **Definition**: 一种在 latent space 中增强 historical BEV embeddings 的归一化方法，先执行不带 affine mapping 的 layer normalization，再用来自语义或运动标签的 scale 与 shift 参数调制 BEV features。
- **Boundary conditions**: 它是特征调制模块，不是单独的 occupancy decoder；语义参数来自 voxel-wise semantic predictions，运动参数来自 ego-pose transformation 与 3D backward centripetal flow。
- **Related concepts**: ['Memory Queue', 'BEV embeddings', '3D backward centripetal flow', 'ego-pose transformation']

## BEV embeddings
- **Notation**: 文中示例为 $\pmb { F } ^ { b e v } \ \in \ \mathbb { R } ^ { h \times w \times c }$，其中 h 与 w 是 BEV 空间分辨率，c 是通道维度。
- **Definition**: 由 history encoder 从 historical camera images 中提取并转换得到的 bird’s-eye-view 表示，用于承载多视角几何信息和后续时序预测。
- **Boundary conditions**: 它不是原始相机图像，也不是最终 voxel occupancy 标签；它是模型内部的 latent BEV feature。
- **Related concepts**: ['History Encoder', 'Memory Queue', 'Semantic- and Motion-Conditional Normalization', 'World Decoder', 'BEV Refinement']

## World Decoder
- **Notation**: 文中记为 $\mathcal { W } _ { \mathcal { D } }$；learnable BEV queries $Q \in \mathbb { R } ^ { h \times w \times c }$ 经过 deformable self-attention、temporal cross-attention、conditional cross-attention 与 feedforward network 输出 generated BEV features。
- **Definition**: Drive-OccWorld 的自回归 transformer decoder，基于 memory queue 中的历史 BEV features 和 expected action conditions 预测下一时刻 BEV embeddings，再通过预测头生成 semantic occupancy 与 3D backward centripetal flow。
- **Boundary conditions**: 它预测环境状态特征和 occupancy-flow 输出，不直接以最低 cost 选择轨迹；轨迹选择由 occupancy-based planner 处理。
- **Related concepts**: ['Memory Queue', 'Action Conditions', 'BEV embeddings', '4D occupancy forecasting']

## Action Conditions
- **Notation**: velocity 写作 $( v _ { x } , v _ { y } )$；trajectory 写作 $( \bar { \bigtriangleup } x , \triangle y )$；在 world model 预备公式中 ego actions 写作 $\{ a _ { - h } , \dotsc , a _ { - 1 } , a _ { 0 } \}$。
- **Definition**: 注入 world model 的 ego motion 条件，用于 action-controllable generation；本文包括 velocity、steering angle、trajectory 和 high-level commands。
- **Boundary conditions**: 在 action-controllable generation 中可以使用多种形式的 a；在 end-to-end planning 中，论文强调使用 predicted trajectories 作为 action conditions，以避免 GT ego actions 泄漏到 planner。
- **Related concepts**: ['Unified Conditioning Interface', 'World Decoder', 'Drive-OccWorld', 'Occupancy-based Planner']

## Unified Conditioning Interface
- **Notation**: 条件嵌入与 BEV queries 在 $\mathcal { W } _ { \mathcal { D } }$ 的 conditional cross-attention 中交互。
- **Definition**: 用于把异构 action conditions 统一编码为 coherent embedding 的接口，先通过 Fourier embeddings 编码所需 actions，再拼接并由 learned projections 融合，使其维度与 world decoder 的 conditional cross-attention layers 对齐。
- **Boundary conditions**: 它不是简单把条件相加到 BEV queries；论文实验讨论中指出 cross-attention 比 additive embeddings 更有效。
- **Related concepts**: ['Action Conditions', 'World Decoder', 'conditional cross-attention', 'Fourier embeddings']

## 3D backward centripetal flow
- **Notation**: 文中写作 $\mathbf { \bar { \mathcal { F } } } \in \mathbb { R } ^ { \mathbf { \bar { h } } \times w \times d \times 3 }$，并由 prediction heads 输出未来 $( S _ { + t } , \mathcal { F } _ { + t } )$。
- **Definition**: 一种 voxel-wise flow，指向当前时刻 voxel 在前一时刻对应的 3D instance center，用于刻画动态对象运动并辅助 flow forecasting 与 motion-aware normalization。
- **Boundary conditions**: 它不是二维 optical flow，也不是只描述 ego vehicle 的运动；论文用它处理其他 agents 的细粒度运动感知。
- **Related concepts**: ['4D occupancy forecasting', 'Semantic- and Motion-Conditional Normalization', 'Flow Forecasting', 'GMO']

## Occupancy-based Planner
- **Notation**: 候选轨迹写作 $\tau _ { + t } ^ { * } \in \check { \mathbb { R } } ^ { N _ { \tau } \times 2 }$；planner 记为 $\bar { \mathcal P }$，occupancy-based cost function 记为 $f _ { o }$。
- **Definition**: 利用 world model 的 future occupancy forecasting 能力进行 end-to-end planning 的规划器，通过 agent、road 与 learned-volume 等 cost factors 评价候选轨迹，并选择 total cost 最小的轨迹。
- **Boundary conditions**: 它不同于 image-based reward function；本文强调利用 geometric 3D features 与 occupancy grids 进行安全约束。
- **Related concepts**: ['Drive-OccWorld', 'Occupancy-based Cost Function', 'BEV Refinement', 'Action Conditions']

## Occupancy-based Cost Function
- **Notation**: 文中 $f _ { o }$ 表示 occupancy-based cost function；在 planning loss 中使用 $f _ { o } ( o , \hat { \tau } )$ 与 $f _ { o } ( o , \tau ^ { * } )$ 比较 expert trajectory 和 candidates。
- **Definition**: 为保证 ego vehicle 安全驾驶而设计的 cost function，由 Agent-Safety Cost、Road-Safety Cost 和 Learned-Volume Cost 组成，总 cost 是这些因素的求和。
- **Boundary conditions**: 它是规划阶段用于候选轨迹评估的 cost，不等同于训练中所有 loss；planning loss 还包含 max-margin、$l _ { 2 }$ imitation 和 collision loss。
- **Related concepts**: ['Occupancy-based Planner', 'Agent-Safety Cost', 'Road-Safety Cost', 'Learned-Volume Cost']

## BEV Refinement
- **Notation**: 使用 $F _ { + t } ^ { b e v }$ 以及 $\mathbf { \bar { \Pi } } _ { { \pmb { F } } _ { { + } t } ^ { b e v } }$ 进行 cross-attention。
- **Definition**: 使用未来 BEV embeddings 的 latent features 进一步细化轨迹的方法，将选出的轨迹编码并与 command embedding 拼接成 ego query，再与 BEV features 做 cross-attention 提取环境细粒度表示，最后由 MLPs 输出 final trajectory。
- **Boundary conditions**: 它发生在规划 refinement 阶段，不是 semantic-conditional normalization；它处理的是轨迹与 BEV features 的交互。
- **Related concepts**: ['Occupancy-based Planner', 'BEV embeddings', 'World Decoder', 'Action Conditions']
