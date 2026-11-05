<?php

require_once '/opt/pipeline/config/settings.php';

$inputPath = $tmpDir . 'transformed.json';
if (!file_exists($inputPath)) {
    fwrite(STDERR, "Error: Transformed data not found at $inputPath\n");
    exit(1);
}

$products = json_decode(file_get_contents($inputPath), true);
if ($products === null) {
    fwrite(STDERR, "Error: Failed to decode transformed JSON\n");
    exit(1);
}

$totalProducts = count($products);
$totalPriceSum = 0.0;
$categoryCounts = [];
$productList = [];

foreach ($products as $product) {
    $totalPriceSum += $product['price'];

    $cat = $product['category'];
    if (!isset($categoryCounts[$cat])) {
        $categoryCounts[$cat] = 0;
    }
    $categoryCounts[$cat]++;

    $productList[] = [
        'name' => $product['name'],
        'price' => $product['price'],
        'category' => $product['category'],
        'stock' => $product['stock'],
        'price_tier' => $product['price_tier'],
    ];
}

ksort($categoryCounts);

$report = [
    'total_products' => $totalProducts,
    'total_price_sum' => round($totalPriceSum, 2),
    'category_counts' => $categoryCounts,
    'products' => $productList,
];

if (!is_dir($outputDir)) {
    mkdir($outputDir, 0755, true);
}

$reportPath = $outputDir . 'report.json';
file_put_contents($reportPath, json_encode($report, JSON_PRETTY_PRINT));

echo "Report written to $reportPath\n";
