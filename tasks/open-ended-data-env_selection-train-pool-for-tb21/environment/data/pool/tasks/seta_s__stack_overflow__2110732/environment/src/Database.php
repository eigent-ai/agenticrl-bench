<?php

class Database
{
    private PDO $pdo;

    public function __construct(string $dbPath = '/app/data/content.db')
    {
        $this->pdo = new PDO("sqlite:$dbPath");
    }

    public function getAllCategories(): array
    {
        $stmt = $this->pdo->query("SELECT DISTINCT category FROM content ORDER BY category");
        return $stmt->fetchAll(PDO::FETCH_COLUMN);
    }

    public function getRecordsByCategory(string $category): array
    {
        $sql = "SELECT * FROM content WHERE category = '$category'";
        $stmt = $this->pdo->query($sql);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
