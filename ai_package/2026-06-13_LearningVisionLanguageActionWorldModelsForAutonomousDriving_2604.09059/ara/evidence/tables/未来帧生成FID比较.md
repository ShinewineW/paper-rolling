# 未来帧生成FID比较
- **Source**: Table 2
- **Caption**: "nuScenes上不同生成模型的未来帧生成结果，采用FID评估。"

| Method | DriveGAN [CVPR21 [31]] | DriveDreamer [ECCV24 [59]] | Drive-WM [CVPR24 [61]] | GenAD [CVPR24 [69]] | GEM [CVPR25 [21]] | Doe-1 [arxiv24 [80]] | FSDrive [NeurIPS25 [74]] | VLA-World |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Type Resolution | GAN 256×256 | Diffusion 128×192 | Diffusion 192×384 | Diffusion 256×448 | Diffusion 576×1024 | Autoregressive 384×672 | Autoregressive 128×192 | Autoregressive 128×192 |
| FID↓ | 73.4 | 52.6 | 15.8 | 15.4 | 10.5 | 15.9 | 10.1 | 9.8 |
