# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

from dataclasses import dataclass

@dataclass
class Session:
    kv_cache: object
    first_frame_latent: object
    cuda_graph: object | None = None

def closed_loop_rollout(policy, traffic, sim, renderer, model, decoder, prompt, first_frame, steps):
    session = Session(kv_cache=model.allocate_kv_cache(), first_frame_latent=model.encode_first_frame(first_frame))
    sim.reset(first_frame=first_frame)
    frames = []
    for chunk_idx in range(steps):
        # pre-fetch：在 chunk 边界先承诺 ego 和 actor 的多步轨迹
        observation = sim.latest_observation()
        ego_traj = policy.plan(observation, horizon=model.chunk_duration)
        actor_traj = traffic.plan(sim.state, horizon=model.chunk_duration)
        sim.commit_trajectories(ego_traj, actor_traj)

        world_video = renderer.render_world_scenario(sim.map, ego_traj, actor_traj, model.camera_rig)
        control_tokens = model.control_mlp(world_video)
        text_tokens = model.text_encoder(prompt)
        noisy_latents = model.sample_initial_latents(chunk_size=model.chunk_size)

        latent_chunk, new_kv = model.denoise_chunk(
            noisy_latents=noisy_latents,
            text_tokens=text_tokens,
            control_tokens=control_tokens,
            first_frame_latent=session.first_frame_latent if chunk_idx == 0 else None,
            kv_cache=session.kv_cache,
            causal=True,
            local_window=True,
        )
        rgb_chunk = decoder.decode(latent_chunk)
        session.kv_cache = model.update_kv_cache_async(session.kv_cache, new_kv)
        sim.inject_frames(rgb_chunk)
        frames.extend(rgb_chunk)
    return frames
