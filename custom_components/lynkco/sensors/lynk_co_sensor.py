import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LynkCoSensor(CoordinatorEntity):
    def __init__(
        self,
        coordinator,
        vin,
        name,
        data_path,
        unit_of_measurement=None,
        state_mapping=None,
    ):
        super().__init__(coordinator)
        self._vin = vin
        self._name = name
        self._data_path = data_path.split(".")
        self._unit_of_measurement = unit_of_measurement
        self._state_mapping = state_mapping

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"lynk_co_{self._vin}")},
            manufacturer="Lynk & Co",
            name=f"Lynk & Co {self._vin}",
        )

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.coordinator.data
        for key in self._data_path:
            if data:
                data = data.get(key)
        if self._state_mapping:
            return self._state_mapping.get(data, data)
        return data

    @property
    def available(self):
        data = self.coordinator.data
        for key in self._data_path:
            if data is not None and key in data:
                data = data[key]
            else:
                _LOGGER.error(
                    f"Data path not found: {self._data_path}, coordinator.data: {self.coordinator.data}"
                )
                return False  # Data path not found, mark as unavailable
        return True  # Data path found, mark as available

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def unique_id(self):
        return f"{self._vin}_{self._name}"
