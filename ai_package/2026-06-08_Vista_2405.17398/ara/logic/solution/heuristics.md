# Heuristics

## H1: 最终损失权重: λ1=1.0(动态增强损失), λ2=0.1(结构保留损失)
- **Rationale**: λ1 较大以充分强化对高运动区域的自适应监督; λ2 较小防止高频监督过度干扰感知质量与运动强度之间的平衡
- **Sensitivity**: λ2 对结构细节与运动质量权衡较敏感; 论文未系统报告灵敏度曲线
- **Bounds**: λ1=1.0, λ2=0.1
- **Code ref**: [Eq.6, Appendix C.3]
- **Source**: Appendix C.3

## H2: 动态先验采样概率按条件帧数量递增: 0/1/2/3 帧分别对应 1/15、2/15、4/15、8/15
- **Rationale**: 递增分布使模型更多接触充分先验场景, 有利于学习一致的长时序动态; 少量零先验样本保留以维持基础生成能力
- **Sensitivity**: 直接影响自回归长时序一致性; 3帧概率过低则长时序出现运动不一致退化
- **Bounds**: 各档概率之和为1; 最多3帧条件
- **Code ref**: [Appendix C.3]
- **Source**: Appendix C.3

## H3: LoRA 秩 rank=16
- **Rationale**: 低秩适配器使冻结 UNet 获得可学习适配能力, 训练后可无损合并到原始权重推理无额外延迟; 不加 LoRA 直接训练投影层会产生视觉损坏(Fig.16)
- **Sensitivity**: 秩过小导致动作可控性不足; 论文未报告不同秩的系统对比
- **Bounds**: rank=16
- **Code ref**: [Appendix C.3, D.5]
- **Source**: Appendix C.3

## H4: 动作独立性约束: 每个训练样本仅激活单一动作模式, 其余填零作为无条件输入; 激活动作以 15% 概率 dropout 以支持无分类器引导
- **Rationale**: 真实开放场景中无法同时获取所有异构动作格式; 此约束避免将训练预算浪费在无实际意义的动作组合上, 在相同步数内最大化各动作模式的学习效率
- **Sensitivity**: 去除此约束导致各子集 FVD 上升(Table 5 对比验证)
- **Bounds**: 每样本仅一种动作激活; dropout ratio=15%
- **Code ref**: [Sec.3.2, Appendix D.3]
- **Source**: Sec.3.2

## H5: 三角形 CFG 引导参数: s_min=1.0, s_max=2.5
- **Rationale**: 线性或固定高引导在自回归长时序中导致色彩饱和漂移; 三角形方案对将用作下一轮条件的中间帧施以适中引导, 其质量通过时序交互传播到低引导帧
- **Sensitivity**: s_max 过高产生饱和漂移; s_min=1.0 确保末帧质量可传递(Fig.15 对比验证)
- **Bounds**: s_min=1.0, s_max=2.5
- **Code ref**: [Appendix C.4, Eq.9]
- **Source**: Appendix C.4

## H6: 奖励估计集成大小 M=5, 每样本去噪步数=10
- **Rationale**: 10 步去噪(完整 50 步的 20%)即可提供足够区分度; 增加去噪步数对奖励对比度提升比增大集成规模更显著(Appendix D.1); M=5 计算量不超过一次完整生成
- **Sensitivity**: 去噪步数对奖励区分度影响大于集成大小; 5步(Fig.14)仍产生可接受估计
- **Bounds**: M=5, 步数=10 (默认); 可降低以换取效率
- **Code ref**: [Appendix C.6, D.1]
- **Source**: Appendix C.6

## H7: 第二阶段两步式分辨率课程: 先以 320×576 低分辨率训练 120K 步, 再以 576×1024 高分辨率微调 10K 步
- **Rationale**: 低分辨率吞吐量提升 3.5×, 可在相同计算预算下完成更多迭代以学习动作可控性语义; 若直接在高分辨率调整则预训练高保真度降级
- **Sensitivity**: 若跳过低分辨率阶段动作可控性弱; 若不做高分辨率微调则低分辨率习得的控制能力无法对齐目标分辨率
- **Bounds**: 低分辨率 120K 步, 高分辨率 10K 步
- **Code ref**: [Sec.3.2, Appendix C.3]
- **Source**: Sec.3.2, Appendix C.3

## H8: Offset noise 强度 0.02
- **Rationale**: 有助于改善视频时间平滑度(Appendix C.3 明确说明)
- **Sensitivity**: 论文未报告灵敏度
- **Bounds**: strength=0.02
- **Code ref**: [Appendix C.3]
- **Source**: Appendix C.3
