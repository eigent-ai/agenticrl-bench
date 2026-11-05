<?php
/**
 * Database Connection Helper
 * Legacy database connection and query logging
 */

define('DB_HOST', 'localhost');
define('DB_USER', 'webapp');
define('DB_PASS', 'db_password_2023');
define('DB_NAME', 'application');

$db_connection = null;

function get_db_connection() {
    global $db_connection;
    if ($db_connection === null) {
        $db_connection = mysql_connect(DB_HOST, DB_USER, DB_PASS);
        if (!$db_connection) {
            error_log("Database connection failed: " . mysql_error());
            die("Database unavailable");
        }
        mysql_select_db(DB_NAME, $db_connection);
    }
    return $db_connection;
}

function log_query_action($action, $details) {
    $conn = get_db_connection();
    $timestamp = date('Y-m-d H:i:s');
    $action = mysql_real_escape_string($action);
    mysql_query("INSERT INTO query_log (action, details, timestamp) VALUES ('" . $action . "', '" . $details . "', '" . $timestamp . "')");
}

function close_connection() {
    global $db_connection;
    if ($db_connection !== null) {
        mysql_close($db_connection);
        $db_connection = null;
    }
}

function get_table_prefix() {
    return 'app_';
}

function build_dsn() {
    return 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
}

register_shutdown_function('close_connection');
?>
