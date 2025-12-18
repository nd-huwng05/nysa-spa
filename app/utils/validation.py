from datetime import datetime
from app.core.errors import NewError


def validate_datetime(datetime_str: str) -> datetime:
    if not datetime_str:
        raise NewError(400, "DATE IS REQUIRED")

    try:
        clean_str = datetime_str.strip()

        if len(clean_str) == 16:
            format_str = "%Y-%m-%d %H:%M"
        elif len(clean_str) == 19:
            format_str = "%Y-%m-%d %H:%M:%S"
        else:
            raise ValueError()

        day = datetime.strptime(clean_str, format_str)

    except ValueError:

        raise NewError(400, f"INVALID DATETIME FORMAT: '{datetime_str}'. Use YYYY-MM-DD HH:MM or HH:MM:SS")

    if day < datetime.now():
        raise NewError(400, "DATETIME CANNOT BE IN THE PAST")

    return day