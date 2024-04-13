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
        car_updated_at=None,
        unit_of_measurement=None,
    ):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._vin = vin
        self._name = name
        self._data_path = data_path.split(".")
        self._car_updated_at_path = (
            car_updated_at.split(".") if car_updated_at else None
        )
        self._unit_of_measurement = unit_of_measurement

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.coordinator.data
        for key in self._data_path:
            if data:
                data = data.get(key)
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

    @property
    def extra_state_attributes(self):
        attributes = {}
        if self._car_updated_at_path:
            data = self.coordinator.data
            for key in self._car_updated_at_path:
                if data:
                    data = data.get(key)
            if data:
                attributes["car_updated_at"] = data
        return attributes
