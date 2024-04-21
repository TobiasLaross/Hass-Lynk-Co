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


class ExpectedStateMonitor:
    def __init__(self):
        self.expected_states = {}
        self.loop_running = False
        self.lock = asyncio.Lock()
        self.state_map = {
            EXPECTED_STATE_ENGINE_ON: (
                "binary_sensor.lynk_co_vehicle_is_running",
                "on",
            ),
            EXPECTED_STATE_ENGINE_OFF: (
                "binary_sensor.lynk_co_vehicle_is_running",
                "off",
            ),
            EXPECTED_STATE_UNLOCKED: ("lock.lynk_co_locks", "unlocked"),
            EXPECTED_STATE_LOCKED: ("lock.lynk_co_locks", "locked"),
            EXPECTED_STATE_CLIMATE_ON: (
                "binary_sensor.lynk_co_pre_climate_active",
                "on",
            ),
            EXPECTED_STATE_CLIMATE_OFF: (
                "binary_sensor.lynk_co_pre_climate_active",
                "off",
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
            entity_id, expected_value = self.state_map[state]
            actual_value = current_states.get(entity_id)
            if actual_value == expected_value:
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
