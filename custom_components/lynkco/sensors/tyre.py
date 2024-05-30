from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    tyre_sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Driver Front Tyre Pressure",
            "vehicle_shadow.vrs.vehicleTyresStatus.driverFrontTyre.pressure",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Driver Rear Tyre Pressure",
            "vehicle_shadow.vrs.vehicleTyresStatus.driverRearTyre.pressure",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Passenger Front Tyre Pressure",
            "vehicle_shadow.vrs.vehicleTyresStatus.passengerFrontTyre.pressure",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Passenger Rear Tyre Pressure",
            "vehicle_shadow.vrs.vehicleTyresStatus.passengerRearTyre.pressure",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Tyres Status Updated At",
            "vehicle_shadow.vrs.vehicleTyresStatus.updatedAt",
        ),
    ]
    return tyre_sensors
