<?php
header('Content-Type: application/json');
echo json_encode(['legacy' => true, 'ext' => 'php5', 'value' => 42]);
