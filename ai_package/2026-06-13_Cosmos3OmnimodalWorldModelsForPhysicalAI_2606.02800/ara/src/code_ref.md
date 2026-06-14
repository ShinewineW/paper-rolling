# Code Reference

**Author-declared open-source.** The paper releases code, model checkpoints, curated synthetic datasets, and the evaluation benchmark under the Linux Foundation's OpenMDW-1.1 License.

- **Repository**: https://github.com/nvidia/cosmos (also `github.com/nvidia/cosmos-framework`)
- **Pinned commit**: not stated in the paper; resolve against the live repository HEAD.
- **Source**: paper abstract + intro (author-declared release)
- **Reproduce**: clone the repository; the paper gives no pinned SHA, so use the latest published tag/commit. This workspace keeps no runnable copy.
- **Model checkpoints**: https://huggingface.co/collections/nvidia/cosmos3 — `Cosmos3-Nano` and `Cosmos3-Super` released; `Cosmos3-Edge` deferred to a later release.
- **Innovation → code location**: not mechanically resolved (the paper gives no file/line references); map modules (dual-stream joint attention, clean-prefix/noisy-target token arrangement, domain-aware action projection) against the actual repo layout when reproducing.
