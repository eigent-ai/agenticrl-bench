<?php
define('DB_HOST', 'localhost');
define('DB_NAME', 'appdb');
define('DB_USER', 'appuser');
define('DB_PASS', 'secret123');

$config_path = '/var/www/html/config/settings.json';
if (file_exists($config_path)) {
    $raw = file_get_contents($config_path);
    $settings = json_decode($raw, true);
}
