# Lynk & Co Home Assistant Custom Component

## Introduction
This custom component allows Home Assistant users to integrate and control their Lynk & Co vehicles directly from Home Assistant. It provides the functionality to start and stop the engine, lock and unlock doors, and monitor various vehicle statuses like battery level, fuel level, and climate control status, enhancing the smart home experience with vehicle management.

## Table of Contents
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
- `refresh_tokens`: Refreshes authentication tokens.
- `start_climate` / `stop_climate`: Starts or stops the climate control system.
- `lock_doors` / `unlock_doors`: Locks or unlocks the doors.
- `start_flash_lights` / `stop_flash_lights`: Activates or deactivates hazard lights.
- `start_engine` / `stop_engine`: Starts or stops the engine. (Experimental)
- `manual_update_data`: Manually updates data from the vehicle.

### Entities
Entities created for monitoring and control include:
- Binary sensors for climate control and engine status.
- A lock entity for door control.
- Various sensors for monitoring vehicle condition.

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
