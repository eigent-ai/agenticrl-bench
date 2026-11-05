<?php
require_once __DIR__ . '/handlers/errors.php';
trigger_error("Test warning from run_tests.php", E_USER_WARNING);
echo "Handler test complete\n";
