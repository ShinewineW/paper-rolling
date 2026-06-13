## 基础模型初始化
- **Value**: Qwen2-VL-2B [56] following FSDrive [74]
- **Rationale**: 主实验以 Qwen2-VL-2B 为 backbone，并沿用 FSDrive 的初始化路线。
- **Search range**: 补充实验还比较 Qwen2.5-VL-3B 和 Qwen2-VL-7B。
- **Sensitivity**: 高；模型规模增大总体提升轨迹规划表现，Qwen2-VL-7B 在表 6 中最好。
- **Source**: Sec 4.1; Table 6; Supp B.3

## 模型家族
- **Value**: Qwen-VL family [56]
- **Rationale**: 实现细节说明 VLA-World 构建在 Qwen-VL family 之上。
- **Search range**: Qwen2-VL-2B、Qwen2.5-VL-3B、Qwen2-VL-7B。
- **Sensitivity**: 高；表 6 显示容量变化影响长期轨迹误差。
- **Source**: Supp B.2; Table 6

## 统一建模形态
- **Value**: single autoregressive transformer
- **Rationale**: 论文将 policy 和 world model 统一到一个 autoregressive transformer 中，使 decision term 与 imagination term 可由同一驾驶 reward 优化。
- **Search range**: 论文将 pure VLA 和 pure World Model 作为特殊情形讨论。
- **Sensitivity**: 高；这是 VLA-World 区别于只做 action 或只做 reconstruction 的核心结构。
- **Source**: Supp A.3

## 输入模态
- **Value**: multi-view visual observations plus ego status and mission goal
- **Rationale**: 输入包含多视角图像、ego-velocity、acceleration、yaw rate、CAN signals，以及 mission goal。
- **Search range**: nuScenes 设置含 six cameras，SFT/RL 还加入 velocity、acceleration、historical trajectories 和 high-level mission commands。
- **Sensitivity**: 高；w/o. Perception 消融显示结构化感知输入对规划有明显贡献。
- **Source**: Sec 3.1; Sec 3.4; Supp B.1; Table 4

## 视觉生成 tokenizer
- **Value**: VQGAN [18, 55] visual tokenizer/codebook
- **Rationale**: 预训练阶段预测 discrete visual tokens，再用 VQGAN visual tokenizer 解码未来图像。
- **Search range**: 论文未报告其他 tokenizer。
- **Sensitivity**: 中；$R _ { \mathrm { v i s } }$ 明确约束 token 长度与 codebook 有效性，移除该 reward 会降低规划表现。
- **Source**: Sec 3.3; Sec 3.5; Table 4

## 最大输入像素数
- **Value**: 524,288
- **Rationale**: 实现中采用 multi-view images 输入并设置最大像素计数。
- **Search range**: 补充实验还比较 input view resolutions 36000 和 52884。
- **Sensitivity**: 中；更高输入分辨率通常在更长时间范围更稳健。
- **Source**: Supp B.2; Table 5; Supp B.3

## 输出结构
- **Value**: <perception>, <prediction>, <visual>, <think>, <action>, <answer>
- **Rationale**: SFT/RL 输出组织为因果推理序列，从场景解析到短期预测、未来视觉 token、反思推理、高层动作与长期轨迹。
- **Search range**: Format Reward 要求这些结构化标签。
- **Sensitivity**: 高；格式 reward 和多步混合训练共同支撑结构化推理。
- **Source**: Sec 3.5; Supp B.1

## 短期预测间隔
- **Value**: 0.5 seconds
- **Rationale**: 模型预测 next waypoint 和 driving direction，并据此生成下一帧未来图像。
- **Search range**: 论文以 next 0.5 seconds / ∆t = 0.5s 作为短期未来示例和实验设置。
- **Sensitivity**: 高；短期预测条件化 visual generation，是后续 reflection 的入口。
- **Source**: Sec 3.2; Sec 3.4; Fig 4; Supp B.1

## 长期轨迹范围
- **Value**: 3s horizon at 0.5 s intervals
- **Rationale**: 最终输出 refined ego-trajectory，以 0.5 s 间隔覆盖 3s horizon。
- **Search range**: 论文主评估报告 1s、2s、3s。
- **Sensitivity**: 高；论文指出长时域上误差积累更明显，VLA-World 的改进在 3-second horizons 更突出。
- **Source**: Sec 3.4; Sec 4.2; Table 1

## 未来帧生成分辨率
- **Value**: Autoregressive 128×192
- **Rationale**: Table 2 中 VLA-World 的生成类型与分辨率。
- **Search range**: 对比方法覆盖 128×192、192×384、256×448、384×672、576×1024。
- **Sensitivity**: 中；VLA-World 在该分辨率下仍优于 FSDrive 和 Doe-1 的 FID。
- **Source**: Table 2

## 模块链路
- **Value**: perception -> short-term prediction -> condition-guided generation -> thinking with visual tokens -> action and trajectory planning
- **Rationale**: SFT 部分逐项定义这些模块，形成 perception-prediction-imagination-reflection-action 闭环。
- **Search range**: 消融移除 perception、generation、reasoning 来验证链路组成。
- **Sensitivity**: 高；perception 和 reasoning 影响大于 visual generation。
- **Source**: Sec 3.4; Sec 4.3; Table 4
