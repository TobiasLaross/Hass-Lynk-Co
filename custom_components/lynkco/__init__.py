import asyncio
import logging
import voluptuous as vol

from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import (
    async_entries_for_device,
    async_get as async_get_entity_registry,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import config_validation as config_validation

from .expected_state_monitor import ExpectedStateMonitor

from .const import (
    CONFIG_DARK_HOURS_END,
    CONFIG_DARK_HOURS_START,
    CONFIG_EXPERIMENTAL_KEY,
    CONFIG_SCAN_INTERVAL_KEY,
    CONFIG_VIN_KEY,
    COORDINATOR,
    DATA_EXPECTED_STATE,
    DATA_IS_FORCE_UPDATE,
    DATA_STORED_DATA,
    DOMAIN,
    EXPECTED_STATE_CLIMATE_OFF,
    EXPECTED_STATE_CLIMATE_ON,
    EXPECTED_STATE_LOCKED,
    EXPECTED_STATE_UNLOCKED,
    EXPECTED_STATE_ENGINE_ON,
    EXPECTED_STATE_ENGINE_OFF,
    SERVICE_LOCK_DOORS_KEY,
    SERVICE_FORCE_UPDATE_KEY,
    SERVICE_REFRESH_TOKENS_KEY,
    SERVICE_START_CLIMATE_KEY,
    SERVICE_START_ENGINE_KEY,
    SERVICE_START_FLASHLIGHT_KEY,
    SERVICE_START_HONK_FLASH_KEY,
    SERVICE_START_HONK_KEY,
    SERVICE_STOP_CLIMATE_KEY,
    SERVICE_STOP_ENGINE_KEY,
    SERVICE_STOP_FLASHLIGHT_KEY,
    SERVICE_STOP_HONK_KEY,
    SERVICE_UNLOCK_DOORS_KEY,
)
from .data_fetcher import (
    async_fetch_vehicle_shadow_data,
    async_fetch_vehicle_record_data,
    async_fetch_vehicle_address_data,
)
from .remote_control_manager import (
    lock_doors,
    start_climate,
    start_engine,
    start_flash_lights,
    stop_flash_lights,
    start_honk,
    start_honk_flash,
    stop_honk,
    stop_climate,
    stop_engine,
    unlock_doors,
    force_update_data,
)
from .token_manager import refresh_tokens

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: config_validation.empty_config_schema(DOMAIN)}, extra=vol.ALLOW_EXTRA
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a configuration entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if entry.entry_id in hass.data[DOMAIN]:
        # The entry is already set up; possibly due to re-authentication or reload
        _LOGGER.debug(f"Entry {entry.entry_id} is already set up.")
        return True

    expected_state_monitor = ExpectedStateMonitor()
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_IS_FORCE_UPDATE: False,
        DATA_STORED_DATA: {},
        CONFIG_VIN_KEY: entry.data.get(CONFIG_VIN_KEY),
        DATA_EXPECTED_STATE: expected_state_monitor,
    }

    _LOGGER.debug(f"Experimental: {entry.options.get(CONFIG_EXPERIMENTAL_KEY, False)}")
    await setup_data_coordinator(hass, entry)

    entry.async_on_unload(entry.add_update_listener(options_update_listener))
    await register_services(hass, entry)
    await setup_platforms(hass, entry)

    return True


async def options_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""

    update_interval_minutes = max(60, entry.options.get(CONFIG_SCAN_INTERVAL_KEY, 240))
    _LOGGER.debug(f"Will update every: {update_interval_minutes} min")

    # Retrieve and update the coordinator's interval
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    coordinator.update_interval = timedelta(minutes=update_interval_minutes)
    await register_services(hass, entry)
    await coordinator.async_refresh()


