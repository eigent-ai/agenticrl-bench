---
name: offline-dev-box-testing
description: "Quirks of the offline 2xH100 dev box when running Miles tests and dev runs (network-less HF hub, baseline failures, Ray log dedup)"
metadata:
  node_type: memory
  type: reference
  originSessionId: a2a72cd3-7920-4095-aca4-96407d24d055
  modified: 2026-10-25T05:02:10.778Z
---

- No network: tests that load `Qwen/Qwen3-0.6B` from the HF hub or clone the GitHub artifacts repo (loss snapshots) fail. Run pytest with `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` so they fail fast instead of retrying for many minutes. Baseline for `tests/fast/{rollout,ray/rollout,backends/training_utils,router,doc}` + test_arguments/test_megatron_cli_flags on the pristine checkout: ~104 failed + 340 errors, all environmental — compare failure sets, not counts.
- Loss snapshots can still be checked offline: `--snapshot` on the pristine checkout, copy `loss_snapshots/*.pt`, `--compare` on the changed one, then delete the copies.
- `pytest-timeout` is not installed (`--timeout` is an unrecognized argument); ruff/pyflakes are absent, black (119 cols) and isort are present.
- Megatron arg parsing needs `CUDA_DEVICE_MAX_CONNECTIONS=1` and `PYTHONPATH=/root/Megatron-LM:/app/miles`.
- `/app/launch/dev_2gpu.sh` saves rollouts to `$HOME/sc-dev/rollouts/<recipe>_<step>.pt` (overwritten by each split run; pass a later `--save-debug-rollout-data` to redirect). Ray de-duplicates near-identical log lines across ranks ("repeated 2x across cluster").
- SGLang's post-warmup `freeze_gc` self-call fails with connection refused in this container; it is caught and harmless.

Related: [[score-centering-sql-agent]]
