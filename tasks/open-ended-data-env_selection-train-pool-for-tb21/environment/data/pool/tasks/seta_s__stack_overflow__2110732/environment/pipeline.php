<?php

require_once __DIR__ . '/src/Logger.php';
require_once __DIR__ . '/src/Database.php';
require_once __DIR__ . '/src/ContentProcessor.php';
require_once __DIR__ . '/src/Pipeline.php';

$pipeline = new Pipeline();
$pipeline->run();
