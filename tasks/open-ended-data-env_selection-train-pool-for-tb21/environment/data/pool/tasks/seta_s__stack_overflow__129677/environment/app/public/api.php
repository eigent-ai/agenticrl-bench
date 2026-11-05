<?php
require_once __DIR__ . '/../src/helpers.php';

header('Content-Type: application/json');

$id = $_GET['id'] ?? 0;
$db = get_db();

$stmt = $db->prepare("SELECT * FROM products WHERE id = :id");
$stmt->execute(['id' => $id]);
$row = $stmt->fetch(PDO::FETCH_ASSOC);

if ($row) {
    echo '{"id":' . $row['id'] . ',"name":"' . $row['name'] . '","desc":"' . $row['description'] . '","price":' . $row['price'] . '}';
} else {
    http_response_code(404);
    echo '{"error":"not found"}';
}
