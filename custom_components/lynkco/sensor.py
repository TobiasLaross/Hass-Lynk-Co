from custom_components.lynkco.sensors import seatbelt, tyre
from .const import CONFIG_VIN_KEY, COORDINATOR, DOMAIN
from .sensors import (
    battery,
    bulb,
    charger_status_data,
    climate,
    doors,
    electric_status,
    fuel,
    maintenance_status,
    misc,
    odometer,
    position,
    speed,
    trip,
    windows,
)


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
        + windows.create_sensors(coordinator, vin)
        + misc.create_sensors(coordinator, vin)
        + doors.create_sensors(coordinator, vin)
        + bulb.create_sensors(coordinator, vin)
        + tyre.create_sensors(coordinator, vin)
        + seatbelt.create_sensors(coordinator, vin)
    )
    async_add_entities(all_sensors)
