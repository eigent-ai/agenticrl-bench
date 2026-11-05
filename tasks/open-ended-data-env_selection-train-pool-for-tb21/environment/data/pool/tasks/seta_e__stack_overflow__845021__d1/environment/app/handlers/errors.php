<?php
$log_file = '/var/log/php_app_errors.log';

function custom_error_handler($errno, $errstr, $errfile, $errline) {
    global $log_file;
}

set_error_handler('custom_error_handler');
