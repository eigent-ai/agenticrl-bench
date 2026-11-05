<?php
$conn = new mysqli('localhost', 'taskboard', 'tb_secret_123', 'taskboard_db');
if ($conn->connect_error) {
    http_response_code(500);
    die("DB_ERROR: " . $conn->connect_error);
}
$result = $conn->query("SELECT 1");
if ($result) {
    echo "DB_OK";
} else {
    http_response_code(500);
    echo "DB_ERROR: " . $conn->error;
}
$conn->close();
?>
