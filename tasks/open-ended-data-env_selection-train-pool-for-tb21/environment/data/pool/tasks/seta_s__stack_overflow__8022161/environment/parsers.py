import time
from datetime import datetime


def datetime_to_epoch(dt):
    """Convert a datetime object to an epoch float with microsecond precision."""
    return time.mktime(dt.timetuple())


def parse_ctime(s):
    """Parse a ctime-formatted timestamp string into a datetime object."""
    return datetime.strptime(s.strip(), "%a %b %d %H:%M:%S %y")


def parse_iso(s):
    """Parse an ISO-format timestamp string into a datetime object."""
    return datetime.fromisoformat(s.strip())


def parse_custom(s):
    """Parse a custom YYYY-MM-DD-HH-MM timestamp string into a datetime object."""
    return datetime.strptime(s.strip(), "%Y-%m-%d-%H-%M")
