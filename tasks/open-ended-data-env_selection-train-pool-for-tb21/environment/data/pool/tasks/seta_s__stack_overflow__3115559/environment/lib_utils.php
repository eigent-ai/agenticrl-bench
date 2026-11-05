<?php
function sanitize_input($input) {
    return htmlspecialchars(strip_tags(trim($input)), ENT_QUOTES, 'UTF-8');
}

function format_list($items) {
    return array_map('strtolower', $items);
}

function get_timestamp() {
    return date('Y-m-d H:i:s');
}

function generate_slug($title) {
    $slug = strtolower($title);
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
    return trim($slug, '-');
}
