# Code Reference

- **Repository**: https://github.com/ucaszyp/World4Drive
- **Pinned commit**: `cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`
- **Source**: paper-text (verified)
- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.

## Innovation → code location

| Innovation | Location (`file:line`) |
|---|---|
| intention-aware latent world model 用 latent world model 生成、评估并选择 multi-modal trajectories | README.md:2 |
| Driving World Encoding 结合 intention encoder 与 physical latent encoder | _not found_ |
| open-vocabulary semantic supervision 通过 Grounded-SAM 生成 pseudo semantic labels | _not found_ |
| scale-aware depth forward projection 形成 3D position maps | _not found_ |
| World Model Selector 用 latent distance 选择训练 modality 并训练 ScoreNet | custom_mmdet3d/ops/paconv/paconv.py:12 |
