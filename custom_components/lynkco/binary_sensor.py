import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get("vin")
    async_add_entities(
        [
            LynkCoBinarySensor(
                coordinator,
                vin,
                "Pre climate active",
                "vehicle_record.climate.preClimateActive",
                icon="mdi:air-conditioner",
            ),
            LynkCoBinarySensor(
                coordinator,
                vin,
                "Vehicle is running",
                "vehicle_shadow.bvs.engineStatus",
                icon="mdi:engine",
            ),
            LynkCoBinarySensor(
                coordinator,
                vin,
                "Lynk & Co Position is trusted",
                "vehicle_record.position.canBeTrusted",
            ),
        ]
    )


class LynkCoBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(
        self,
        coordinator,
        vin,
        name,
        data_path,
        car_updated_at=None,
        device_class=None,
        icon=None,
    ):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._vin = vin
        self._name = name
        self._data_path = data_path
        self._car_updated_at_path = (
            car_updated_at.split(".") if car_updated_at else None
        )
        self._device_class = device_class
        self._icon = icon
        self._state = None

    @property
    def name(self):
        return f"Lynk & Co {self._name}"

    @property
    def is_on(self):
        if self.coordinator.data:
            data_path = self._data_path.split(".")
            data = self.coordinator.data
            for key in data_path:
                if data is not None and key in data:
                    data = data[key]
                else:
                    return False

            if data == "ENGINE_RUNNING":
                return True
            elif data == "ENGINE_OFF":
                return False
            return bool(data)
        return False

    @property
    def available(self):
        if self.coordinator.data:
            data_path = self._data_path.split(".")
            data = self.coordinator.data
            for key in data_path:
                if data is not None and key in data:
                    data = data[key]
                else:
                    _LOGGER.error(
                        f"Data path not found: {self._data_path}, coodinator.data: {self.coordinator.data}"
                    )
                    return False  # Data path not found, mark as unavailable
            if data != "NO_ENGINE_INFO":
                return True  # Data path found, mark as available
        return False

    @property
    def device_class(self):
        return self._device_class

    @property
    def icon(self):
        return self._icon

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
