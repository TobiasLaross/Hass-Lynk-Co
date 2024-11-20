import logging

from homeassistant.components.lock import LockEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN
from .remote_control_manager import lock_doors, unlock_doors

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get("vin")
    async_add_entities(
        [
            LynkCoLock(
                hass,
                coordinator,
                vin,
                "Lynk & Co Locks",
                "vehicle_shadow.vls.doorLocksStatus",
            ),
        ]
    )


class LynkCoLock(CoordinatorEntity, LockEntity):
    def __init__(self, hass, coordinator, vin, name, data_path, car_updated_at=None):
        super().__init__(coordinator)
        self._data_path = data_path.split(".")
        self._hass = hass
        self._vin = vin
        self._name = name
        self._state = None
        self._car_updated_at_path = (
            car_updated_at.split(".") if car_updated_at else None
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"lynk_co_{self._vin}")},
            manufacturer="Lynk & Co",
            name=f"Lynk & Co {self._vin}",
        )

    @property
    def name(self):
        return f"{self._name}"

    @property
    def is_locked(self):
        data = self.coordinator.data
        for key in self._data_path:
            if data is not None and key in data:
                data = data[key]
            else:
                return None
        return (
            data == "DOOR_LOCKS_STATUS_LOCKED"
            or data == "DOOR_LOCKS_STATUS_SAFE_LOCKED"
        )

    async def async_lock(self, **kwargs):
        """Lock the vehicle."""
        await lock_doors(self._hass, self._vin)

    async def async_unlock(self, **kwargs):
        """Unlock the vehicle."""
        await unlock_doors(self._hass, self._vin)

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
                    return False
            return data != "NO_ENGINE_INFO"
        return False

    @property
    def unique_id(self):
        return f"{self._name}_{self._vin}"

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
