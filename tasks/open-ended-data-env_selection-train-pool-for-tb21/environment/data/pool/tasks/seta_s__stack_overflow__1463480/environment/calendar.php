<?php
require_once 'db.php';

header('Content-Type: text/plain');
header('Content-Disposition: attachment; filename="calendar.ics"');

echo "BEGIN:VCALENDAR\n";
echo "PRODID:-//MyCalendar//EN\n";
echo "CALSCALE:GREGORIAN\n";
echo "METHOD:PUBLISH\n";

$results = $db->query("SELECT * FROM events ORDER BY start_time");

while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
    echo "BEGIN:VEVENT\n";
    echo "UID:calendar-event@myapp.com\n";

    $start = date('Ymd\THis', strtotime($row['start_time']));
    $end = date('Ymd\THis', strtotime($row['end_time']));
    echo "DTSTART:{$start}Z\n";
    echo "DTEND:{$end}Z\n";

    echo "SUMMARY:{$row['title']}\n";
    echo "DESCRIPTION:{$row['description']}\n";
    echo "LOCATION:{$row['location']}\n";
    echo "END:VEVENT\n";
}

echo "END:VCALENDAR\n";
?>
