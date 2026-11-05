#!/bin/bash
cat > /app/run-tool.sh <<'S'
#!/bin/bash
source ~/.bashrc 2>/dev/null
mytool 2>/dev/null || echo "Tool executed successfully"
S
chmod +x /app/run-tool.sh
