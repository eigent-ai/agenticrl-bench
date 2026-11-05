<?php
header('Content-Type: application/json');
echo json_encode([
    'status'      => 'ok',
    'sapi'        => php_sapi_name(),
    'php_version' => PHP_VERSION,
]);
