from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Speed",
            "vehicle_record.speed.speed",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Speed Unit",
            "vehicle_record.speed.speedUnit",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Speed Direction",
            "vehicle_record.speed.direction",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Speed Updated",
            "vehicle_record.speed.vehicleUpdatedAt",
        ),
    ]
    return sensors
