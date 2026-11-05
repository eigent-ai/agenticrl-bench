<?php
$numbers = [3, 7, 11, 13, 17];
$sum     = array_sum($numbers);
$product = array_product($numbers);
header('Content-Type: application/json');
echo json_encode(['sum' => $sum, 'product' => $product]);
