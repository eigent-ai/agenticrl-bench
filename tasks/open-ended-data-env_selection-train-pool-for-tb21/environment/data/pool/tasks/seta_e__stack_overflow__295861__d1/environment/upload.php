<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    die("UPLOAD_ERROR: POST method required");
}
if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    die("UPLOAD_ERROR: No valid file provided");
}
$target_dir = __DIR__ . '/uploads/';
$target_file = $target_dir . basename($_FILES['file']['name']);
if (move_uploaded_file($_FILES['file']['tmp_name'], $target_file)) {
    echo "UPLOAD_OK";
} else {
    http_response_code(500);
    echo "UPLOAD_ERROR: Failed to save file";
}
?>
