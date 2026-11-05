<?php
if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["filename"])) {
    $f = "/var/www/tenant_b/" . basename($_POST["filename"]);
    file_put_contents($f, "created by tenant_b at " . date("Y-m-d H:i:s"));
    echo "Created: $f";
} else {
    echo "POST filename to create a file";
}
?>
