from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Battery Updated",
            "vehicle_record.electricStatus.vehicleUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Time until charged",
            "vehicle_record.electricStatus.timeToFullyCharged",
            "minutes",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Battery",
            "vehicle_record.electricStatus.chargeLevel",
            "%",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Battery distance",
            "vehicle_record.electricStatus.distanceToEmptyOnBatteryOnly",
            "km",
        ),
    ]
    return sensors
