# Environment
- **Python**: 论文未报告
- **Framework**: 基于[19]的code framework；具体Python框架未报告
- **Hardware**: 48 NVIDIA H20 GPUs用于训练；Appendix C在single NVIDIA H20 GPU上分析per-chunk inference cost
- **Key dependencies**: AdamW [62], Wan2.2-TI2V-5B [40], base checkpoint released by [19], Qwen3-VL-8B [9], VAE [40], FlowCache [26], Euler ODE solver, vLLM compilation
- **Random seeds**: 论文未报告
