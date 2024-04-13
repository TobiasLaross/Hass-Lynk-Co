# Detailed Entities Information

This document provides detailed descriptions and technical specifications for each entity created by the Lynk & Co integration for Home Assistant.

## Sensors

Each sensor's description includes what the sensor measures, its unique entity ID, and additional notes if applicable.

### Lynk & Co 12V Battery
- **Description**: Displays the status of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery`

### Lynk & Co 12V Battery Charge
- **Description**: Shows the charge level of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_charge`

### Lynk & Co 12V Battery Energy Level
- **Description**: Indicates the energy level of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_energy_level`

### Lynk & Co 12V Battery Health
- **Description**: Provides health status of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_health`

### Lynk & Co 12V Battery Power Level
- **Description**: Indicates the power level of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_power_level`

### Lynk & Co 12V Battery Voltage
- **Description**: Displays the voltage of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_voltage`

### Lynk & Co Address
- **Description**: Displays the vehicle's current GPS address in a human-readable format.
- **Entity ID**: `sensor.lynk_co_address`

### Lynk & Co Address Raw
- **Description**: Provides the vehicle's current address in raw data format, potentially useful for integration with mapping services.
- **Entity ID**: `sensor.lynk_co_address_raw`

### Lynk & Co Altitude
- **Description**: Reports the vehicle's current altitude.
- **Entity ID**: `sensor.lynk_co_altitude`

### Lynk & Co Battery
- **Description**: Shows the main battery's charge level as a percentage.
- **Entity ID**: `sensor.lynk_co_battery`

### Lynk & Co Battery Distance
- **Description**: Shows the estimated distance that can be traveled on the current battery power alone.
- **Entity ID**: `sensor.lynk_co_battery_distance`

### Lynk & Co Battery Updated
- **Description**: Timestamp of the last battery status update.
- **Entity ID**: `sensor.lynk_co_battery_updated`

### Lynk & Co Charge State
- **Description**: Displays the current charging state of the vehicle.
- **Entity ID**: `sensor.lynk_co_charge_state`

### Lynk & Co Charger Connection Status
- **Description**: Indicates whether the charger is connected or disconnected.
- **Entity ID**: `sensor.lynk_co_charger_connection_status`

### Lynk & Co Charger Updated
- **Description**: Timestamp of the last charger status update.
- **Entity ID**: `sensor.lynk_co_charger_updated`

### Lynk & Co Climate Updated
- **Description**: Timestamp of the last update to the climate control system.
- **Entity ID**: `sensor.lynk_co_climate_updated`

### Lynk & Co Days To Service
- **Description**: The number of days until the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_days_to_service`

### Lynk & Co Distance To Service
- **Description**: The distance that can be driven before the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_distance_to_service`

### Lynk & Co Door Lock Status
- **Description**: Indicates the current lock status of the vehicle's doors.
- **Entity ID**: `sensor.lynk_co_door_lock_status`

### Lynk & Co Door Lock Updated
- **Description**: Timestamp of the last update to the door lock status.
- **Entity ID**: `sensor.lynk_co_door_lock_updated`

### Lynk & Co Engine Coolant Temperature
- **Description**: Reports the temperature of the engine coolant.
- **Entity ID**: `sensor.lynk_co_engine_coolant_temperature`

