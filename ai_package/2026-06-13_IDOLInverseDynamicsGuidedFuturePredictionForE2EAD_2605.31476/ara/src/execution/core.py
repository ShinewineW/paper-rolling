# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

def run(backbone, anchors, ego_state, world_model, idm, cross_attn, mln_idm, mln_cl, decoder, reward_model, obs, U=2, L=2):
    B = backbone(obs)
    outputs = []
    for anchor in anchors:
        e0 = make_query(ego_state, anchor)
        prev_bar = e0
        for ell in range(L):
            e_in = e0 if ell == 0 else mln_cl(e0, prev_bar)
            e = e_in
            bev_seq = [inject(B, e, anchor)]
            for u in range(U):
                x = [e, bev_seq[-1]]
                e, next_bev = world_model(x)
                bev_seq.append(inject(next_bev, e, anchor))
            spatial, global_feat = [], []
            for u in range(U):
                S_u, g_u = idm(bev_seq[u], bev_seq[u + 1])
                spatial.append(S_u)
                global_feat.append(g_u)
            S = mean(spatial)
            g = mean(global_feat)
            e_tilde = norm(e_in + cross_attn(e_in, S, S))
            prev_bar = mln_idm(e_tilde, g)
        traj = decoder(prev_bar, anchor)
        score = reward_model(traj, B)
        outputs.append((score, traj))
    return max(outputs)[1]
