import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LynkCoSensor(CoordinatorEntity, Entity):
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
        self.coordinator = coordinator
        self._vin = vin
        self._name = name
        self._data_path = data_path.split(".")
        self._unit_of_measurement = unit_of_measurement
        self._state_mapping = state_mapping

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
        if self.coordinator.data:
            data = self.coordinator.data
            for key in self._data_path:
                if data is not None and key in data:
                    data = data[key]
                else:
                    _LOGGER.error(
                        f"Data path not found: {self._data_path}, coodinator.data: {self.coordinator.data}"
                    )
                    return False  # Data path not found, mark as unavailable
            return True  # Data path found, mark as available
        return False

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"lynk_co_{self._vin}")},
            "name": f"Lynk & Co {self._vin}",
            "manufacturer": "Lynk & Co",
        }

    @property
    def unique_id(self):
        return f"{self._vin}_{self._name}"
