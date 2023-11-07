import pytz
from timezonefinder import TimezoneFinder


def get_timezone_from_coordinates(latitude, longitude):
    tz_finder = TimezoneFinder()
    timezone_str = tz_finder.timezone_at(lng=longitude, lat=latitude)
    return pytz.timezone(timezone_str) if timezone_str else pytz.utc
