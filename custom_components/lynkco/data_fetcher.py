import logging

import aiohttp

from .token_manager import get_ccc_token

_LOGGER = logging.getLogger(__name__)


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
    except Exception as e:
        _LOGGER.error(f"Exception occurred while fetching vehicle data: {e}")
        return None
