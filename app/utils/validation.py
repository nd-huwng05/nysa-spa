from datetime import datetime

from app.core.errors import NewError

def validate_datetime(date_str:str, time_str:str = None):
    if not date_str:
        return NewError(400, "DATE IS NOT VALID")

    if not time_str:
        return NewError(400, "TIME IS NOT VALID")

    datetime_str = f"{date_str} {time_str if time_str else '00:00:00'}"
    format_str = "%Y-%m-%dT%H:%M:%S"

    try:
        day = datetime.strptime(datetime_str,format_str)
    except ValueError:
        raise NewError(400, "ERROR FORMAT DATETIME ")

    if day < datetime.now():
        raise NewError(400, "ERROR DATETIME IN PAST ")

    return day