### Lynk & Co Engine Hours To Service
- **Description**: The number of engine hours remaining until the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_engine_hours_to_service`

### Lynk & Co Engine Oil Level Status
- **Description**: Shows the current level of the engine oil.
- **Entity ID**: `sensor.lynk_co_engine_oil_level_status`

### Lynk & Co Engine Oil Pressure Status
- **Description**: Indicates the current oil pressure status.
- **Entity ID**: `sensor.lynk_co_engine_oil_pressure_status`

### Lynk & Co Exterior Temperature
- **Description**: Displays the temperature outside the vehicle.
- **Entity ID**: `sensor.lynk_co_exterior_temperature`

### Lynk & Co Exterior Temperature Quality
- **Description**: Quality of the exterior temperature measurement.
- **Entity ID**: `sensor.lynk_co_exterior_temperature_quality`

### Lynk & Co Exterior Temperature Unit
- **Description**: The unit used for the exterior temperature measurement (e.g., Celsius or Fahrenheit).
- **Entity ID**: `sensor.lynk_co_exterior_temperature_unit`

### Lynk & Co Fuel Avg Consumption
- **Description**: The average fuel consumption.
- **Entity ID**: `sensor.lynk_co_fuel_avg_consumption`

### Lynk & Co Fuel Avg Consumption Latest Cycle
- **Description**: The average fuel consumption during the latest cycle.
- **Entity ID**: `sensor.lynk_co_fuel_avg_consumption_latest_cycle`

### Lynk & Co Fuel Distance
- **Description**: The estimated distance that can be traveled with the remaining fuel.
- **Entity ID**: `sensor.lynk_co_fuel_distance`

### Lynk & Co Fuel Level
- **Description**: Displays the current fuel level in liters.
- **Entity ID**: `sensor.lynk_co_fuel_level`

### Lynk & Co Fuel Level Status
- **Description**: Indicates the status of the fuel level.
- **Entity ID**: `sensor.lynk_co_fuel_level_status`

### Lynk & Co Fuel Type
- **Description**: Type of fuel the vehicle uses.
- **Entity ID**: `sensor.lynk_co_fuel_type`

### Lynk & Co Fuel Updated
- **Description**: Timestamp of the last update to the fuel data.
- **Entity ID**: `sensor.lynk_co_fuel_updated`

### Lynk & Co Interior Temperature
- **Description**: Reports the temperature inside the vehicle.
- **Entity ID**: `sensor.lynk_co_interior_temperature`

### Lynk & Co Interior Temperature Quality
- **Description**: Quality of the interior temperature measurement.
- **Entity ID**: `sensor.lynk_co_interior_temperature_quality`

### Lynk & Co Interior Temperature Unit
- **Description**: The unit used for the interior temperature measurement (e.g., Celsius or Fahrenheit).
- **Entity ID**: `sensor.lynk_co_interior_temperature_unit`

### Lynk & Co Last Updated by Car
- **Description**: Timestamp of the last update received directly from the vehicle.
- **Entity ID**: `sensor.lynk_co_last_updated_by_car`

### Lynk & Co Latitude
- **Description**: The latitude component of the vehicle's current position.
- **Entity ID**: `sensor.lynk_co_latitude`

### Lynk & Co Locks Updated
- **Description**: Timestamp of the last update to the lock status.
- **Entity ID**: `sensor.lynk_co_locks_updated`

### Lynk & Co Longitude
- **Description**: The longitude component of the vehicle's current position.
- **Entity ID**: `sensor.lynk_co_longitude`

### Lynk & Co Maintenance Status Updated
- **Description**: Timestamp of the last update to the maintenance status.
- **Entity ID**: `sensor.lynk_co_maintenance_status_updated`

### Lynk & Co Odometer
- **Description**: Measures the total distance the vehicle has traveled in kilometers.
- **Entity ID**: `sensor.lynk_co_odometer`

### Lynk & Co Odometer Miles
- **Description**: Measures the total distance the vehicle has traveled in miles.
- **Entity ID**: `sensor.lynk_co_odometer_miles`

### Lynk & Co Odometer Updated
- **Description**: Timestamp of the last update to the odometer reading.
- **Entity ID**: `sensor.lynk_co_odometer_updated`

### Lynk & Co Position Updated
- **Description**: Timestamp of the last update to the vehicle's position.
- **Entity ID**: `sensor.lynk_co_position_updated`

### Lynk & Co Service Warning Status
- **Description**: Indicates if there is a service warning for the vehicle.
- **Entity ID**: `sensor.lynk_co_service_warning_status`

### Lynk & Co Speed
- **Description**: Displays the current speed of the vehicle.
- **Entity ID**: `sensor.lynk_co_speed`

### Lynk & Co Speed Direction
- **Description**: Indicates the direction of travel when speed was last recorded.
- **Entity ID**: `sensor.lynk_co_speed_direction`

### Lynk & Co Speed Unit
- **Description**: The unit used for speed measurement (e.g., km/h or mph).
- **Entity ID**: `sensor.lynk_co_speed_unit`

### Lynk & Co Speed Updated
- **Description**: Timestamp of the last update to the speed data.
- **Entity ID**: `sensor.lynk_co_speed_updated`

### Lynk & Co 12V Battery Health
- **Description**: Provides health status of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_health`

