import logging
from datetime import timedelta
from typing import NamedTuple

from homeassistant.const import LENGTH_MILLIMETERS, TEMP_CELSIUS, SPEED_KILOMETERS_PER_HOUR

SensorType = NamedTuple(
    "SensorType",
    [
        ("name", str),
        ("unit", str),
        ("icon", str),
    ],
)


LOGGER = logging.getLogger(__package__)
UPDATE_INTERVAL = timedelta(seconds=300)
ATTRIBUTION = "Data provided by Meteoserver"
DEFAULT_NAME = "weerlive"

ICON_THERMOMETER = "mdi:thermometer"
ICON_WEATHER_POURING = "mdi:weather-pouring"
ICON_WIND_SPEED = "mdi:weather-windy"
ICON_WIND_DIRECTION = "mdi:windsock"

ITEM_TEMP = "temperature"
ITEM_FEEL_TEMP = "temperature_feels_like"
ITEM_WIND_SPEED = "wind_speed"
ITEM_WIND_DIRECTION = "wind_direction"

SENSOR_TYPES = {
    ITEM_TEMP: SensorType(
        "Temperature",
        TEMP_CELSIUS,
        ICON_THERMOMETER
    ),
    ITEM_FEEL_TEMP: SensorType(
        "Temperature (feels like)",
        TEMP_CELSIUS,
        ICON_THERMOMETER
    ),
    ITEM_WIND_SPEED: SensorType(
        "Wind speed",
        SPEED_KILOMETERS_PER_HOUR,
        ICON_WIND_SPEED
    ),
    ITEM_WIND_DIRECTION: SensorType(
        "Wind direction",
        "",
        ICON_WIND_DIRECTION
    ),
}
