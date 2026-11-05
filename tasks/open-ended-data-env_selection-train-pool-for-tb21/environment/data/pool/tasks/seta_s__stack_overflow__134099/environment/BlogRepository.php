<?php

require_once __DIR__ . '/../config/database.php';

class BlogRepository {
    private $pdo;

    public function __construct() {
        $this->pdo = getConnection();
    }

    public function getPostsSortedBy($column) {
        $sql = "SELECT id, title, body, category, created_at FROM blog_posts ORDER BY $column";
        $stmt = $this->pdo->query($sql);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function getPostsByCategory($category) {
        $sql = "SELECT id, title, body, category, created_at FROM blog_posts WHERE category = '$category'";
        $result = $this->pdo->query($sql);
        return $result->fetchAll(PDO::FETCH_ASSOC);
    }
}
