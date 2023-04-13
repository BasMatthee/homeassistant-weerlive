from datetime import datetime, timedelta
from typing import Any, Mapping, Optional, Union

import requests

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    CONF_API_KEY,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util

from .const import (
    ATTRIBUTION,
    DEFAULT_NAME,
    ITEM_TEMP,
    ITEM_FEEL_TEMP,
    ITEM_WIND_SPEED,
    ITEM_WIND_DIRECTION,
)
from .const import LOGGER as _LOGGER
from .const import SENSOR_TYPES, UPDATE_INTERVAL, SensorType
from .weerlive_api import Weerlive

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_MONITORED_CONDITIONS, default=[ITEM_TEMP]): vol.All(
            cv.ensure_list, vol.Length(min=1), [vol.In(SENSOR_TYPES.keys())]
        ),

        vol.Inclusive(
            CONF_LATITUDE, "coordinates", "Latitude and longitude must exist together"
        ): cv.latitude,

        vol.Inclusive(
            CONF_LONGITUDE, "coordinates", "Latitude and longitude must exist together"
        ): cv.longitude,

        vol.Required(
            CONF_API_KEY, "api_keys", "API-Key of Weerlive"
        ): cv.string,

        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    latitude = config.get(CONF_LATITUDE, hass.config.latitude)
    longitude = config.get(CONF_LONGITUDE, hass.config.longitude)
    key = config.get(CONF_API_KEY)

    if None in (latitude, longitude):
        _LOGGER.error("Latitude or longitude not set in HomeAssistant config")
        return

    api = Weerlive(longitude, latitude, key)

    def api_update():
        api.update(safe=True)

        _LOGGER.debug("New data: %s", api.data)

    async def async_api_update():
        await hass.async_add_executor_job(api_update)

    client_name = config.get(CONF_NAME)
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=client_name,
        update_method=async_api_update,
        update_interval=UPDATE_INTERVAL,
    )
    entities = [
        WeerliveSensor(coordinator, api, sensor, client_name)
        for sensor in config[CONF_MONITORED_CONDITIONS]
    ]
    async_add_entities(entities, True)

class WeerliveSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        api: Weerlive,
        sensor_type_name: str,
        client_name: str
    ) -> None:
        super().__init__(coordinator)
        self._api = api
        self._sensor_type_name = sensor_type_name
        self._client_name = client_name

    @property
    def name(self) -> str:
        return f"{self._client_name} {self._sensor_type.name}"

    @property
    def unit_of_measurement(self) -> str:
        return self._sensor_type.unit

    @property
    def icon(self) -> str:
        return self._sensor_type.icon

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        attr = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

        return attr

    @property
    def state(self) -> Optional[Union[datetime, float]]:
        _LOGGER.debug("Get state: %s", self._sensor_type_name)
        if not self._api.has_data:
            return None

        if self._sensor_type_name == ITEM_TEMP:
            return round(self._api.temperature, 1)
        elif self._sensor_type_name == ITEM_FEEL_TEMP:
            return round(self._api.feel_temperature, 1)
        elif self._sensor_type_name == ITEM_WIND_DIRECTION:
            return self._api.wind_direction
        elif self._sensor_type_name == ITEM_WIND_SPEED:
            return self._api.wind_speed
        else:
            raise NotImplementedError("Unknown sensor type")

    @property
    def _sensor_type(self) -> SensorType:
        return SENSOR_TYPES[self._sensor_type_name]
