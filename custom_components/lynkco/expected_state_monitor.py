import asyncio
import logging
from datetime import datetime, timedelta

from custom_components.lynkco.remote_control_manager import force_update_data

from .const import (
    COORDINATOR,
    DOMAIN,
    EXPECTED_STATE_ENGINE_OFF,
    EXPECTED_STATE_ENGINE_ON,
    EXPECTED_STATE_UNLOCKED,
    EXPECTED_STATE_LOCKED,
    EXPECTED_STATE_CLIMATE_OFF,
    EXPECTED_STATE_CLIMATE_ON,
)


_LOGGER = logging.getLogger(__name__)

LOCKED_STATES = ("DOOR_LOCKS_STATUS_LOCKED", "DOOR_LOCKS_STATUS_SAFE_LOCKED")


def get_data_value(data, data_path):
    """Read a dotted path from the coordinator data, or None if it is missing."""
    for key in data_path.split("."):
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


class ExpectedStateMonitor:
    def __init__(self):
        self.expected_states = {}
        self.loop_running = False
        self.lock = asyncio.Lock()
        # Each expected state maps to the coordinator data path the matching
        # entity reads, and a check of that raw value.
        self.state_map = {
            EXPECTED_STATE_ENGINE_ON: (
                "vehicle_shadow.bvs.engineStatus",
                lambda value: value == "ENGINE_RUNNING",
            ),
            EXPECTED_STATE_ENGINE_OFF: (
                "vehicle_shadow.bvs.engineStatus",
                lambda value: value == "ENGINE_OFF",
            ),
            EXPECTED_STATE_UNLOCKED: (
                "vehicle_shadow.vls.doorLocksStatus",
                lambda value: value is not None and value not in LOCKED_STATES,
            ),
            EXPECTED_STATE_LOCKED: (
                "vehicle_shadow.vls.doorLocksStatus",
                lambda value: value in LOCKED_STATES,
            ),
            EXPECTED_STATE_CLIMATE_ON: (
                "vehicle_record.climate.preClimateActive",
                lambda value: bool(value),
            ),
            EXPECTED_STATE_CLIMATE_OFF: (
                "vehicle_record.climate.preClimateActive",
                lambda value: not value,
            ),
        }

    async def expect_state(self, state, hass, entry):
        """Expect a specific state to be reached and manage the monitoring loop."""
        async with self.lock:
            self.expected_states[state] = datetime.now()
            await self.remove_opposite(state)
            if not self.loop_running:
                self.loop_running = True
                asyncio.create_task(self.monitor_states(hass, entry))

    async def remove_opposite(self, state):
        """Remove the opposite state if present."""
        opposite_states = {
            EXPECTED_STATE_ENGINE_ON: EXPECTED_STATE_ENGINE_OFF,
            EXPECTED_STATE_ENGINE_OFF: EXPECTED_STATE_ENGINE_ON,
            EXPECTED_STATE_UNLOCKED: EXPECTED_STATE_LOCKED,
            EXPECTED_STATE_LOCKED: EXPECTED_STATE_UNLOCKED,
            EXPECTED_STATE_CLIMATE_ON: EXPECTED_STATE_CLIMATE_OFF,
            EXPECTED_STATE_CLIMATE_OFF: EXPECTED_STATE_CLIMATE_ON,
        }

        opposite_state = opposite_states.get(state)
        if opposite_state in self.expected_states:
            _LOGGER.info(f"Removing {opposite_state} since we are expecting {state}")
            del self.expected_states[opposite_state]

    async def monitor_states(self, hass, entry):
        """Monitor expected states and update them continuously."""
        poll_time = 5
        try:
            while True:
                await asyncio.sleep(poll_time)
                await force_update_data(hass, entry)
                coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

                async with self.lock:
                    current_states = coordinator.data
                    if self.check_and_update_states(current_states):
                        break
                poll_time = min(30, poll_time + 10)
        finally:
            self.loop_running = False

    def check_and_update_states(self, current_states):
        """Check and update states based on current data. Return True if monitoring should stop."""
        to_remove = []
        now = datetime.now()
        for state, timestamp in self.expected_states.items():
            data_path, is_reached = self.state_map[state]
            if is_reached(get_data_value(current_states, data_path)):
                _LOGGER.info(f"State {state} reached the expected value.")
                to_remove.append(state)
            elif (now - timestamp) > timedelta(minutes=3):
                _LOGGER.info(
                    f"State {state} has not been reached within the expected time and will be removed."
                )
                to_remove.append(state)

        for state in to_remove:
            del self.expected_states[state]

        return (
            not self.expected_states
        )  # Return True if no states are left, stopping the monitor
