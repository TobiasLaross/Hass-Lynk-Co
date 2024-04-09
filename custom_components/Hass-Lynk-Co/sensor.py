from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import CONFIG_VIN_KEY, DOMAIN, COORDINATOR
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get(CONFIG_VIN_KEY)
    async_add_entities(
        [
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Odometer",
                "vehicle_record.odometer.odometerKm",
                "vehicle_record.odometer.vehicleUpdatedAt",
                "km",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Battery",
                "vehicle_record.electricStatus.chargeLevel",
                "vehicle_record.electricStatus.vehicleUpdatedAt",
                "%",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Fuel Level",
                "vehicle_record.fuel.level",
                "vehicle_record.fuel.vehicleUpdatedAt",
                "liters",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Fuel Level status",
                "vehicle_record.fuel.levelStatus",
                "vehicle_record.fuel.vehicleUpdatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Fuel distance",
                "vehicle_record.fuel.distanceToEmpty",
                "vehicle_record.fuel.vehicleUpdatedAt",
                "km",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Time until charged",
                "vehicle_record.electricStatus.timeToFullyCharged",
                "vehicle_record.electricStatus.vehicleUpdatedAt",
                "minutes",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Battery distance",
                "vehicle_record.electricStatus.distanceToEmptyOnBatteryOnly",
                "vehicle_record.electricStatus.vehicleUpdatedAt",
                "km",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Interior temperature",
                "vehicle_record.climate.interiorTemp.temp",
                "vehicle_record.climate.vehicleUpdatedAt",
                "°C",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Exterior temperature",
                "vehicle_record.climate.exteriorTemp.temp",
                "vehicle_record.climate.vehicleUpdatedAt",
                "°C",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Charger connection status",
                "vehicle_shadow.evs.chargerStatusData.chargerConnectionStatus",
                "vehicle_shadow.evs.chargerStatusData.updatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Charge state",
                "vehicle_shadow.evs.chargerStatusData.chargerState",
                "vehicle_shadow.evs.chargerStatusData.updatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Address",
                "vehicle_address",
                "vehicle_record.position.vehicleUpdatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Address raw",
                "vehicle_address_raw",
                "vehicle_record.position.vehicleUpdatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Door lock status",
                "vehicle_shadow.vls.doorLocksStatus",
                "vehicle_shadow.vls.doorLocksUpdatedAt",
                "",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Last updated by car",
                "vehicle_record.updatedAt",
                "",
            ),
        ]
    )


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
