<?php
$server_info = php_uname();
$php_ver = phpversion();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MagentoLite Store</title>
</head>
<body>
    <h1>Welcome to MagentoLite</h1>
    <p>Your e-commerce platform is running smoothly.</p>
    <div class="server-info">
        <h3>Server Information</h3>
        <ul>
            <li>Server: <?php echo $server_info; ?></li>
            <li>PHP Version: <?php echo $php_ver; ?></li>
            <li>Timestamp: <?php echo date('Y-m-d H:i:s'); ?></li>
        </ul>
    </div>
    <div class="products">
        <h3>Featured Products</h3>
        <ul>
            <li>Widget Pro - $29.99</li>
            <li>Gadget Plus - $49.99</li>
            <li>Accessory Kit - $19.99</li>
        </ul>
    </div>
</body>
</html>
