# Related Work

## R1: FSDrive [74]
- **DOI**: 
- **Type**: VLA世界模型相关方法
- **Delta**:
  - What changed: FSDrive通过生成未来图像作为中间推理步骤来进行视觉化思考；VLA-World进一步把世界模型的预测性想象与VLA框架的反思式推理结合，并在多视角、动作条件生成和规划修正中形成统一管线。
  - Why: 该差异直接支撑C1和C2，因为论文把规划与生成优势都归因于对想象未来的显式推理。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['未来图像作为中间推理线索', 'Qwen2-VL相关视觉语言基础模型']

## R2: DriveDreamer [59]
- **DOI**: 
- **Type**: 自动驾驶世界模型
- **Delta**:
  - What changed: DriveDreamer使用diffusion-based framework生成真实驾驶未来视频并预测后续动作；VLA-World保留未来场景模拟思想，但将其接入反思式决策与轨迹优化。
  - Why: 该对比说明VLA-World不是只追求视觉仿真，而是将生成未来用于安全相关规划。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['未来驾驶场景生成评测方向', 'FID生成质量评估']

## R3: OccWorld [78]
- **DOI**: 
- **Type**: 占用世界模型
- **Delta**:
  - What changed: OccWorld利用过去的3D occupancy observations生成未来3D occupancy maps以保持多视角一致性；VLA-World则使用多视角视觉生成预训练和动作条件未来帧来服务反思式推理。
  - Why: 该关系界定了VLA-World相对传统世界模型的重点转移：从纯场景演化建模转向可解释的规划修正。
- **Claims affected**: ['C1']
- **Adopted elements**: ['世界演化建模思想', '多视角一致性问题意识']

## R4: OmniDrive [57]
- **DOI**: 
- **Type**: VLA自动驾驶基线
- **Delta**:
  - What changed: OmniDrive支持3D perception、reasoning和planning；VLA-World在此类VLA能力之上加入短期未来帧生成与对自生成未来的反思。
  - Why: 该对比支撑C1和C3，因为论文将VLA-World的规划与动作预测提升解释为生成未来和反思推理带来的收益。
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['VLA式感知推理规划统一框架', 'nuScenes规划评测协议']

## R5: Qwen2-VL [56]
- **DOI**: 
- **Type**: 视觉语言基础模型
- **Delta**:
  - What changed: 论文以Qwen2-VL-2B初始化VLA-World，并在补充实验中比较Qwen-VL系列不同骨干规模。
  - Why: 该基础模型选择支撑C3和C5，因为动作预测、模型规模消融和规划能力都建立在该系列骨干之上。
- **Claims affected**: ['C3', 'C5']
- **Adopted elements**: ['Qwen-VL family', '多模态视觉语言初始化']
