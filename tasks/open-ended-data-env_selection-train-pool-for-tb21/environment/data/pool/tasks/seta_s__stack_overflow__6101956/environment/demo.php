<?php
require_once __DIR__ . '/passgen.php';

echo "=== generateBasic (8 chars) ===\n";
for ($i = 0; $i < 5; $i++) {
    $pw = generateBasic(8);
    $type = gettype($pw);
    echo "  result: " . (is_array($pw) ? '[' . implode('', $pw) . '] (ARRAY!)' : $pw) . "  (type: $type)\n";
}

echo "\n=== generateWithSymbol (10 chars) ===\n";
$syms = '!@#$%^&*()-+?';
for ($i = 0; $i < 10; $i++) {
    $pw = generateWithSymbol(10);
    $has_sym = false;
    for ($j = 0; $j < strlen($pw); $j++) {
        if (strpos($syms, $pw[$j]) !== false) { $has_sym = true; break; }
    }
    echo "  result: '$pw'  len=" . strlen($pw) . "  has_symbol=" . ($has_sym ? 'yes' : 'NO!') . "\n";
}

echo "\n=== generateCustom ===\n";
echo "  generateCustom(5, 'abc0123'): " . generateCustom(5, 'abc0123') . "\n";
echo "  generateCustom(10, 'A')     : " . generateCustom(10, 'A') . "\n";
echo "  generateCustom(8, 'ab')     : " . generateCustom(8, 'ab') . "\n";
