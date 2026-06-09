# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch

def build_condition(img_emb, layout_emb, text_emb, action_emb):
    # c_t = [i_0, l_0, e_0, a_t] (Eq.5)
    return torch.cat([img_emb, layout_emb, text_emb, action_emb], dim=1)

def generate_multiview_video(joint_model, factorized_model, obs, actions):
    prev_frames = obs['frames']  # 初始上下文帧
    generated = []
    for action in actions:
        c_t = build_condition(obs['img_emb'], obs['layout_emb'], obs['text_emb'], action)
        # 第一步: 联合模型生成参考视图 {F, BL, BR}
        ref_views = joint_model.ddim_sample(c_t, prev_frames, steps=50, cfg=5.0)
        # 第二步: 因式分解模型以参考视图为条件生成缝合视图 {FL, B, FR}
        stitched = factorized_model.ddim_sample(c_t, ref_views, prev_frames, steps=50, cfg=5.0)
        frame = merge_views(ref_views, stitched)
        generated.append(frame)
        prev_frames = frame  # 作为下一帧上下文
    return generated

# 树状规划主循环
for timestep in range(planning_horizon):
    obs = get_current_obs()
    candidates = vad_planner.sample_trajectories(obs, commands=['straight', 'left', 'right'])
    best_traj, best_reward = None, float('-inf')
    for traj in candidates:
        future_video = generate_multiview_video(joint_model, factorized_model, obs, traj.actions)
        map_r = map_predictor.reward(future_video)   # 离路缘距离 + 中心线一致性
        obj_r = detector.reward(future_video)        # 与道路用户的距离
        reward = map_r * obj_r
        if reward > best_reward:
            best_reward, best_traj = reward, traj
    execute_action(best_traj.actions[0])
