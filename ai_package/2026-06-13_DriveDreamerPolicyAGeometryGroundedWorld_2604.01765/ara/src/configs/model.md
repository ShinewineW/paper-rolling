## 总体架构
- **Value**: LLM + depth generator + video generator + action generator，通过固定大小 query bottleneck 连接
- **Rationale**: LLM 负责 multimodal understanding，专家负责 depth、video、action 的模态专用生成。
- **Search range**: 论文未报告替代总架构范围。
- **Sensitivity**: 高；这是统一 world-action modeling 的核心设计。
- **Source**: Sec 3.2 DriveDreamer-Policy

## LLM 初始化
- **Value**: Qwen3-VL-2B
- **Rationale**: 用于处理和理解 multimodal inputs。
- **Search range**: 论文未报告其他 LLM。
- **Sensitivity**: 高；LLM 能力决定 instruction、multi-view image 与 action context 的融合质量。
- **Source**: Sec 3.3 Model Initialization and Adaptation

## 输入流
- **Value**: language instruction、synchronized multi-view RGB observations、current action context
- **Rationale**: 三类输入共同支持 world modeling 和 planning。
- **Search range**: 论文未报告移除输入流的系统性范围。
- **Sensitivity**: 高；去掉动作或视觉上下文会削弱生成和规划条件。
- **Source**: Sec 3.2.1 Input Processing

## query 顺序与掩码
- **Value**: depth queries → video queries → action queries；video queries 可使用 depth context，action queries 可使用 depth 和 video context
- **Rationale**: 形成单次前向的信息流，让几何先于视频，再进入动作。
- **Search range**: 论文未报告其他 attention ordering。
- **Sensitivity**: 高；Table 4 和 Table 5 的消融支持 depth 与 video 对 planning 和 video generation 的互补作用。
- **Source**: Sec 3.2.1 Embeddings Generation

## 默认 query 配置
- **Value**: 64 depth-query tokens、64 video-query tokens、8 action-query tokens
- **Rationale**: 论文默认实验配置，提供固定容量的几何、外观和动作上下文槽位。
- **Search range**: 论文比较了更小预算 32 depth + 32 video + 4 action query tokens。
- **Sensitivity**: 高；query budget 消融显示更大 query 数通常提升 planning 与 world-generation。
- **Source**: Sec 4.1 Implementation Details；Sec 4.3 Ablations on Number of Queries

## depth generator
- **Value**: pixel-space diffusion transformer，使用 standard flow-matching objective，并通过 cross-attention 条件化于 LLM world depth embeddings
- **Rationale**: 直接在像素空间生成 monocular depth，保留边界细节并作为 3D scaffold。
- **Search range**: 论文未报告非 pixel-space depth generator 替代。
- **Sensitivity**: 高；深度生成是 geometry-grounded imagination 和 planning 的核心。
- **Source**: Sec 3.2.2 Depth Generator

## depth generator 初始化
- **Value**: PPD
- **Rationale**: depth generator 从 PPD 初始化。
- **Search range**: 论文比较了 zero-shot PPD、fine-tune PPD 和 DriveDreamer-Policy 的深度结果。
- **Sensitivity**: 中；初始化影响 depth generator 的几何先验。
- **Source**: Sec 3.3 Model Initialization and Adaptation；Sec 4.2 World Performance Comparison

## video generator
- **Value**: text-image-to-video diffusion transformer；使用 VAE 编码当前 RGB images，并以 noisy video latents 初始化目标 horizon
- **Rationale**: 在 latent-space 生成未来视频，同时由 LLM world video embeddings 和视觉条件引导。
- **Search range**: 论文未报告其他视频生成器架构。
- **Sensitivity**: 高；视频分支提供未来动态与外观想象。
- **Source**: Sec 3.2.2 Video Generator

## video generator 初始化
- **Value**: Wan-2.1-T2V-1.3B，并适配到 image-to-video task
- **Rationale**: 利用已有 text-to-video backbone，再改造为图像到视频任务。
- **Search range**: 论文未报告其他初始化模型。
- **Sensitivity**: 中；初始化模型影响视频生成质量和训练成本。
- **Source**: Sec 3.3 Model Initialization and Adaptation

## 视频视觉条件
- **Value**: CLIP 从当前图像帧提取 lightweight visual condition，并与 world video embeddings 拼接后注入 denoiser
- **Rationale**: 保持 appearance、identity 和 camera content。
- **Search range**: 论文未报告无 CLIP 条件的结果。
- **Sensitivity**: 中；视觉条件缺失可能降低当前场景一致性。
- **Source**: Sec 3.2.2 Video Generator

## action generator
- **Value**: standalone diffusion transformer，将 noise trajectory 映射为 feasible future action sequence，并通过 cross-attention 条件化于 action embedding
- **Rationale**: 动作头保持轻量，同时吸收 instruction、multi-view observations、geometry 与 imagination cues。
- **Search range**: 论文未报告其他 action generator 架构。
- **Sensitivity**: 高；这是 planning 输出的直接模块。
- **Source**: Sec 3.2.2 Action Generator

## action encoder
- **Value**: 2-layer MLP with layer normalization
- **Rationale**: 将 action context 编码为 action tokens 输入 LLM。
- **Search range**: 论文未报告其他 action encoder。
- **Sensitivity**: 中；编码器容量影响动作上下文的表达。
- **Source**: Sec 4.1 Implementation Details

## 轨迹状态表示
- **Value**: $( x , y ,$ cos ??, sin ??)
- **Rationale**: 避免角度 wrap-around，并鼓励平滑转向动态。
- **Search range**: 论文未报告其他状态表示。
- **Sensitivity**: 中；轨迹参数化会影响 heading 学习稳定性。
- **Source**: Sec 3.2.2 Action Generator
