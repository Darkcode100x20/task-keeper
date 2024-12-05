from datetime import datetime
from pytz import UTC

def get_current_utc_time():
    """Returns the current time in UTC."""
    return datetime.now(UTC)
