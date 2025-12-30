from datetime import datetime

def validate_datetime(date_str: str, time_str: str = None) -> datetime:
    if not date_str:
        raise ValueError("DATE IS REQUIRED")

    if not time_str:
        time_str = "00:00"

    try:
        clean_date = date_str.strip()
        clean_time = time_str.strip()
        full_str = f"{clean_date} {clean_time}"

        if len(full_str) == 16:
            format_str = "%Y-%m-%d %H:%M"
        elif len(full_str) == 19:
            format_str = "%Y-%m-%d %H:%M:%S"
        else:
            raise ValueError("INVALID DATE TIME FORMAT")

        day = datetime.strptime(full_str, format_str)

    except ValueError:
        raise ValueError(f"INVALID DATETIME FORMAT: '{full_str}'. Use YYYY-MM-DD HH:MM")

    if day < datetime.now():
        raise ValueError("DATETIME CANNOT BE IN THE PAST")

    return day