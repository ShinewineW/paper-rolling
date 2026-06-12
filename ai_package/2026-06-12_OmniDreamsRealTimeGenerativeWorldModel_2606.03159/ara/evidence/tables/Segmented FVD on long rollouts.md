# Segmented FVD on long rollouts
- **Source**: Table 6
- **Caption**: "长 rollout 分段 FVD；每个 rollout 被拆为四个时间窗口并与同一 real-video front-wide reference distribution 比较。"

| Training teacher | 0-5s↓ | 5-10s↓ | 10-15s← | 15-20s↓ | Mean↓ | △↓ |
| --- | --- | --- | --- | --- | --- | --- |
| Short-context teacher | 109.3 | 183.0 | 258.3 | 409.2 | 240.0 | 299.9 |
| Progressive long-context teacher | 95.5 | 151.0 | 202.5 | 268.4 | 179.4 | 172.9 |
