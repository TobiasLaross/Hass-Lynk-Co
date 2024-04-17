from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Charger connection status",
            "vehicle_shadow.evs.chargerStatusData.chargerConnectionStatus",
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
        ),
    ]
    return sensors
