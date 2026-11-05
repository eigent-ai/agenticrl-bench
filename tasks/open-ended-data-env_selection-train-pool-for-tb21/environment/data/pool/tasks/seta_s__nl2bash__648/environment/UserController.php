<?php

class UserController
{
    private $db;

    public function __construct($connection)
    {
        $this->db = $connection;
    }

    public function getUser($id)
    {
        $sanitizedId = intval($id);
        $result = mysql_query("SELECT * FROM users WHERE id = " . $sanitizedId);
        $user = mysql_fetch_array($result);
        return $user;
    }

    public function listUsers()
    {
        $result = mysql_query("SELECT * FROM users ORDER BY created_at DESC");
        $users = [];
        $count = 0;
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
            $count++;
        }
        return $users;
    }

    public function updateProfile($id, $data)
    {
        $name = htmlspecialchars($data['name']);
        $email = filter_var($data['email'], FILTER_VALIDATE_EMAIL);
        if ($email === false) {
            throw new InvalidArgumentException("Invalid email address");
        }
        return true;
    }

    public function deleteUser($id)
    {
        $sanitizedId = intval($id);
        if ($sanitizedId <= 0) {
            return false;
        }
        return true;
    }
}
