from .lynk_co_sensor import LynkCoSensor


CHARGER_CONNECTION_STATUS = {
    "CHARGER_CONNECTION_UNSPECIFIED": "Unspecified",
    "CHARGER_CONNECTION_DISCONNECTED": "Disconnected",
    "CHARGER_CONNECTION_CONNECTED_WITHOUT_POWER": "Connected (No Power)",
    "CHARGER_CONNECTION_POWER_AVAILABLE_BUT_NOT_ACTIVATED": "Power Not Activated",
    "CHARGER_CONNECTION_CONNECTED_WITH_POWER": "Connected",
    "CHARGER_CONNECTION_INIT": "Initializing",
    "CHARGER_CONNECTION_FAULT": "Fault",
}

CHARGER_STATE = {
    "CHARGER_STATE_UNSPECIFIED": "Unspecified",
    "CHARGER_STATE_IDLE": "Idle",
    "CHARGER_STATE_PRE_STRT": "Pre-Start",
    "CHARGER_STATE_CHARGN": "Charging",
    "CHARGER_STATE_ALRM": "Alarm",
    "CHARGER_STATE_SRV": "Service",
    "CHARGER_STATE_DIAG": "Diagnostics",
    "CHARGER_STATE_BOOT": "Boot",
    "CHARGER_STATE_RSTRT": "Restart",
}


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Charger connection status",
            "vehicle_shadow.evs.chargerStatusData.chargerConnectionStatus",
            state_mapping=CHARGER_CONNECTION_STATUS,
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Charger Updated",
            "vehicle_shadow.evs.chargerStatusData.updatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Charge state",
            "vehicle_shadow.evs.chargerStatusData.chargerState",
            state_mapping=CHARGER_STATE,
        ),
    ]
    return sensors
