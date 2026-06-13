# Environment
- **Python**: 论文未说明
- **Framework**: PyTorch；论文称FSDP是PyTorch implementation of ZeRO，并使用torch.float32、torch.bfloat16、torch.compile
- **Hardware**: 训练效率处报告8-GPU cluster和8-GPU training setup；真实世界评测使用25 physical robots spanning 3 distinct commercial platforms，平台为AgileX、Agibot G1、Galaxea R1Pro
- **Key dependencies**: Qwen2.5-VL, Qwen3-VL-235B-A22B, LingBot-Depth, Flow Matching, FSDP, FSDP2, FlexAttention, torch.compile, rosbag, GM-100, RoboTwin 2.0, Libero
- **Random seeds**: 论文未说明
