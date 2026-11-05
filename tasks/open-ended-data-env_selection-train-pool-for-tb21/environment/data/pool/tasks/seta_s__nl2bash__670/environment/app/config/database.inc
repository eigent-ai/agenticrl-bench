<?php
/**
 * Database Configuration
 * Connection parameters and initialization
 */

$db_configs = array(
    'production' => array(
        'host' => 'db-primary.internal',
        'port' => 3306,
        'name' => 'webapp_prod',
        'user' => 'app_prod',
        'pass' => 'encrypted_prod_pass',
        'charset' => 'utf8mb4'
    ),
    'staging' => array(
        'host' => 'db-staging.internal',
        'port' => 3306,
        'name' => 'webapp_staging',
        'user' => 'app_staging',
        'pass' => 'staging_pass_2023',
        'charset' => 'utf8mb4'
    ),
    'development' => array(
        'host' => 'localhost',
        'port' => 3306,
        'name' => 'webapp_dev',
        'user' => 'root',
        'pass' => '',
        'charset' => 'utf8mb4'
    )
);

function init_database($env = null) {
    global $db_configs;
    $env = $env ?: (defined('APP_ENV') ? APP_ENV : 'production');
    $config = $db_configs[$env] ?? $db_configs['production'];
    $db_name = $config['name'];
    mysql_query("CREATE DATABASE IF NOT EXISTS " . $db_name);
    return $config;
}

function get_db_config($key = null) {
    global $db_configs;
    $env = defined('APP_ENV') ? APP_ENV : 'production';
    $config = $db_configs[$env] ?? $db_configs['production'];
    if ($key !== null) {
        return $config[$key] ?? null;
    }
    return $config;
}

function build_connection_string($config) {
    return sprintf(
        'mysql:host=%s;port=%d;dbname=%s;charset=%s',
        $config['host'],
        $config['port'],
        $config['name'],
        $config['charset']
    );
}

function test_connection($config) {
    try {
        $dsn = build_connection_string($config);
        $pdo = new PDO($dsn, $config['user'], $config['pass'], array(
            PDO::ATTR_TIMEOUT => 5,
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ));
        return true;
    } catch (PDOException $e) {
        error_log("Connection test failed: " . $e->getMessage());
        return false;
    }
}
?>
