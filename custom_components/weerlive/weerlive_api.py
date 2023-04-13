from datetime import datetime, timedelta
from typing import Any, Mapping, Optional
from .const import LOGGER as _LOGGER

import requests

class Weerlive:
    __REQUEST_URL = "https://weerlive.nl/api/json-data-10min.php"

    def __init__(
        self,
        lon: float,
        lat: float,
        key: str
    ) -> None:
        self.lon = lon
        self.lat = lat
        self.key = key

        self.updated_at: Optional[datetime] = None
        self.data: Mapping[str, Any] = {}

    @property
    def temperature(self) -> Optional[float]:
        return float(self.data.get("temp"))

    @property
    def feel_temperature(self) -> Optional[float]:
        return float(self.data.get("gtemp"))

    @property
    def wind_direction(self) -> Optional[str]:
        return self.data.get("windr")

    @property
    def wind_speed(self) -> float:
        return float(self.data.get("windkmh"))

    @property
    def has_data(self) -> bool:
        return bool(self.data)

    def update(self, timeout: timedelta = 30, safe: bool = False) -> None:
        now = datetime.now()

        if safe:
            data = self._fetch_data_safe(timeout)
            if not data:
                # Error fetching data, return so updated_at isn't updated.
                _LOGGER.debug("Data: %s, updated at: %s", self.data, self.updated_at)
                return
            self.data = data
        else:
            self.data = self._fetch_data(timeout)

        self.updated_at = now

        _LOGGER.debug("Data: %s, updated at: %s", self.data, self.updated_at)

    def _fetch_data(self, timeout: timedelta) -> Mapping[str, Any]:
        params = {
            "locatie": str(self.lat) + "," + str(self.lon),
            "key": self.key,
        }

        resp = requests.get(self.__REQUEST_URL, params=params, timeout=30)
        resp.raise_for_status()

        _LOGGER.debug("URL: %s, Data: %s", resp.url, resp.text)

        data = resp.json()

        return data.get('liveweer')[0]

    def _fetch_data_safe(self, timeout: timedelta) -> Mapping[str, Any]:
        try:
            return self._fetch_data(timeout)
        except requests.exceptions.RequestException as exc:
            _LOGGER.warning("Error fetching data safely: %s", exc)

        return {}
