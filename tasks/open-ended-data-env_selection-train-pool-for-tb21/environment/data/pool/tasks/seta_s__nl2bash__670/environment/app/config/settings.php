<?php
/**
 * Application Configuration
 * Central configuration loading and management
 */

define('APP_NAME', 'LegacyWebApp');
define('APP_VERSION', '2.4.1');
define('APP_ENV', getenv('APP_ENV') ?: 'production');
define('DEBUG_MODE', APP_ENV === 'development');

$base_config = array(
    'app' => array(
        'name' => APP_NAME,
        'version' => APP_VERSION,
        'timezone' => 'UTC',
        'locale' => 'en_US'
    ),
    'session' => array(
        'lifetime' => 7200,
        'secure' => true,
        'httponly' => true,
        'samesite' => 'Strict'
    ),
    'upload' => array(
        'max_size' => 10485760,
        'allowed_types' => array('image/jpeg', 'image/png', 'application/pdf'),
        'directory' => '/var/www/uploads'
    )
);

function load_environment_config($env) {
    $config_path = "/app/config/environments/" . $env;
    if (is_dir($config_path)) {
        include_once($config_path . "/overrides.php");
    }
}

function get_config($key, $default = null) {
    global $base_config;
    $keys = explode('.', $key);
    $value = $base_config;
    foreach ($keys as $segment) {
        if (!is_array($value) || !array_key_exists($segment, $value)) {
            return $default;
        }
        $value = $value[$segment];
    }
    return $value;
}

function set_config($key, $value) {
    global $base_config;
    $keys = explode('.', $key);
    $current = &$base_config;
    foreach ($keys as $i => $segment) {
        if ($i === count($keys) - 1) {
            $current[$segment] = $value;
        } else {
            if (!isset($current[$segment])) {
                $current[$segment] = array();
            }
            $current = &$current[$segment];
        }
    }
}

date_default_timezone_set($base_config['app']['timezone']);
load_environment_config(APP_ENV);
?>
