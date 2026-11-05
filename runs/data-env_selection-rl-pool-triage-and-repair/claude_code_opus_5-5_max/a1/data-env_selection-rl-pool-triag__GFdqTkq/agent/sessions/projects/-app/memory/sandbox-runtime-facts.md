---
name: sandbox-runtime-facts
description: Verified quirks of the training sandboxes (Modal/gVisor via sandbox_broker) that silently break task rewards
metadata:
  node_type: memory
  type: reference
  originSessionId: 7bdf0c96-622d-4ad3-bede-0e8e9ce48a16
  modified: 2026-10-24T22:44:16.936Z
---

Verified 2026-10-24 on the terminal-RL box (sandbox CLI `sandbox`, harbor `-e sandbox_broker.harbor_env:BrokerEnvironment`):

- Broker only builds `environment/` dirs whose content hash is in /etc/sandbox-broker/build-contexts.txt; an edited Dockerfile can't be run on the box (validate such tasks by pairing new tests/solution with the original environment/).
- Modal + gVisor: root, hostname `modal`, 1 CPU / 2 GB, no network (DNS fails), loopback TCP works, only `lo`.
- Capability bounding set a80c05fb: no cap_net_raw/cap_net_admin/cap_sys_admin even for root → no packet capture, no mount; a binary with file caps in +e can't be exec'd by non-root.
- PID 1 is dumb-init running the image ENTRYPOINT with CMD replaced by `sleep infinity`; no systemd.
- Platform injects PYTHONPATH=/pkg/:/root/ — a .py left in /root shadows the verifier's pytest imports unless test.sh uses `env -u PYTHONPATH uvx`.
- Docker RUN uses dash: `printf '\x..'` is NOT interpreted (use octal `\NNN`).
- Terminus-2 runs in tmux on the default socket: agent `tmux kill-*`, `rm -rf /tmp/*`, `exit`/`exec` → harness RuntimeError.

Related: [[terminal-rl-pool]]
