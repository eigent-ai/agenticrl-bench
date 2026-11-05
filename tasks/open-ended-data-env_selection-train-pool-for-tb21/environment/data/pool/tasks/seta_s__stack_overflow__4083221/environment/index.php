<?php
$uri = $_SERVER['REQUEST_URI'];
$path = strtok($uri, '?');
http_response_code(200);
header('Content-Type: text/plain');
echo "OK route=" . $path . "\n";
