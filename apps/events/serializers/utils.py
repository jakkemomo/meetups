from datetime import datetime, timedelta
from typing import Any

from django.contrib.gis.geos import Polygon, Point

from apps.events.models.city import City

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


def area_bbox(location: dict):
    """
    Return Poligon area approximately 1 km radius around specified koordinates
    """
    r = 0.01
    min_lat = float(location['latitude']) - r
    max_lat = float(location['latitude']) + r
    min_lng = float(location['longitude']) - r
    max_lng = float(location['longitude']) + r

    bbox = (min_lng, min_lat, max_lng, max_lat)
    return Polygon.from_bbox(bbox)


def update_city_if_exist(instance, validated_data):
    city_location = validated_data.pop("city_location")
    city = City.objects.filter(
        location__within=area_bbox(city_location["location"])
    ).first()
    if not city:
        city = City.objects.create(
            place_id=city_location["place_id"],
            north_east_point=Point((
                city_location["north_east_point"]["longitude"],
                city_location["north_east_point"]["latitude"]
            )),
            south_west_point=Point((
                city_location["south_west_point"]["longitude"],
                city_location["south_west_point"]["latitude"],
            )),
            location=Point((
                city_location["location"]["longitude"],
                city_location["location"]["latitude"],
            )),
        )
        instance.city_location = city
        return instance
    if city.place_id != city_location["place_id"] and city_location["place_id"] != "":
        city.place_id = city_location["place_id"]
        city.save()
    instance.city_location = city
    return instance
