from zoneinfo import ZoneInfo
from datetime import datetime

from config.timezone_config import CENTRAL_TZ


def convert_to_central(utc_dt: datetime) -> datetime:
    """Convert a naive UTC datetime to US Central local time.

    Args:
        utc_dt: A naive datetime object representing UTC time.
    Returns:
        An aware datetime object in the Central US timezone.
    """
    utc_aware = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    return utc_aware.astimezone(ZoneInfo(CENTRAL_TZ))
