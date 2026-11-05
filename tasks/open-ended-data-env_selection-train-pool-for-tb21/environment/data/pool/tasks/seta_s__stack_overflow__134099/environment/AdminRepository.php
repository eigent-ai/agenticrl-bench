<?php

require_once __DIR__ . '/../config/database.php';

class AdminRepository {
    private $pdo;

    public function __construct() {
        $this->pdo = getConnection();
    }

    public function getTable($tableName) {
        $sql = "SELECT * FROM $tableName LIMIT 50";
        $stmt = $this->pdo->query($sql);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
