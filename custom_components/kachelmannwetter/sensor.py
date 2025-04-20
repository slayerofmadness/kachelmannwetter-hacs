import logging
import aiohttp
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, API_BASE_URL, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data[CONF_API_KEY]
    lat = config_entry.data[CONF_LATITUDE]
    lon = config_entry.data[CONF_LONGITUDE]

    session = aiohttp.ClientSession()

    async def fetch_data():
        url = f"{API_BASE_URL}/forecast/dwd-icon/point?lat={lat}&lon={lon}&model=icon-d2"
        headers = {"api-key": api_key}
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise UpdateFailed(f"API error: {response.status}")
            return await response.json()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="kachelmannwetter",
        update_method=fetch_data,
        update_interval=timedelta(minutes=15),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        TemperatureSensor(coordinator),
        ConditionSensor(coordinator),
        PrecipitationSensor(coordinator)
    ]

    async_add_entities(sensors)

class TemperatureSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kachelmann Temperatur"
        self._attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self):
        try:
            return self.coordinator.data["forecast"]["data"]["temperature"]["values"][0]["value"]
        except Exception:
            return None

class ConditionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kachelmann Wetterzustand"

    @property
    def native_value(self):
        try:
            return self.coordinator.data["forecast"]["data"]["symbol"]["values"][0]["value"]
        except Exception:
            return None

class PrecipitationSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Kachelmann Regenwahrscheinlichkeit"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        try:
            return self.coordinator.data["forecast"]["data"]["precipitation_probability"]["values"][0]["value"]
        except Exception:
            return None
