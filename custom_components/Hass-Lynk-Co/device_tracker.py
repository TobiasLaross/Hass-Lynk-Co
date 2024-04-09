from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from .const import DOMAIN, COORDINATOR
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get("vin")
    async_add_entities([LynkCoDeviceTracker(coordinator, vin)])


class LynkCoDeviceTracker(CoordinatorEntity, TrackerEntity):
    def __init__(self, coordinator, vin):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._vin = vin
        self._data_path_long = "vehicle_record.position.longitude".split(".")
        self._data_path_lat = "vehicle_record.position.latitude".split(".")
        self._attr_unique_id = f"{DOMAIN}_{self._vin}_location"
        self._attr_name = "Lynk & Co Vehicle Tracker"

    @property
    def latitude(self):
        return self._get_data_by_path(self._data_path_lat)

    @property
    def longitude(self):
        return self._get_data_by_path(self._data_path_long)

    def _get_data_by_path(self, path):
        data = self.coordinator.data
        for key in path:
            if data is not None and key in data:
                data = data[key]
            else:
                return None
        return data

    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def available(self):
        # Check if both latitude and longitude data are not None
        return self.latitude is not None and self.longitude is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"lynk_co_{self._vin}")},
            "name": f"Lynk & Co {self._vin}",
            "manufacturer": "Lynk & Co",
        }

    @property
    def unique_id(self):
        return f"{self._vin}_{self._attr_name}"
