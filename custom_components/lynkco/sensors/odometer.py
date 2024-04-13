from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Odometer",
            "vehicle_record.odometer.odometerKm",
            "km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Odometer miles",
            "vehicle_record.odometer.odometerMile",
            "miles",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Odometer Updated",
            "vehicle_record.odometer.vehicleUpdatedAt",
        ),
    ]
    return sensors
