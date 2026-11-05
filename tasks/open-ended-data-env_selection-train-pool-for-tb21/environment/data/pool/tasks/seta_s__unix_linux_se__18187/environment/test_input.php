<?php
$data = array(1, 2, 3, 4, 5);
$result = array();

while (count($data) > 0) {
    $item = array_shift($data);
    while ($item > 0) {
        if ($item % 2 == 0) {
            $result[] = $item;
            break;
        }
        $item--;
    }
}

echo implode(", ", $result);
?>
