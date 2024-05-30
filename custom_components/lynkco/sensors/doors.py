from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door lock status",
            "vehicle_shadow.vls.doorLocksStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Trunk Status",
            "vehicle_shadow.vls.trunkOpenStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Engine Hood Status",
            "vehicle_shadow.vls.engineHoodStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door lock Updated",
            "vehicle_shadow.vls.doorLocksUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Open Status Driver",
            "vehicle_shadow.vls.doorOpenStatusDriver",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Open Status Driver Rear",
            "vehicle_shadow.vls.doorOpenStatusDriverRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Open Status Passenger",
            "vehicle_shadow.vls.doorOpenStatusPassenger",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Open Status Passenger Rear",
            "vehicle_shadow.vls.doorOpenStatusPassengerRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Lock Status Driver",
            "vehicle_shadow.vls.doorLockStatusDriver",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Lock Status Driver Rear",
            "vehicle_shadow.vls.doorLockStatusDriverRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Lock Status Passenger",
            "vehicle_shadow.vls.doorLockStatusPassenger",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Door Lock Status Passenger Rear",
            "vehicle_shadow.vls.doorLockStatusPassengerRear",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Central Locking Updated At",
            "vehicle_shadow.vls.centralLockingUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Sunroof Updated At",
            "vehicle_shadow.vls.sunroofUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Tank Flap Updated At",
            "vehicle_shadow.vls.tankFlapUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Alarm Status Updated At",
            "vehicle_shadow.vls.alarmStatusUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trunk Open Updated At",
            "vehicle_shadow.vls.trunkOpenUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Engine Hood Updated At",
            "vehicle_shadow.vls.engineHoodUpdatedAt",
        ),
    ]
    return sensors
