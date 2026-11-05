<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !isset($_FILES['file'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Bad request']);
    exit;
}
$filename = basename($_FILES['file']['name']);
if (!preg_match('/^[\w\-\.]+$/', $filename)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid filename']);
    exit;
}
$dest = __DIR__ . '/uploads/' . $filename;
if (move_uploaded_file($_FILES['file']['tmp_name'], $dest)) {
    http_response_code(200);
    echo json_encode(['success' => true, 'file' => $filename]);
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Write failed']);
}
