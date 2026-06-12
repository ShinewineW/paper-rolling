# Problem Specification

## Observations

### O1: 端到端自动驾驶从原始传感器直接规划轨迹，但论文指出这类方法由于缺少预测动态环境的
- **Statement**: 端到端自动驾驶从原始传感器直接规划轨迹，但论文指出这类方法由于缺少预测动态环境的world knowledge，泛化能力和安全鲁棒性存在不足。
- **Evidence**: Introduction中说明端到端模型直接从raw sensor data规划轨迹，同时指出insufficient world knowledge for forecasting dynamic environments会带来generalization ability和safety robustness缺陷。
- **Implication**: 规划器不能只看当前观测，还需要能预演未来环境如何变化。

### O2: 既有world model多偏向数据生成或预训练范式，尚未充分服务于端到端规划的
- **Statement**: 既有world model多偏向数据生成或预训练范式，尚未充分服务于端到端规划的安全与鲁棒性。
- **Evidence**: Introduction和End-to-End Planning部分均指出多数world model关注data generation或pretraining paradigms，并忽略enhancement of safety and robustness for end-to-end planning。
- **Implication**: 需要把未来预测能力转化为规划时可用的几何与安全约束。

### O3: 未来驾驶状态会随自车动作变化，因此同一历史观测下应能生成由动作条件控制的不同未来
- **Statement**: 未来驾驶状态会随自车动作变化，因此同一历史观测下应能生成由动作条件控制的不同未来occupancy。
- **Evidence**: Action-Controllable Generation部分说明ego vehicle的motion states对理解交互至关重要，并提出用diverse action conditions赋予controllable generation能力。
- **Implication**: 动作条件是把世界模型从被动预测器变成可用于决策评估的关键接口。

## Gaps

### G1: 图像或视频式world model难以直接利用环境的geometric 3D f
- **Statement**: 图像或视频式world model难以直接利用环境的geometric 3D features做安全规划。
- **Caused by**: 未来状态表达没有直接暴露可采样、可碰撞检查的occupancy grids。
- **Existing attempts**: ['Drive-WM使用generated driving videos和image-based reward function规划轨迹', 'ST-P3使用occupancy representation作为安全规划的cost factor']
- **Why they fail**: 图像奖励或视频生成更偏外观层面，论文指出geometric 3D features of the environment are not fully exploited for motion planning。

### G2: 只用历史观测预测future occupancy会缺少对自车动作反事实的建模。
- **Statement**: 只用历史观测预测future occupancy会缺少对自车动作反事实的建模。
- **Caused by**: 既有occupancy forecasting方法主要从历史与当前观测外推未来状态。
- **Existing attempts**: ['Cam4DOcc建立camera-based occupancy forecasting benchmark', 'Drive-OccWorld用统一接口注入diverse action conditions']
- **Why they fail**: 若未来预测不随velocity、steering angle、trajectory或commands变化，规划候选轨迹就难以和对应未来状态绑定。

### G3: 原始BEV embeddings来自图像特征，语义判别性不足且跨时间运动会造成对
- **Statement**: 原始BEV embeddings来自图像特征，语义判别性不足且跨时间运动会造成对齐和动态建模困难。
- **Caused by**: 图像到BEV的特征投影与多时间步动态变化会混合语义与运动误差。
- **Existing attempts**: ['semantic-conditional normalization强调高语义概率的BEV响应', 'motion-conditional normalization用ego-pose transformation和3D backward centripetal flow补偿运动']
- **Why they fail**: Supplementary中说明原始BEV embeddings呈ray-shaped patterns，且Method中强调需要同时处理ego vehicle和other agents的运动。

## Key Insight
- **Insight**: 把未来occupancy和flow作为世界模型的状态表示，再让规划器在这些预测状态上评估候选轨迹，可以把生成式未来预演转化为可解释的安全约束。
- **Derived from**: 论文将world model W的future occupancy and flow forecasting与planner P的occupancy-based cost function组合，并采用连续rollout让预测轨迹作为后续动作条件。
- **Enables**: 同时支持action-controllable generation、4D occupancy forecasting和end-to-end planning。

## Assumptions
- 未来occupancy与flow能提供足够细粒度的agent和background状态供规划使用。
- 动作条件能够反映ego vehicle与环境的交互，从而影响未来状态预测。
- 由语义与运动标签调制BEV记忆能提升历史特征对未来预测和规划的可用性。
