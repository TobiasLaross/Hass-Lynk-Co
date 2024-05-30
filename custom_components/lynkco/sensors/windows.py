from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Driver",
            "vehicle_shadow.vls.windowStatusDriver",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Driver Rear",
            "vehicle_shadow.vls.windowStatusDriverRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Passenger",
            "vehicle_shadow.vls.windowStatusPassenger",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Passenger Rear",
            "vehicle_shadow.vls.windowStatusPassengerRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Sunroof",
            "vehicle_shadow.vls.sunroofOpenStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Window Status Updated",
            "vehicle_shadow.vls.windowStatusDriverUpdatedAt",
        ),
    ]
    return sensors
