from .const import CONFIG_VIN_KEY, COORDINATOR, DOMAIN
from .sensors import (battery, charger_status_data, climate, electric_status,
                      fuel, maintenance_status, odometer, position, speed,
                      trip)
from .sensors.lynk_co_sensor import LynkCoSensor


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get(CONFIG_VIN_KEY)
    all_sensors = (
        battery.create_sensors(coordinator, vin)
        + charger_status_data.create_sensors(coordinator, vin)
        + climate.create_sensors(coordinator, vin)
        + trip.create_sensors(coordinator, vin)
        + speed.create_sensors(coordinator, vin)
        + odometer.create_sensors(coordinator, vin)
        + maintenance_status.create_sensors(coordinator, vin)
        + fuel.create_sensors(coordinator, vin)
        + electric_status.create_sensors(coordinator, vin)
        + position.create_sensors(coordinator, vin)
        + [
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Door lock status",
                "vehicle_shadow.vls.doorLocksStatus",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Door lock Updated",
                "vehicle_shadow.vls.doorLocksUpdatedAt",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Last updated by car",
                "vehicle_record.updatedAt",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Vehicle is running updated",
                "vehicle_shadow.bvs.engineStatusUpdatedAt",
            ),
            LynkCoSensor(
                coordinator,
                vin,
                "Lynk & Co Locks Updated",
                "vehicle_shadow.vls.doorLocksUpdatedAt",
            ),
        ]
    )
    async_add_entities(all_sensors)
