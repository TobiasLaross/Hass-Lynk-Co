from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Distance To Service",
            "vehicle_record.maintenanceStatus.distanceToService",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Days To Service",
            "vehicle_record.maintenanceStatus.daysToService",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Engine Hours To Service",
            "vehicle_record.maintenanceStatus.engineHoursToService",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Engine Coolant Temperature",
            "vehicle_record.maintenanceStatus.engineCoolantTemperature",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Service Warning Status",
            "vehicle_record.maintenanceStatus.serviceWarningStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Engine Oil Level Status",
            "vehicle_record.maintenanceStatus.engineOilLevelStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Engine Oil Pressure Status",
            "vehicle_record.maintenanceStatus.engineOilPressureStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Washer Fluid Level Status",
            "vehicle_record.maintenanceStatus.washerFluidLevelStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Maintenance Status Updated",
            "vehicle_record.maintenanceStatus.vehicleUpdatedAt",
        ),
    ]
    return sensors
