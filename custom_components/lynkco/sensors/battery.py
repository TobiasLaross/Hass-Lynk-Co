from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery",
            "vehicle_record.battery.chargeLevel",
            "%",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery Charge",
            "vehicle_record.battery.charge",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery Health",
            "vehicle_record.battery.health",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery Power level",
            "vehicle_record.battery.powerLevel",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery Energy level",
            "vehicle_record.battery.energyLevel",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co 12V Battery Voltage",
            "vehicle_record.battery.voltage",
        ),
    ]
    return sensors