### Lynk & Co 12V Battery Power Level
- **Description**: Indicates the power level of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_power_level`

### Lynk & Co 12V Battery Voltage
- **Description**: Displays the voltage of the 12V battery.
- **Entity ID**: `sensor.lynk_co_12v_battery_voltage`

### Lynk & Co Address
- **Description**: Displays the vehicle's current GPS address in a human-readable format.
- **Entity ID**: `sensor.lynk_co_address`

### Lynk & Co Address Raw
- **Description**: Provides the vehicle's current address in raw data format, potentially useful for integration with mapping services.
- **Entity ID**: `sensor.lynk_co_address_raw`

### Lynk & Co Altitude
- **Description**: Reports the vehicle's current altitude.
- **Entity ID**: `sensor.lynk_co_altitude`

### Lynk & Co Battery
- **Description**: Shows the main battery's charge level as a percentage.
- **Entity ID**: `sensor.lynk_co_battery`

### Lynk & Co Battery Distance
- **Description**: Shows the estimated distance that can be traveled on the current battery power alone.
- **Entity ID**: `sensor.lynk_co_battery_distance`

### Lynk & Co Battery Updated
- **Description**: Timestamp of the last battery status update.
- **Entity ID**: `sensor.lynk_co_battery_updated`

### Lynk & Co Charge State
- **Description**: Displays the current charging state of the vehicle.
- **Entity ID**: `sensor.lynk_co_charge_state`

### Lynk & Co Charger Connection Status
- **Description**: Indicates whether the charger is connected or disconnected.
- **Entity ID**: `sensor.lynk_co_charger_connection_status`

### Lynk & Co Charger Updated
- **Description**: Timestamp of the last charger status update.
- **Entity ID**: `sensor.lynk_co_charger_updated`

### Lynk & Co Climate Updated
- **Description**: Timestamp of the last update to the climate control system.
- **Entity ID**: `sensor.lynk_co_climate_updated`

### Lynk & Co Days To Service
- **Description**: The number of days until the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_days_to_service`

### Lynk & Co Distance To Service
- **Description**: The distance that can be driven before the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_distance_to_service`

### Lynk & Co Door Lock Status
- **Description**: Indicates the current lock status of the vehicle's doors.
- **Entity ID**: `sensor.lynk_co_door_lock_status`

### Lynk & Co Door Lock Updated
- **Description**: Timestamp of the last update to the door lock status.
- **Entity ID**: `sensor.lynk_co_door_lock_updated`

### Lynk & Co Engine Coolant Temperature
- **Description**: Reports the temperature of the engine coolant.
- **Entity ID**: `sensor.lynk_co_engine_coolant_temperature`

### Lynk & Co Engine Hours To Service
- **Description**: The number of engine hours remaining until the vehicle needs servicing.
- **Entity ID**: `sensor.lynk_co_engine_hours_to_service`

### Lynk & Co Engine Oil Level Status
- **Description**: Shows the current level of the engine oil.
- **Entity ID**: `sensor.lynk_co_engine_oil_level_status`

### Lynk & Co Engine Oil Pressure Status
- **Description**: Indicates the current oil pressure status.
- **Entity ID**: `sensor.lynk_co_engine_oil_pressure_status`

### Lynk & Co Exterior Temperature
- **Description**: Displays the temperature outside the vehicle.
- **Entity ID**: `sensor.lynk_co_exterior_temperature`

### Lynk & Co Exterior Temperature Quality
- **Description**: Quality of the exterior temperature measurement.
- **Entity ID**: `sensor.lynk_co_exterior_temperature_quality`

### Lynk & Co Exterior Temperature Unit
- **Description**: The unit used for the exterior temperature measurement (e.g., Celsius or Fahrenheit).
- **Entity ID**: `sensor.lynk_co_exterior_temperature_unit`

### Lynk & Co Time Until Charged
- **Description**: Provides the estimated time until the battery is fully charged.
- **Entity ID**: `sensor.lynk_co_time_until_charged`

### Lynk & Co Trip Average Speed
- **Description**: The average speed during the current trip.
- **Entity ID**: `sensor.lynk_co_trip_average_speed`

### Lynk & Co Trip Average Speed Last Cycle
- **Description**: The average speed during the last trip cycle.
- **Entity ID**: `sensor.lynk_co_trip_average_speed_last_cycle`

### Lynk & Co Trip Meter
- **Description**: The distance covered during the current trip.
- **Entity ID**: `sensor.lynk_co_trip_meter`

### Lynk & Co Trip Meter2
- **Description**: An additional trip meter measuring the distance covered.
- **Entity ID**: `sensor.lynk_co_trip_meter2`

### Lynk & Co Trip Updated
- **Description**: Timestamp of the last update to trip data.
- **Entity ID**: `sensor.lynk_co_trip_updated`

### Lynk & Co Vehicle Tracker
- **Description**: Tracks the vehicle's geographical location.
- **Entity ID**: `device_tracker.lynk_co_vehicle_tracker`

### Lynk & Co Washer Fluid Level Status
- **Description**: Indicates the current level of the washer fluid.
- **Entity ID**: `sensor.lynk_co_washer_fluid_level_status`

### Vehicle is Running Updated
- **Description**: Timestamp of the last update to the vehicle's running status.
- **Entity ID**: `sensor.vehicle_is_running_updated`
