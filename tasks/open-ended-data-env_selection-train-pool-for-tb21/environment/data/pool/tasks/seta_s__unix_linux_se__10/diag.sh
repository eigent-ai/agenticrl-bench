#!/bin/bash
TARGET="/var/www/html/config.php"

echo "=== 1. getfattr -d at build time ==="
getfattr -d "$TARGET" 2>&1

echo ""
echo "=== 2. setfattr user.test_attr=hello ==="
setfattr -n user.test_attr -v hello "$TARGET" 2>&1

echo ""
echo "=== 3. getfattr -d after runtime set ==="
getfattr -d "$TARGET" 2>&1

echo ""
echo "=== 4. Python os.listxattr ==="
python3 -c "import os; print(os.listxattr('$TARGET'))" 2>&1

echo ""
echo "=== 5. mount | grep overlay ==="
mount | grep overlay 2>&1

echo ""
echo "=== 6. setfattr user.scan_status=clean ==="
setfattr -n user.scan_status -v clean "$TARGET" 2>&1

echo ""
echo "=== 7. getfattr -d after scan_status ==="
getfattr -d "$TARGET" 2>&1

echo ""
echo "=== 8. Python os.listxattr final ==="
python3 -c "import os; print(os.listxattr('$TARGET'))" 2>&1
