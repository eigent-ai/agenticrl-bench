#!/bin/bash
cat > /app/run-tool.sh <<'S'
#!/bin/bash
set -e
mytool() {
    /opt/tools/bin/custom/my-tool "$@"
}
mytool
S
chmod +x /app/run-tool.sh
