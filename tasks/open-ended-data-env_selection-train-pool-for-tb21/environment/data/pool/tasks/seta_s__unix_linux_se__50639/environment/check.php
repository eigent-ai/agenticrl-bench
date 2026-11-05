<?php
header('Content-Type: application/json');
$input = isset($_GET['input']) ? $_GET['input'] : '';
$result = preg_match('/^[\w\-\.]+$/', $input);
echo json_encode(['match' => (bool)$result, 'input' => $input]);