async def register_services(hass: HomeAssistant, entry: ConfigEntry):
    """Register or unregister services based on the experimental option."""
    vin = hass.data[DOMAIN][entry.entry_id][CONFIG_VIN_KEY]
    expected_state_monitor: ExpectedStateMonitor = hass.data[DOMAIN][entry.entry_id][
        DATA_EXPECTED_STATE
    ]
    experimental = entry.options.get(CONFIG_EXPERIMENTAL_KEY, False)
    _LOGGER.info(f"Register services using experimental: {experimental}")

    # Define async wrappers for your coroutine service calls
    async def refresh_tokens_service(call):
        await refresh_tokens(hass)

    async def start_climate_service(call):
        climate_level = call.data.get(
            "climate_level",
            "MEDIUM",
        ).upper()
        duration_in_minutes = call.data.get("duration_in_minutes", 15)

        await expected_state_monitor.expect_state(
            EXPECTED_STATE_CLIMATE_ON, hass, entry
        )
        await start_climate(hass, vin, climate_level, duration_in_minutes)

    async def stop_climate_service(call):
        await expected_state_monitor.expect_state(
            EXPECTED_STATE_CLIMATE_OFF, hass, entry
        )
        await stop_climate(hass, vin)

    async def lock_doors_service(call):
        await expected_state_monitor.expect_state(EXPECTED_STATE_LOCKED, hass, entry)
        await lock_doors(hass, vin)

    async def unlock_doors_service(call):
        await expected_state_monitor.expect_state(EXPECTED_STATE_UNLOCKED, hass, entry)
        await unlock_doors(hass, vin)

    async def start_flash_lights_service(call):
        await start_flash_lights(hass, vin)

    async def stop_flash_lights_service(call):
        await stop_flash_lights(hass, vin)

    async def start_honk_service(call):
        await start_honk(hass, vin)

    async def start_honk_flash_service(call):
        await start_honk_flash(hass, vin)

    async def stop_honk_service(call):
        await stop_honk(hass, vin)

    async def force_update_data_service(call):
        await force_update_data(hass, entry)

    async def start_engine_service(call):
        await expected_state_monitor.expect_state(EXPECTED_STATE_ENGINE_ON, hass, entry)
        await start_engine(hass, vin, call.data.get("duration_in_minutes", 15))

    async def stop_engine_service(call):
        await expected_state_monitor.expect_state(
            EXPECTED_STATE_ENGINE_OFF, hass, entry
        )
        await stop_engine(hass, vin)

    # Common services registration
    hass.services.async_register(
        DOMAIN, SERVICE_REFRESH_TOKENS_KEY, refresh_tokens_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_START_CLIMATE_KEY, start_climate_service
    )
    hass.services.async_register(DOMAIN, SERVICE_STOP_CLIMATE_KEY, stop_climate_service)
    hass.services.async_register(DOMAIN, SERVICE_LOCK_DOORS_KEY, lock_doors_service)
    hass.services.async_register(DOMAIN, SERVICE_UNLOCK_DOORS_KEY, unlock_doors_service)
    hass.services.async_register(
        DOMAIN, SERVICE_START_FLASHLIGHT_KEY, start_flash_lights_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_STOP_FLASHLIGHT_KEY, stop_flash_lights_service
    )
    hass.services.async_register(DOMAIN, SERVICE_START_HONK_KEY, start_honk_service)
    hass.services.async_register(
        DOMAIN, SERVICE_START_HONK_FLASH_KEY, start_honk_flash_service
    )
    hass.services.async_register(DOMAIN, SERVICE_STOP_HONK_KEY, stop_honk_service)
    hass.services.async_register(
        DOMAIN, SERVICE_FORCE_UPDATE_KEY, force_update_data_service
    )

    # Experimental services
    if experimental:
        hass.services.async_register(
            DOMAIN, SERVICE_START_ENGINE_KEY, start_engine_service
        )
        hass.services.async_register(
            DOMAIN, SERVICE_STOP_ENGINE_KEY, stop_engine_service
        )
    else:
        await safely_remove_service(hass, DOMAIN, SERVICE_START_ENGINE_KEY)
        await safely_remove_service(hass, DOMAIN, SERVICE_STOP_ENGINE_KEY)


def service_is_registered(hass: HomeAssistant, domain: str, service: str) -> bool:
    """Check if a service is already registered."""
    return service in hass.services.async_services().get(domain, {})


async def safely_remove_service(hass: HomeAssistant, domain: str, service: str):
    """Safely remove a service if it's registered."""
    if service_is_registered(hass, domain, service):
        hass.services.async_remove(domain, service)


async def setup_data_coordinator(hass: HomeAssistant, entry: ConfigEntry):
    update_interval_minutes = max(60, entry.options.get(CONFIG_SCAN_INTERVAL_KEY, 240))
    _LOGGER.debug(f"Will update every: {update_interval_minutes} min")
    """Setup the data update coordinator."""
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{entry.entry_id}_vehicle_data",
        update_method=lambda: update_data(hass, entry),
        update_interval=timedelta(minutes=update_interval_minutes),
        request_refresh_debouncer=Debouncer(hass, _LOGGER, cooldown=10, immediate=True),
    )

    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id][COORDINATOR] = coordinator
    else:
        _LOGGER.error(
            f"Failed to set coordinator for entry {entry.entry_id}, with {DOMAIN} in {hass.data[DOMAIN]}"
        )

    await coordinator.async_config_entry_first_refresh()


