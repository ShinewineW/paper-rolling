# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/Minecraft 世界模型比较.md](tables/Minecraft 世界模型比较.md) | Table 1 | ['C2'] | Minecraft 世界模型比较。Dreamer 4 被报告为能准确模拟多种物体交互和游戏机制，并在保持实时交互推理的同时扩展上下文长度。 |
| [tables/模型设计选择级联.md](tables/模型设计选择级联.md) | Table 2 | ['C4'] | 模型设计选择级联。论文从朴素 diffusion forcing transformer 出发，逐步加入 objective 与 architecture 修改，并报告推理速度和 FVD。 |
| [tables/Minecraft 智能体实验设置比较.md](tables/Minecraft 智能体实验设置比较.md) | Table 3 | ['C5'] | 不同 Minecraft 智能体实验设置比较。Dreamer 4 被定位为纯离线经验学习，并使用高分辨率图像输入和低层键鼠动作。 |
| [tables/离线钻石挑战成功率.md](tables/离线钻石挑战成功率.md) | Table 7 | ['C1'] | 每个 milestone item 的成功率，按 1000 evaluation episodes 平均。 |
| [tables/离线钻石挑战到达时间.md](tables/离线钻石挑战到达时间.md) | Table 8 | ['C1'] | 成功 episode 中到达每个 milestone item 所需分钟数；低成功率项目的时间被省略以保证统计显著性。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/629a02d1a4a94fd7a89661a53d3ce53609191901d81595d1e8a7656616643f34.jpg` | result | Figure 1: Dreamer 4 learns to solve complex control tasks by reinforcement learning inside of its world model. We decode the imagined training sequences for visualization, showing that the world model has learned to simulate a wide range of game mechanics from low-level mouse and keyboard actions, i |
| `images/b3f82cc8f902ae4283ee0f39b6a8a0423366e30c2d84ffc1f96c4b485ad54480.jpg` | architecture | Figure 2: World model design. Dreamer 4 consists of a causal tokenizer and an interactive dynamics model, which both use the same block-causal transformer architecture. The tokenizer encodes partially masked image patches and latent tokens, squeezes the latents through a low-dimensional projection w |
| `images/1cb8da582057dc95af48f6dbd2b2eb26f0f497f791becb46d122c9de1d436fb8.jpg` | architecture | Figure 2: World model design. Dreamer 4 consists of a causal tokenizer and an interactive dynamics model, which both use the same block-causal transformer architecture. The tokenizer encodes partially masked image patches and latent tokens, squeezes the latents through a low-dimensional projection w |
| `images/a5c19b1d0b723d3bf9a370156d52e6e63d709452ad2bc5c546872ec964748d86.jpg` | result | Figure 3: Agent performance in Minecraft without environment interaction. All methods have access to the same contractor dataset15 with image inputs and low-level mouse and keyboard actions. We report the success rates of important items obtained during 60-minute episodes that start in random worlds |
| `images/6f1ecaf43f6b1d89cb8584c1c517791e1d47f7923e38cd237d885ed641a91d6c.jpg` | result | Figure 4: Agent ablations on the offline diamond challenge. We report success rates and time needed to reach an item for four milestone items. Dreamer 4 outperforms methods based on behavioral cloning in both metrics, demonstrating that imagination training improves both the robustness and efficienc |
| `images/250d38530749fc5596d9b3226d12c94696160038575727fa859392e346e9a8bd.jpg` | result | Figure 5: Human interaction. A human player counterfactually interacts with the world model in real time via mouse and keyboard to perform the same task from the same initial image. Dreamer 4 is the first world model to accurately predict the object interactions and game mechanics of placing the blo |
| `images/b4f5dddcb1b0ace2e9d3c32d736105ad7425b8f5efebb6ed65e4614eeb62a293.jpg` | result | Figure 6: Robotics generations for counterfactual actions. Dreamer 4 learns an accurate real-time simulator of the environment, allowing human operators to control the imagined robot to pick up objects, flip over a bowl, press a ball onto a plate, move a towel, and throw a bowl. |
| `images/e62705ea4994b4a69523e18aa22a57df0d855c59f63329b566b6599659590cdf.jpg` | result | Action data (hours) |
| `images/3b18d75b641354d669968ae1032e8efc259868a5acec8fd4d3791a141c31f29d.jpg` | result | Figure 7: Action generalization. (left) Dreamer 4 learns accurate action conditioning from 2500 hours of video with only 100 hours of paired actions. It achieves over 80% of the action-conditioned generation accuracy, normalized within the range of training without any actions and using all actions. |
| `images/e0c2b497fab471d2a627a86e1bb710de0cffb8532fc583f6e00c3a4a8fdaa4f3.jpg` | result | Figure 7: Action generalization. (left) Dreamer 4 learns accurate action conditioning from 2500 hours of video with only 100 hours of paired actions. It achieves over 80% of the action-conditioned generation accuracy, normalized within the range of training without any actions and using all actions. |
| `images/4ce954e41498a5104f52b42de8190683601f0950624119dbf5d3b2e93d4c6f54.jpg` | result | Figure 7: Action generalization. (left) Dreamer 4 learns accurate action conditioning from 2500 hours of video with only 100 hours of paired actions. It achieves over 80% of the action-conditioned generation accuracy, normalized within the range of training without any actions and using all actions. |
| `images/4ccb07180b4c2989bad6a4ce988e7eb7703e97a6a456e00c24b918f12183f0d2.jpg` | result | Figure 8: Generation quality of shortcut forcing compared to diffusion forcing. Shortcut forcing with only 4 sampling steps approaches the quality of diffusion forcing with 64 steps, resulting in 16× faster generations. |
| `images/e72848994c37f22c8a8862611c86f7ed3a31ed4e06c99ad1c91e44c8a36d4ebc.jpg` | result | Figure 9: Kitchen video generations starting from holdout context. |
| `images/fb8c4df04ce90f238296ea547121730620ac8ba67f4667e0c551fff93dd74d5c.jpg` | result | Figure 10: Comparison of input images for different agents. Dreamer 4 learns directly from highresolution images reflecting the experience of human players. |
| `images/0ef261af672eeee1d1b42f194db54f3822c42a46ad993a88d418e6d0f2dabd63.jpg` | result | Figure 10: Comparison of input images for different agents. Dreamer 4 learns directly from highresolution images reflecting the experience of human players. |
| `images/7e06e2f07f9d789a3e87d3df9bba085de32fa728a5c03d27b87d7d8112cb39a4.jpg` | result | Figure 10: Comparison of input images for different agents. Dreamer 4 learns directly from highresolution images reflecting the experience of human players. |
| `images/acc941d7a3735e8cbe022081bd06e3e76b1fde0f11bf17a222ca54d5077c4cac.jpg` | result | Figure 11: Comparison of multi-step video generations between Dreamer 3 and Dreamer 4. |
| `images/17dee9ac1280b63a3b1f36dfecb41604952df3adf2437da1fec436ba611578e3.jpg` | result | Figure 12: Lucid-v1 |
| `images/edc0b527e313861b2bb4e22557a244f8452f088e1b4a3838fa0696dd4fd37b06.jpg` | result | Figure 13: Oasis (large) |
| `images/5f9f0bb89b05161d869bfd8f84adba8c004f76b02f417b0b4608bf3e1f5b9f98.jpg` | result | Figure 14: Dreamer 4 |
