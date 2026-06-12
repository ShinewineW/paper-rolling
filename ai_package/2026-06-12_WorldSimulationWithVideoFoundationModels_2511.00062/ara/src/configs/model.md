## 模型家族与规模
- **Value**: Cosmos-Predict2.5发布2B和14B scales；Cosmos-Transfer2.5-2B建立在Cosmos-Predict2.5-2B上
- **Rationale**: 2B与14B覆盖不同容量；Transfer版本通过control-net style框架扩展世界翻译和控制能力。
- **Search range**: 2B、14B；Transfer2.5为2B
- **Sensitivity**: 高；人评中14B相对2B的优势更明显，Transfer2.5虽小于Transfer1但质量更高。
- **Source**: Abstract; Sec 5; Sec 6.1

## 统一生成模式
- **Value**: 单个Cosmos-Predict2.5模型支持Text2World、Image2World和Video2World
- **Rationale**: 相比前代，架构简化并把多种生成能力合并到一个模型中。
- **Search range**: 三种模式：Text2World、Image2World、Video2World
- **Sensitivity**: 高；这是论文主张的核心架构变化，影响训练任务设计和条件接口。
- **Source**: Abstract; Sec 3.2

## 主干网络
- **Value**: 复用Cosmos-Predict1 DiT风格的latent diffusion velocity prediction network，并基于flow matching预测velocity
- **Rationale**: FM把去噪网络参数化为预测扩散轨迹速度，作者称其目标更直接并有助于平滑优化和样本质量。
- **Search range**: 论文未给出替代主干范围；与Cosmos-Predict1的EDM式参数化形成对比
- **Sensitivity**: 高；这是从Cosmos-Predict1到Cosmos-Predict2.5的主要方法变化之一。
- **Source**: Sec 3.1; Sec 3.2

## 位置编码
- **Value**: 移除absolute positional embeddings，仅保留relative positional embeddings；Table 3标注Positional Embedding为3D RoPE
- **Rationale**: absolute embeddings限制对训练中未见分辨率或序列长度的泛化；去除后更灵活地处理高分辨率内容和更长视频序列。
- **Search range**: 论文未说明其他位置编码配置
- **Sensitivity**: 高；直接服务于高分辨率和长视频post-training泛化。
- **Source**: Sec 3.2; Tab. 3

## Cosmos-Predict2.5-2B结构
- **Value**: Number of Layers 32；Model Dimension 2,048；FFN Hidden Dimension 8,192；AdaLN-LoRA Dimension 256；Number of Attention Heads 16；Head Dimension 128；MLP Activation GELU；Positional Embedding 3D RoPE
- **Rationale**: Table 3给出2B配置，体现较小规模模型的层数、宽度和注意力头设计。
- **Search range**: 与14B配置形成规模对照
- **Sensitivity**: 中高；容量和宽度影响质量、训练效率和部署成本。
- **Source**: Tab. 3

## Cosmos-Predict2.5-14B结构
- **Value**: Number of Layers 36；Model Dimension 5,120；FFN Hidden Dimension 20,480；AdaLN-LoRA Dimension 256；Number of Attention Heads 40；Head Dimension 128；MLP Activation GELU；Positional Embedding 3D RoPE
- **Rationale**: Table 3给出14B配置，主要通过模型维度、FFN维度和注意力头数扩展容量。
- **Search range**: 与2B配置形成规模对照
- **Sensitivity**: 高；论文人评显示14B相对2B的收益更明显。
- **Source**: Tab. 3; Sec 5

## 视觉tokenizer
- **Value**: 使用WAN2.1 VAE，时间、高度、宽度压缩率为4 × 8 × 8，并进一步使用1 × 2 × 2 patchification
- **Rationale**: 大幅降低计算成本，同时保留关键时空结构。
- **Search range**: 论文未说明其他tokenizer选项
- **Sensitivity**: 高；tokenizer压缩率决定latent序列长度和视频细节保留。
- **Source**: Sec 3.2

## 生成片段长度
- **Value**: 训练模型一次生成93 frames，对应24 latent frames，使用16 fps videos，每段约5.8 seconds
- **Rationale**: 定义主模型训练和生成的基本时间窗口。
- **Search range**: 论文主模型配置为93 pixel frames；部分应用另有203 frames或多视角设置
- **Sensitivity**: 中高；窗口长度影响时间一致性、上下文长度和内存需求。
- **Source**: Sec 3.2

## 文本编码器
- **Value**: 使用Cosmos-Reason1替代Cosmos-Predict1中的T5 encoder；拼接多个blocks的token activations并投影到1024-dimensional space
- **Rationale**: 获得更丰富的文本表示，并通过cross-attention直接引导视频生成。
- **Search range**: 论文未说明拼接哪些blocks或替代投影维度
- **Sensitivity**: 高；作者将其列为Prompt对齐和细粒度控制提升的关键改动。
- **Source**: Sec 3.2

## Image2World和Video2World条件注入
- **Value**: 采用frame-replacement strategy，用conditioned frames一致替换生成序列初始帧
- **Rationale**: 既允许按任务调整条件帧数量，也能增强时间一致性并让输入视觉线索平滑传播到后续帧。
- **Search range**: 条件帧数量可按任务调整；预训练中出现1或5帧，最终阶段也采样0、1、2帧
- **Sensitivity**: 中高；影响条件忠实度和后续帧连贯性。
- **Source**: Sec 3.2; Sec 4.1

## Cosmos-Transfer2.5控制块布局
- **Value**: 相对Cosmos-Transfer1-7B在主分支开始顺序插入四个control blocks，Cosmos-Transfer2.5-2B把四个control blocks更均匀分布为每七个主分支blocks后插入一个
- **Rationale**: 保持控制块数量不变，同时让条件信息更渐进地整合进网络。
- **Search range**: 四个control blocks；每七个blocks插入一个
- **Sensitivity**: 中高；论文把该结构变化与更好的控制输入遵循和质量关联。
- **Source**: Sec 6.1

## Action-conditioned模块
- **Value**: 新增action embedder MLP，把每个action映射为tensor，并加到DiT模块的timestamp embeddings中
- **Rationale**: actions是预训练中不存在的新模态，需要额外条件模块；time embeddings方案在Bridge消融中优于cross-attention和channel concatenation。
- **Search range**: 比较TimeEmbedding、CrossAtten、ChannelConcat三种注入方式
- **Sensitivity**: 高；Tab. 20显示TimeEmbedding方向性能最好。
- **Source**: Sec 6.6; Tab. 20