async def update_data(hass: HomeAssistant, entry: ConfigEntry):
    """Update vehicle data."""
    vin = hass.data[DOMAIN][entry.entry_id][CONFIG_VIN_KEY]
    is_force_update = hass.data[DOMAIN][entry.entry_id][DATA_IS_FORCE_UPDATE]
    hass.data[DOMAIN][entry.entry_id][DATA_IS_FORCE_UPDATE] = False
    combined_data = hass.data[DOMAIN][entry.entry_id].get(DATA_STORED_DATA, {})
    dark_hours_start = int(entry.options.get(CONFIG_DARK_HOURS_START, 1))
    dark_hours_end = int(entry.options.get(CONFIG_DARK_HOURS_END, 4))
    if not vin:
        _LOGGER.error("Missing VIN for vehicle data update.")
        raise UpdateFailed("Missing VIN.")
    now = datetime.now()
    is_interval_spanning_two_days = dark_hours_end < dark_hours_start
    is_current_time_in_dark_hours = (
        is_interval_spanning_two_days
        and (now.hour >= dark_hours_start or now.hour < dark_hours_end)
    ) or (
        not is_interval_spanning_two_days
        and dark_hours_start <= now.hour < dark_hours_end
    )
    if not is_force_update and (is_current_time_in_dark_hours):
        _LOGGER.debug("Skipping automatic update due to time restrictions.")
        return combined_data

    record, shadow = await asyncio.gather(
        async_fetch_vehicle_record_data(hass, vin),
        async_fetch_vehicle_shadow_data(hass, vin),
    )
    latitude = None
    longitude = None

    if not record:
        _LOGGER.error("Failed to fetch vehicle record data.")
        return combined_data
    else:
        combined_data["vehicle_record"] = record
        if isinstance(record, dict):
            position = record.get("position")
            if isinstance(position, dict):
                latitude = position.get("latitude")
                longitude = position.get("longitude")

    if not shadow:
        _LOGGER.error("Failed to fetch vehicle shadow data.")
        return combined_data
    else:
        combined_data["vehicle_shadow"] = shadow

    address_raw = "Unavailable"
    if latitude is not None and longitude is not None:
        address_response = await async_fetch_vehicle_address_data(
            hass, latitude, longitude
        )
        address = parse_address(address_response)
        if (
            isinstance(address_response, dict)
            and "addressComponents" in address_response
        ):
            address_data = address_response["addressComponents"]
            address_raw = ", ".join(component["longName"] for component in address_data)
    else:
        address = "Unavailable"
        _LOGGER.error("Latitude or longitude not available for address lookup.")

    combined_data["vehicle_address"] = address
    combined_data["vehicle_address_raw"] = address_raw
    hass.data[DOMAIN][entry.entry_id][DATA_STORED_DATA] = combined_data
    return combined_data


def parse_address(address_response):
    # Define the types of address components you are interested in
    desired_types = {
        "street_name": ["route", "street", "road"],  # Street name variations
        "street_number": ["street_number"],  # Street number
        "city": [
            "postal_town",
            "locality",
            "administrative_area_level_2",
        ],  # City variations
    }

    street_name, street_number, city = "", "", ""

    for component in address_response["addressComponents"]:
        for comp_type in component["types"]:
            if comp_type in desired_types["street_name"]:
                street_name = component["longName"]
            elif comp_type in desired_types["street_number"]:
                street_number = component["longName"]
            elif comp_type in desired_types["city"]:
                city = component["longName"]
            if street_name or street_number or city:
                break

    street_address = f"{street_name} {street_number}".strip()
    formatted_address = ", ".join(filter(None, [street_address, city]))

    return formatted_address


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Determine if the device can be safely removed."""
    entity_registry = async_get_entity_registry(hass)

    # Get all entities associated with this device
    entries = async_entries_for_device(
        entity_registry, device_entry.id, include_disabled_entities=True
    )

    # Filter entities that belong to this config entry
    entries = [
        entry for entry in entries if entry.config_entry_id == config_entry.entry_id
    ]

    if entries:
        _LOGGER.debug(
            f"Cannot remove device {device_entry.id} because it has entities: {entries}"
        )
        return False

    _LOGGER.debug(f"Device {device_entry.id} can be safely removed")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a configuration entry."""
    platforms = ["sensor", "binary_sensor", "lock", "device_tracker"]
    unload_ok = await hass.config_entries.async_unload_platforms(entry, platforms)
    if unload_ok:
        # Clean up integration data
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug(f"Unloaded entry {entry.entry_id}")
    else:
        _LOGGER.error(f"Failed to unload entry {entry.entry_id}")
    return unload_ok


async def setup_platforms(hass: HomeAssistant, entry: ConfigEntry):
    """Setup platforms like sensor, lock, etc."""
    platforms = ["sensor", "binary_sensor", "lock", "device_tracker"]
    await hass.config_entries.async_forward_entry_setups(entry, platforms)
