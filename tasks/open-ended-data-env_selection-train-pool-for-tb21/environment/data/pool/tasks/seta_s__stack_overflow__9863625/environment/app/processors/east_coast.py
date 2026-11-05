from zoneinfo import ZoneInfo
from datetime import datetime

from config.timezone_config import EAST_TZ


def convert_to_eastern(utc_dt: datetime) -> datetime:
    """Convert a naive UTC datetime to US Eastern local time.

    Args:
        utc_dt: A naive datetime object representing UTC time.
    Returns:
        An aware datetime object in the Eastern US timezone.
    """
    utc_aware = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    return utc_aware.astimezone(ZoneInfo(EAST_TZ))
