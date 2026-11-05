<?php

function getConnection() {
    $host = '127.0.0.1';
    $dbname = 'webapp';
    $user = 'root';
    $pass = '';

    $dsn = "mysql:host=$host;dbname=$dbname";

    $pdo = new PDO($dsn, $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->exec("SET NAMES gbk");

    return $pdo;
}
