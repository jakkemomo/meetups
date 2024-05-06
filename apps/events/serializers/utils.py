from datetime import datetime, timedelta
from typing import Any

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def nearest_weekday(day_of_week: str):
    """Calculate the nearest future day of the week from the current date"""
    current_datetime = datetime.now()
    current_day_index = DAYS.index(day_of_week)
    current_weekday_index = current_datetime.weekday()
    delta = current_day_index - current_weekday_index
    if delta <= 0:
        delta += 7
    return current_datetime + timedelta(days=delta)


def get_schedule_start(schedules: list[dict[str, Any]]) -> datetime:
    # Find the closest schedule
    closest_schedule = min(schedules, key=lambda x: nearest_weekday(x["day_of_week"]))

    # Get the nearest future day of the week
    nearest_day = nearest_weekday(closest_schedule["day_of_week"])

    # Get schedule time
    schedule_time = closest_schedule["time"]

    # Combine the date and time
    closest_datetime = nearest_day.replace(
        hour=schedule_time.hour,
        minute=schedule_time.minute,
        second=0,
        microsecond=0
    )
    return closest_datetime
