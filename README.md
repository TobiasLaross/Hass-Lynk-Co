# Lynk & Co Home Assistant Custom Component

## :warning: **Warning**: Use of this integration with Lynk & Co's services might lead to your account being blocked. Use at your own risk.

## Introduction
This custom component allows Home Assistant users to integrate and control their Lynk & Co vehicles directly from Home Assistant.
It provides the functionality for multiple users to control pre climate and sensor monitoring.
An experimental service to start and stop the engine is included as well as lock and unlock doors, and monitor various vehicle
statuses like battery level, fuel level, and climate control status, enhancing the smart home experience with vehicle management.
This has been tested on european models only.

## Table of Contents
- [Warning](#warning-warning)
- [Introduction](#introduction)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Adding the Custom Repository to HACS](#adding-the-custom-repository-to-hacs)
  - [Installing the Integration](#installing-the-integration)
- [Configuration](#configuration)
  - [Initial Setup](#initial-setup)
- [Features and Usage](#features-and-usage)
  - [Services](#services)
  - [Entities](#entities)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Installation

### Prerequisites
Before installing this component, make sure you have:
- Home Assistant running.
- Access to your Lynk & Co account credentials.
- Your vehicle's VIN.

### Adding the Custom Repository to HACS
1. Navigate to HACS in Home Assistant.
2. Go to "Integrations".
3. Click on the three dots in the top right corner and select "Custom repositories".
4. Enter the URL of this GitHub repository.
5. Select "Integration" in the "Category" dropdown.
6. Click "Add".

### Installing the Integration
1. Find the Lynk & Co integration in the HACS Integrations section and click "Install".
2. Restart Home Assistant.

## Configuration
Configure this integration through the Home Assistant UI.

### Initial Setup
1. Navigate to Configuration > Integrations in Home Assistant.
2. Click on "Add Integration" and search for "Lynk & Co".
3. Follow the on-screen instructions to enter your vehicle details and complete the setup.

## Features and Usage

### Services
This component offers various services to interact with your vehicle, including:
- `start_climate` / `stop_climate`: Starts or stops the climate control system.
- `lock_doors` / `unlock_doors`: Locks or unlocks the doors.
- `start_flash_lights` / `stop_flash_lights`: Activates or deactivates hazard lights.
- `start_engine` / `stop_engine`: Starts or stops the engine. (Note: This feature is experimental and undocumented by Lynk & Co.)
- `force_update_data`: Forcing update data from the vehicle, bypassing night limit.
- `refresh_tokens`: Refreshes authentication tokens, this should not be needed, handled automatically.

#### Detailed Service Information

- **start_engine / stop_engine**: This service allows you to remotely start or stop your vehicle's engine. It's an experimental feature not officially supported by the Lynk & Co app.
Use with caution, as it may not always perform as expected. My observations are that the EV engine will be started and climate will be set to HI, this service have not been tested without sufficient EV battery.

### Entities
The integration creates entities for comprehensive monitoring and control of the Lynk & Co vehicle, including both sensors and binary sensors.

#### Sensors
Sensors provide detailed information about various aspects of the vehicle's status and environment. These include:

- **Lynk & Co Odometer**: Measures the total distance the vehicle has traveled in kilometers.
- **Lynk & Co Battery**: Shows the current battery charge level as a percentage.
- **Lynk & Co Fuel Level**: Displays the current fuel level in liters.
- **Lynk & Co Fuel Level Status**: Indicates the status of the fuel level.
- **Lynk & Co Fuel Distance**: Reports the estimated distance (in kilometers) that can be traveled with the remaining fuel.
- **Lynk & Co Time Until Charged**: Provides the estimated time (in minutes) until the battery is fully charged.
- **Lynk & Co Battery Distance**: Shows the estimated distance (in kilometers) that can be traveled on battery power alone.
- **Lynk & Co Interior Temperature**: Reports the temperature inside the vehicle in degrees Celsius.
- **Lynk & Co Exterior Temperature**: Displays the temperature outside the vehicle in degrees Celsius.
- **Lynk & Co Charger Connection Status**: Indicates whether the charger is connected or disconnected.
- **Lynk & Co Charge State**: Shows the current charging state of the vehicle.
- **Lynk & Co Address**: Displays the vehicle's current address in a human-readable format.
- **Lynk & Co Address Raw**: Provides the vehicle's current address in a format that includes raw data, potentially useful for integration with mapping services.
- **Lynk & Co Door Lock Status**: Indicates the current lock status of the vehicle's doors.
- **Lynk & Co Last Updated by Car**: Timestamp of the last update received from the vehicle.

#### Binary Sensors
Binary sensors indicate specific vehicle states that have a true or false condition. These include:

- **Pre Climate Active**: Indicates whether the pre-climate control system is active, ensuring the vehicle's interior is at a comfortable temperature before you enter. It uses the icon `mdi:air-conditioner` to visually represent this feature in the Home Assistant UI.
- **Vehicle is Running**: Shows if the vehicle's engine is currently running. This sensor is crucial for understanding the immediate operational state of your vehicle and uses the `mdi:engine` icon for easy identification.

For a comprehensive list of all entities, including detailed descriptions and additional sensors, please refer to [Detailed Entities Information](entities.md).

## Troubleshooting

- **2FA Code Issues**: Ensure the code is entered correctly and within its validity period. Generate a new code if issues persist.
- **Connection Issues**: Check that your vehicle is in an area with good cellular reception and that your Lynk & Co account is active and not facing any service disruptions.

## Contributing
Contributions are welcome! You can contribute by reporting issues, suggesting features, or submitting pull requests. Please adhere to existing coding standards and commit message guidelines.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Thanks to everyone who has contributed to this project by reporting issues, suggesting features, or submitting pull requests.
- Appreciation to the Home Assistant community for their continuous support and contributions to the ecosystem.
