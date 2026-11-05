<?php
header('Content-Type: application/json');
$dir = __DIR__ . '/uploads/';
$files = array_values(array_diff(scandir($dir), ['.', '..']));
echo json_encode($files);
