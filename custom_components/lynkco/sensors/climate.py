from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Interior Temperature",
            "vehicle_record.climate.interiorTemp.temp",
            "°C",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Interior Temperature Quality",
            "vehicle_record.climate.interiorTemp.Quality",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Interior Temperature Unit",
            "vehicle_record.climate.interiorTemp.Unit",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Climate Updated",
            "vehicle_record.climate.vehicleUpdatedAt",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Exterior temperature",
            "vehicle_record.climate.exteriorTemp.temp",
            "°C",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Exterior Temperature Quality",
            "vehicle_record.climate.exteriorTemp.Quality",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Exterior Temperature Unit",
            "vehicle_record.climate.exteriorTemp.Unit",
        ),
    ]
    return sensors
