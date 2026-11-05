<?php
function load_page($slug) {
    $pages_dir = '/var/www/html/data/pages/';
    $file = $pages_dir . $slug . '.json';
    if (!file_exists($file)) {
        return null;
    }
    $content = file_get_contents($file);
    return json_decode($content, true);
}

function render_page($page_data) {
    if (!$page_data) {
        return '<h1>404 - Page Not Found</h1>';
    }
    $title = htmlspecialchars($page_data['title']);
    $body = htmlspecialchars($page_data['body']);
    return "<h1>{$title}</h1><div>{$body}</div>";
}
