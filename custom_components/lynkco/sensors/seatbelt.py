from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Driver Seatbelt Status",
            "vehicle_shadow.vrs.seatBeltStatus.driver.fastened",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Driver Rear Seatbelt Status",
            "vehicle_shadow.vrs.seatBeltStatus.driverRear.fastened",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Passenger Seatbelt Status",
            "vehicle_shadow.vrs.seatBeltStatus.passenger.fastened",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Passenger Rear Seatbelt Status",
            "vehicle_shadow.vrs.seatBeltStatus.passengerRear.fastened",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Mid Rear Seatbelt Status",
            "vehicle_shadow.vrs.seatBeltStatus.midRear.fastened",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Seatbelt Status Updated At",
            "vehicle_shadow.vrs.seatBeltStatus.updatedAt",
        ),
    ]
    return sensors
