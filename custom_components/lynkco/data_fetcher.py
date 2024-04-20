import aiohttp
import logging

from .token_manager import get_ccc_token

_LOGGER = logging.getLogger(__name__)

base_url = "https://vehicle-data-tls.aion.connectedcar.cloud/api/v1/vds/vehicles/"
address_base_url = "https://geospatial-locator-tls.aion.connectedcar.cloud/geospatial-locator/api/geocoding/v1/position?"


async def async_fetch_vehicle_address_data(hass, latitude, longitude):
    url = f"{address_base_url}latitude={latitude}&longitude={longitude}"
    return await async_fetch_vehicle_data(hass, url)


async def async_fetch_vehicle_shadow_data(hass, vin):
    url = f"{base_url}{vin}/data/shadow"
    return await async_fetch_vehicle_data(hass, url)


async def async_fetch_vehicle_record_data(hass, vin):
    url = f"{base_url}{vin}/data/record"
    return await async_fetch_vehicle_data(hass, url)


async def async_fetch_vehicle_data(hass, url):
    """Fetch vehicle data using the CCC token."""
    ccc_token = await get_ccc_token(hass)
    if not ccc_token:
        _LOGGER.error("Failed to retrieve CCC token.")
        return None

    headers = {
        "Authorization": f"Bearer {ccc_token}",
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    _LOGGER.error(
                        f"Failed to fetch vehicle data, HTTP status: {response.status}, response: {await response.text()}"
                    )
                    return None
    except Exception as error:
        _LOGGER.error("Exception occurred while fetching vehicle data: %s", str(error))
        return None
