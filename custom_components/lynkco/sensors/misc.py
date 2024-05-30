from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Last updated by car",
            "vehicle_record.updatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Vehicle is running updated",
            "vehicle_shadow.bvs.engineStatusUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Vehicle Alarm Status",
            "vehicle_shadow.vls.alarmStatusData",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co SRS Status",
            "vehicle_shadow.vrs.airbagStatus.srsStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Airbag Status Updated At",
            "vehicle_shadow.vrs.airbagStatus.updatedAt",
        ),
    ]
    return sensors
