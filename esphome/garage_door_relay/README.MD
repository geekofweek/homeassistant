## Parts Used

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [4 Relay ESP32](https://amzn.to/3abd0vG) | 1 | Wi-Fi | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Automated to open / close garage door on location and auto close after specific time intervals |
| [Honeywell Ademco 958 Overhead Door Contacts](https://amzn.to/33CpKZG) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Door Sensor used with ESPHome Relay |
| [Temp Sensor Probe DS18b20](https://amzn.to/3bx9RGF) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/) | Waterproof Temperature sensor, connected directly to ESPHome module |
| [4.7K Ohm Metal Film Resistor](https://amzn.to/3ar95uB) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/) | external pullup resistor |

## GPIO Mapping

| Terminal  | GPIO Pin | Purpose | Terminals Used |
| ------------- | :---: | ------------- | ------------- |
| Relay1 | GPIO21 | Garage Door Switch | NO / C |
| Relay2 | GPIO22 | Unused | Unused |
| Relay3 | GPIO18 | Unused | Unused |
| Relay4 | GPIO19 | Unused | Unused |
| AN1 | GPIO36 | Unused | Unused |
| IN1 | GPIO05 | Unused | Unused |
| IN2 | GPIO12 | Garage Door Sensor | IN2+ IN2- |
| IN3 | GPIO13 | Unused | Unused |
| IN4 | GPIO14 | Dallas Temp Sensor (Yellow) | IN4+ / 4.7K Ohm Resistor |
| 3.3V | NA | Dallas Temp Sensor (Red) | 3.3v+ |
| 5v | NA | Dallas Temp Sensor (Black) | 5v- / 4.7K Ohm Resistor |
