def to_minutes(s: str):
    parts = s.split()
    if len(parts) == 1:
        return int(parts[0].strip("min"))
    else:
        return int(parts[0].strip("h")) * 60 + int(parts[1].strip("min"))


def strtime_diff(time1: str, time2: str):
    """Get difference between first and second time.
    Example 3h 12min - 1h 10min"""

    return abs(to_minutes(time1) - to_minutes(time2))
