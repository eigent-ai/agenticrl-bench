<?php
require_once __DIR__ . '/handlers/errors.php';
require_once __DIR__ . '/lib/stats.php';
require_once __DIR__ . '/lib/formatter.php';

$data = [4, 8, 15, 16, 23, 42];
$stats = calculate_stats($data);
$output = format_result($stats);
echo json_encode($output) . "\n";
