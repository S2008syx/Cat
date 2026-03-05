"""
UserData Converter — local birth time + UTC offset → UTC datetime.
"""

from datetime import datetime, timezone, timedelta


def local_to_utc(birth_date: str, birth_time: str, utc_offset: float) -> datetime:
    """Convert local birth date/time + UTC offset to UTC datetime.

    Args:
        birth_date: "YYYY-MM-DD"
        birth_time: "HH:MM"
        utc_offset: Hours offset from UTC (e.g. 8.0 for China, -5.0 for US Eastern)

    Returns:
        datetime in UTC timezone.
    """
    dt_str = f"{birth_date} {birth_time}"
    local_tz = timezone(timedelta(hours=utc_offset))
    local_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=local_tz)
    return local_dt.astimezone(timezone.utc)
