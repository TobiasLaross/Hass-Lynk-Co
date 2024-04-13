from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trip Average Speed",
            "vehicle_record.trip.avgSpeed",
            "km/h",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trip Average Speed Last Cycle",
            "vehicle_record.trip.avgSpeedLastDrivingCycle",
            "km/h",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trip Meter",
            "vehicle_record.trip.tripMeter",
            "km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trip Meter2",
            "vehicle_record.trip.tripMeter2",
            "km",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Trip Updated",
            "vehicle_record.trip.vehicleUpdatedAt",
        ),
    ]
    return sensors
