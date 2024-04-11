from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta, datetime
import asyncio
import logging
from .const import (
    CONFIG_SCAN_INTERVAL_KEY,
    DOMAIN,
    COORDINATOR,
    SERVICE_LOCK_DOORS_KEY,
    SERVICE_MANUAL_UPDATE_KEY,
    SERVICE_REFRESH_TOKENS_KEY,
    SERVICE_START_CLIMATE_KEY,
    SERVICE_START_FLASHLIGHT_KEY,
    SERVICE_STOP_CLIMATE_KEY,
    SERVICE_STOP_ENGINE_KEY,
    CONFIG_EXPERIMENTAL_KEY,
    CONFIG_VIN_KEY,
    SERVICE_START_ENGINE_KEY,
    SERVICE_STOP_FLASHLIGHT_KEY,
    SERVICE_UNLOCK_DOORS_KEY,
)
from .token_manager import refresh_tokens
from .remote_control_manager import (
    start_climate,
    stop_climate,
    start_engine,
    stop_engine,
    unlock_doors,
    lock_doors,
    stop_flash_lights,
    start_flash_lights,
)
from .data_fetcher import async_fetch_vehicle_data

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a configuration entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "is_manual_update": False,
        "vin": entry.data.get(CONFIG_VIN_KEY),
    }

    _LOGGER.info(f"Experimental: {entry.options.get(CONFIG_EXPERIMENTAL_KEY, False)}")
    await setup_data_coordinator(hass, entry)

    entry.add_update_listener(options_update_listener)
    await register_services(hass, entry)
    await setup_platforms(hass, entry)

    return True


async def options_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""

    update_interval_minutes = entry.options.get(CONFIG_SCAN_INTERVAL_KEY, 60)

    # Retrieve and update the coordinator's interval
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    coordinator.update_interval = timedelta(minutes=update_interval_minutes)
    await register_services(hass, entry)
    await coordinator.async_refresh()


async def register_services(hass: HomeAssistant, entry: ConfigEntry):
    """Register or unregister services based on the experimental option."""
    vin = hass.data[DOMAIN][entry.entry_id][CONFIG_VIN_KEY]
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

        await start_climate(hass, vin, climate_level, duration_in_minutes)

    async def stop_climate_service(call):
        await stop_climate(hass, vin)

    async def lock_doors_service(call):
        await lock_doors(hass, vin)

    async def unlock_doors_service(call):
        await unlock_doors(hass, vin)

    async def start_flash_lights_service(call):
        await start_flash_lights(hass, vin)

    async def stop_flash_lights_service(call):
        await stop_flash_lights(hass, vin)

    async def manual_update_data_service(call):
        await manual_update_data(hass, entry)

    async def start_engine_service(call):
        await start_engine(hass, vin, call.get("duration_in_minutes", 15))

    async def stop_engine_service(call):
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
    hass.services.async_register(
        DOMAIN, SERVICE_MANUAL_UPDATE_KEY, manual_update_data_service
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
    update_interval_minutes = entry.options.get(CONFIG_SCAN_INTERVAL_KEY, 60)
    """Setup the data update coordinator."""
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{entry.entry_id}_vehicle_data",
        update_method=lambda: update_data(hass, entry),
        update_interval=timedelta(seconds=update_interval_minutes),
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
    is_manual_update = hass.data[DOMAIN][entry.entry_id]["is_manual_update"]
    failed_requests = 0
    combined_data = {}
    if not vin:
        _LOGGER.error("Missing VIN for vehicle data update.")
        raise UpdateFailed("Missing VIN.")
    now = datetime.now()
    if not is_manual_update and (1 <= now.hour <= 4):
        _LOGGER.info("Skipping automatic update due to time restrictions.")
        return {}
    record_url = f"https://vehicle-data-tls.aion.connectedcar.cloud/api/v1/vds/vehicles/{vin}/data/record"
    shadow_url = f"https://vehicle-data-tls.aion.connectedcar.cloud/api/v1/vds/vehicles/{vin}/data/shadow"

    record, shadow = await asyncio.gather(
        async_fetch_vehicle_data(hass, record_url),
        async_fetch_vehicle_data(hass, shadow_url),
        return_exceptions=True,
    )

    if isinstance(record, Exception):
        _LOGGER.error("Failed to fetch vehicle record data.")
        failed_requests += 1
    else:
        combined_data["vehicle_record"] = record

    if isinstance(shadow, Exception):
        _LOGGER.error("Failed to fetch vehicle shadow data.")
        failed_requests += 1
    else:
        combined_data["vehicle_shadow"] = shadow

    latitude = (
        combined_data.get("vehicle_record", {}).get("position", {}).get("latitude")
    )
    longitude = (
        combined_data.get("vehicle_record", {}).get("position", {}).get("longitude")
    )

    address_raw = "Unavailable"
    if latitude is not None and longitude is not None:
        address_base_url = "https://geospatial-locator-tls.aion.connectedcar.cloud/geospatial-locator/api/geocoding/v1/position?"
        address_url = f"{address_base_url}latitude={latitude}&longitude={longitude}"
        address_response = await async_fetch_vehicle_data(hass, address_url)
        address = parse_address(address_response)
        if (
            isinstance(address_response, dict)
            and "addressComponents" in address_response
        ):
            address_data = address_response["addressComponents"]
            address_raw = ", ".join(component["longName"] for component in address_data)
    else:
        address = "Unavailable"
        failed_requests += 1
        _LOGGER.error("Latitude or longitude not available for address lookup.")

    combined_data["vehicle_address"] = address
    combined_data["vehicle_address_raw"] = address_raw
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


async def manual_update_data(hass: HomeAssistant, entry: ConfigEntry):
    """Trigger a manual data update, bypassing the time check."""
    hass.data[DOMAIN][entry.entry_id]["is_manual_update"] = True
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    await coordinator.async_request_refresh()
    hass.data[DOMAIN][entry.entry_id]["is_manual_update"] = False


async def setup_platforms(hass: HomeAssistant, entry: ConfigEntry):
    """Setup platforms like sensor, lock, etc."""
    for platform in ["sensor", "binary_sensor", "lock", "device_tracker"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
