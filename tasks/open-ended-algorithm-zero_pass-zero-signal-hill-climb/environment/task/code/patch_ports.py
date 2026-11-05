"""Static ports below the sandbox's ephemeral range (gVisor: 16000-65535), applied to the image's Miles checkout.
Miles picks SGLang's http / nccl / dist-init ports from 20000 upward and Megatron's master port from 20000-21000,
checks them free and binds later; a client socket can take one in between (EADDRINUSE, dead engine). Idempotent."""
import pathlib
for f, old, new in (("/root/miles/miles/utils/workers/addr_allocator.py", "_DYNAMIC_PORT_START = 20000",
                     "_DYNAMIC_PORT_START = 9100   # OE-T1: below the sandbox's ephemeral range (16000-65535)"),
                    ("/root/miles/miles/ray/train_actor.py", "get_free_port(start_port=random.randint(20000, 21000))",
                     "get_free_port(start_port=random.randint(9700, 9900))   # OE-T1: below the ephemeral range")):
    p = pathlib.Path(f)
    s = p.read_text()
    if new in s:
        continue
    assert s.count(old) == 1, f"port patch: {old!r} not found exactly once in {f}"
    p.write_text(s.replace(old, new))
print("ports patched")
