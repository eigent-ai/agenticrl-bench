<?php
function send_notification($to, $subject, $body) {
    $headers = "From: noreply@myapp.local\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    return mail($to, $subject, $body, $headers);
}

function send_admin_alert($message) {
    $admin_email = 'admin@myapp.local';
    return send_notification($admin_email, 'System Alert', $message);
}
