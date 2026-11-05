#!/bin/sh
# Install the workload side of the sandbox gate into an interpreter, without pip and without the
# daemon/backend modules (so no platform code or names land where workloads can read them):
#   sh install-client.sh <python> [bin-dir]
# Installs sandbox_broker/{__init__,cli,client,protocol,policy,harbor_env}.py into <python>'s
# site-packages and a `sandbox` command into bin-dir (default /usr/local/bin). Run as root at build time.
set -eu
py="$1"; bindir="${2:-/usr/local/bin}"
here="$(cd "$(dirname "$0")/.." && pwd)"
site="$("$py" -I -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
dest="$site/sandbox_broker"
rm -rf "$dest"
install -d -m 0755 "$dest"
for f in __init__.py cli.py client.py protocol.py policy.py harbor_env.py; do
  install -m 0644 "$here/sandbox_broker/$f" "$dest/$f"
done
install -d -m 0755 "$bindir"
printf '#!%s -I\nimport sys\nfrom sandbox_broker.cli import main\nsys.exit(main())\n' "$py" > "$bindir/sandbox"
chmod 0755 "$bindir/sandbox"
"$py" -I -B -c 'import sandbox_broker.cli, sandbox_broker.client'
echo "sandbox client installed into $dest; command: $bindir/sandbox"
