# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import random

class DiffusionWorldModel:
    def train_step(self, batch):
        sigma = sample_lognormal(p_mean=-0.4, p_std=1.2)
        x_hist, a_hist, x_next = batch
        x_noisy = add_gaussian_noise(x_next, sigma)
        x_hat = self.denoise(x_noisy, sigma, x_hist, a_hist)
        return mse(x_hat, x_next)

    def sample_next(self, x_hist, a_hist, steps=3):
        x = sample_prior_like(x_hist[-1])
        for tau in reversed(make_schedule(steps)):
            x = euler_reverse_step(self.denoise, x, tau, x_hist, a_hist)
        return x

class RewardEndModel:
    def train_step(self, seq):
        return reward_end_cross_entropy(seq)

class ActorCritic:
    def act(self, obs):
        return sample_policy(obs)

    def train_on_imagination(self, traj):
        returns = lambda_returns(traj)
        return reinforce_loss(traj, returns) + value_loss(traj, returns)

def training_loop(env, epochs=1000, collect_steps=100, horizon=15):
    replay = []
    world = DiffusionWorldModel()
    reward_end = RewardEndModel()
    agent = ActorCritic()
    for _ in range(epochs):
        obs = env.reset()
        for _ in range(collect_steps):
            action = agent.act(obs)
            next_obs, reward, done = env.step(action)
            replay.append((obs, action, reward, done))
            obs = env.reset() if done else next_obs
        for _ in range(400):
            world.train_step(sample_world_batch(replay))
            reward_end.train_step(sample_reward_batch(replay))
            x_hist, a_hist = sample_context(replay)
            traj = []
            for _ in range(horizon):
                action = agent.act(x_hist[-1])
                reward, done = predict_reward_done(reward_end, x_hist, a_hist + [action])
                next_obs = world.sample_next(x_hist, a_hist + [action], steps=3)
                traj.append((x_hist[-1], action, reward, done, next_obs))
                x_hist = (x_hist + [next_obs])[-4:]
                a_hist = (a_hist + [action])[-4:]
            agent.train_on_imagination(traj)
