from .lynk_co_sensor import LynkCoSensor


def create_sensors(coordinator, vin):
    sensors = [
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Left Turn Any",
            "vehicle_shadow.vms.bulbStatus.leftTurnAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Right Turn Any",
            "vehicle_shadow.vms.bulbStatus.rightTurnAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Low Beam Any",
            "vehicle_shadow.vms.bulbStatus.lowBeamAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Low Beam Left",
            "vehicle_shadow.vms.bulbStatus.lowBeamLeft",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Low Beam Right",
            "vehicle_shadow.vms.bulbStatus.lowBeamRight",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status High Beam Any",
            "vehicle_shadow.vms.bulbStatus.highBeamAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status High Beam Left",
            "vehicle_shadow.vms.bulbStatus.highBeamLeft",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status High Beam Right",
            "vehicle_shadow.vms.bulbStatus.highBeamRight",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Fog Front Any",
            "vehicle_shadow.vms.bulbStatus.fogFrontAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Fog Rear Any",
            "vehicle_shadow.vms.bulbStatus.fogRearAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Stop Any",
            "vehicle_shadow.vms.bulbStatus.stopAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Position Any",
            "vehicle_shadow.vms.bulbStatus.positionAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Day Running Any",
            "vehicle_shadow.vms.bulbStatus.dayRunningAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Trailer Turn Any",
            "vehicle_shadow.vms.bulbStatus.trailerTurnAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Trailer Turn Left Any",
            "vehicle_shadow.vms.bulbStatus.trailerTurnLeftAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Trailer Turn Right Any",
            "vehicle_shadow.vms.bulbStatus.trailerTurnRightAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Trailer Stop Any",
            "vehicle_shadow.vms.bulbStatus.trailerStopAny",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Trailer El Failure",
            "vehicle_shadow.vms.bulbStatus.trailerElFailure",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Multiple",
            "vehicle_shadow.vms.bulbStatus.multiple",
        ),
        LynkCoSensor(
            coordinator,
            vin,
            "Lynk & Co Bulb Status Updated At",
            "vehicle_shadow.vms.bulbStatus.updatedAt",
        ),
    ]
    return sensors
