<?php

function universal_sanitize($str) {
    return htmlspecialchars(addslashes($str), ENT_QUOTES, 'UTF-8');
}

function get_db() {
    $db = new PDO('sqlite:/app/data/app.db');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $db;
}
