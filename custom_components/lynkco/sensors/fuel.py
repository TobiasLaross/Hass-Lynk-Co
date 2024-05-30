from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel Level",
            "vehicle_record.fuel.level",
            "liters",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel Updated",
            "vehicle_record.fuel.vehicleUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel Level status",
            "vehicle_record.fuel.levelStatus",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel Type",
            "vehicle_record.fuel.fuelType",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel distance",
            "vehicle_record.fuel.distanceToEmpty",
            "km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel avg consumption",
            "vehicle_record.fuel.averageConsumption",
            "L/100km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Fuel avg consumption latest cycle",
            "vehicle_record.fuel.averageConsumptionLatestDrivingCycle",
            "L/100km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Tank Flap Status",
            "vehicle_shadow.vls.tankFlapStatus",
        ),
    ]
    return sensors
