# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

from dataclasses import dataclass

@dataclass
class WorldState:
    h: object
    z: object | None = None

class WorldModel:
    def infer(self, h_prev, obs):
        return {'belief_from': obs, 'history': h_prev}

    def policy(self, z, h):
        return 'act'

    def value(self, z, h):
        return 0.0

    def transition(self, z, action):
        return {'next_from': z, 'action': action}

    def observe(self, z):
        return {'observation_from': z}

    def outcome(self, z, action):
        return {'reward': 0.0, 'gamma': 1.0}

    def update_memory(self, h_prev, z, action_prev):
        return {'prev': h_prev, 'z': z, 'last_action': action_prev}

def rollout(model, observations, h0=None):
    state = WorldState(h=h0)
    last_action = None
    trace = []
    for obs in observations:
        state.z = model.infer(state.h, obs)
        state.h = model.update_memory(state.h, state.z, last_action)
        action = model.policy(state.z, state.h)
        value = model.value(state.z, state.h)
        next_z = model.transition(state.z, action)
        next_obs = model.observe(next_z)
        outcome = model.outcome(state.z, action)
        trace.append({'z': state.z, 'h': state.h, 'action': action, 'value': value, 'next_obs': next_obs, 'outcome': outcome})
        last_action = action
    return trace

if __name__ == '__main__':
    wm = WorldModel()
    print(rollout(wm, ['first observation', 'second observation']))
