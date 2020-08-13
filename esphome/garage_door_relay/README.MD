## Overview

[ESPHome](https://esphome.io/index.html) configuration and steps used to enable auatomation of Garage Door Motor, Garage Door Open/Close Status, and temperature readings in detached garage.  Integration with Home Assistant via [ESPHome integration](https://www.home-assistant.io/integrations/esphome/).

The ESPHome device was built using a custom board with screw down terminals that has 4 relays built in. [ESPHome Docker](https://esphome.io/guides/getting_started_command_line.html) was utlizied to compile the initial configuration and that was uploaded onto the ESP32 board. The ESP32 board is enclosed in an ABS plastic junction box and is powered via a micro USB cable.  The door sensor from honeywell are made for Garage Doors.


## Parts Used

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [4 Relay ESP32](https://amzn.to/3abd0vG) | 1 | Wi-Fi | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Automated to open / close garage door on location and auto close after specific time intervals |
| [Honeywell Ademco 958 Overhead Door Contacts](https://amzn.to/33CpKZG) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Door Sensor used with ESPHome Relay |
| [Temp Sensor Probe DS18b20](https://amzn.to/3bx9RGF) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/) | Waterproof Temperature sensor, connected directly to ESPHome module |
| [4.7K Ohm Metal Film Resistor](https://amzn.to/3ar95uB) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/) | external pullup resistor |
| [ABS Plastic IP65 Junction Box](https://amzn.to/3asXMCa) | 1 | NA | NA | Junction Box for ESP32 Board and wires |

## GPIO Mapping

| Relay / Input | GPIO Pin | Purpose | Terminals | Terminals Used |
| ------------- | :---: | ------------- | ------------- | ------------- |
| **Relay1** | **GPIO21** | **Garage Door Switch** | NO, C, NC| **NO, C** |
| Relay2 | GPIO22 | Unused | NO, C, NC| Unused |
| Relay3 | GPIO18 | Unused | NO, C, NC| Unused |
| Relay4 | GPIO19 | Unused | NO, C, NC| Unused |
| AN1 | GPIO36 | Unused | AN1+, AN1- | Unused |
| IN1 | GPIO05 | Unused | IN1+, IN1- | Unused |
| **IN2** | **GPIO12** | **Garage Door Sensor** | IN2+, IN2- | **IN2+, IN2-** |
| IN3 | GPIO13 | Unused | IN3+, IN3- | Unused |
| **IN4** | **GPIO14** | **Dallas Temp Sensor (Yellow)** | IN4+, IN4- | **IN4+, 4.7K Ohm Resistor** |
| **3.3V** | NA | **Dallas Temp Sensor (Red)** | 3.3v+ | **3.3v+** |
| **5v** | NA | **Dallas Temp Sensor (Black**) | 5v+, 5v- | **5v-, 4.7K Ohm Resistor** |

## Images
![UI](images/4RelayESP32.jpeg?raw=true "ESP32")

## Home Assistant UI Example
![UI](images/ha-esp32.png?raw=true "HA UI Example")
