---
name: eval-cluster-gvisor-quirks
description: Sandbox and verifier quirks of the Harbor/Modal eval cluster that break otherwise-correct benchmark tests
metadata:
  node_type: memory
  type: project
  originSessionId: 04a467b9-aa60-48e8-8faf-a5d770be900e
  modified: 2026-10-24T19:25:37.976Z
---

The eval cluster (`/app/eval/run_release_eval.sh`: Harbor 0.23, `-e modal`, gVisor-style sandboxes)
has quirks that silently break benchmark tests:

- **valgrind cannot start.** It dies in the client's dynamic loader before `main`, because faults on
  unmapped pages are reported as `SEGV_ACCERR` instead of `SEGV_MAPERR`. Any test that greps
  valgrind output needs a fallback.
- **`ulimit -c unlimited` is EPERM**, so `set -e` scripts that enable core dumps abort there.
- **`tests/test.sh` runs under a non-login shell**, so `~/.bashrc` PATH edits are not picked up.
- **pytest usually runs via `uvx`,** whose venv cannot see packages the agent pip-installed. Run the
  agent's own programs with the image's Python (export it from `test.sh` before the `uvx` call).
- **Old distro images cannot apt-install.** `debian:bullseye` pools are archived, and pinned
  `pkg=version` installs 404 once a pool rotates; prefer unpinned installs plus `apt-get update`.

**Why:** each of these produced reward 0 for a correct solution or a reference run, not a real
failure.

**How to apply:** when a task fails on the cluster but looks right, check these before debugging the
task itself. See [[terminal-suite-release-gate]].
