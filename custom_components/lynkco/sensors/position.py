from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Address",
            "vehicle_address",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Latitude",
            "vehicle_record.position.latitude",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Longitude",
            "vehicle_record.position.longitude",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Altitude",
            "vehicle_record.position.altitude",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Position Updated",
            "vehicle_record.position.vehicleUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Address raw",
            "vehicle_address_raw",
        ),
    ]
    return sensors
