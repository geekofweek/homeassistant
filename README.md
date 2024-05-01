[![GitHub stars](https://img.shields.io/github/stars/geekofweek/homeassistant.svg?style=plasticr)](https://github.com/geekofweek/homeassistant/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/geekofweek/homeassistant.svg?style=plasticr)](https://github.com/geekofweek/homeassistant/commits/master)
[![HA Version](https://img.shields.io/badge/Running%20Home%20Assistant-2024.5.0%20-darkblue)](https://github.com/home-assistant/home-assistant/releases/latest)
[![HA Version](https://img.shields.io/badge/Original%20Home%20Assistant-0.14%20-darkblue)](https://github.com/home-assistant/core/releases/0.14)
[![HA Community](https://img.shields.io/badge/HA%20community-forum-orange)](https://community.home-assistant.io/u/geekoftheweek/summary)


# Overview
My personal [Home Assistant Container](https://home-assistant.io) configurations with 300+ automations.  These are my active automations and configurations that I use every day.  Updated frequently as I add more devices and come up with more and more complicated ways to do simple tasks.

# <a name="menu">Menu</a>
 | [Hubs](#hubs) | [Lighting](#lighting) | [Climate](#climate)| [Outlets & Switches](#outlets)|  [Locks](#locks) | [Security](#security) | [Voice Assistant](#voice) | [Media](#media) | [Sensors](#sensors) | [Cameras](#cameras) | [Garage](#garage) | [Vacuum](#vacuum) | [Blinds](#blinds) | [Energy](#energy) | [Appliances](#appliances) | [Network](#network) | [Other Hardware](#other) | [Software](#software) | [Retired Devices](#retired)  | [Screenshots](#screenshots) |

## <a name="hubs">Hubs</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [SONOFF Zigbee 3.0 USB Dongle Plus-E](https://amzn.to/3oLXD9z) | 1 | USB | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Used to control all Zigbee smart bulbs and Blinds.  ZHA was becoming un-reliable for me so switched to Zigbee2MQTT |
| [Aeotec Z-Stick 7](https://amzn.to/3xQXuA4)| 1 | USB | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Used to control all Z-Wave Devices.  Integrated via zwavejs2mqtt container |
| [Lutron Smart Bridge 2 Pro](https://amzn.to/2WLpKEF)| 1 | Ethernet | [Lutron Caséta](https://www.home-assistant.io/integrations/lutron_caseta) | Controls Lutron Caseta light switches, dimmers, and Pico remotes |
| [Bond Home](https://amzn.to/3i7dLds)| 1 | Wi-Fi | [Bond Home](https://www.home-assistant.io/integrations/bond/) | Controls ceiling fans and lights via RF remote control commands.  Existing fans are each wired to a single switch that controls both power and light with fan and light controls done via a physical remote.  The Bond Home Hub allowed for sending of those RF remote commands via the hub and the local API makes it possible to send said commands from Home Assistant. |


Relevant hub configurations can be found within [configuration.yaml](https://github.com/geekofweek/homeassistant/blob/master/configuration.yaml)

## <a name="lighting">Lighting</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Philips Hue White and Color Ambiance](https://amzn.to/2Ip8waU) | 7 | Zigbee | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Color changing smart bulbs|
| [Philips Hue White and Color Ambiance LightStrip Plus Dimmable](https://amzn.to/2Kx27qF) | 1 | Zigbee | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Color changing smart led strip. Used as accent lighting|
| [Philips Hue White](https://amzn.to/2LaUFTd) | 9 | Zigbee | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Non color changing smart bulbs|
| [Cree Connected](https://amzn.to/2IpKAnZ) | 9 | Zigbee | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Non color changing smart bulbs|
| [Lutron Caseta Wireless Dimmer](https://amzn.to/2KwDJWc) | 17 | Lutron Clear Connect | [Lutron Caséta](https://www.home-assistant.io/integrations/lutron_caseta) | Smart dimmer switches that do not require a neutral wire|
| [Lutron Caseta Wireless Lighting Switch](https://amzn.to/2YvDWjg) | 2 | Lutron Clear Connect | [Lutron Caséta](https://www.home-assistant.io/integrations/lutron_caseta) | Smart on / off light switches |
| [Lutron Caseta Pico Wireless Dimmer Switch](https://amzn.to/2Etw0HP) | 6 | Lutron Clear Connect | [Lutron Caséta](https://www.home-assistant.io/integrations/lutron_caseta) | Decora wall mountable remote (that looks like a dimmer switch). Controls various lights |
| [Lutron Aurora Smart Bulb Dimmer](https://amzn.to/2OyI0PI) | 4 | Zigbee | [Zigbee2MQTT](https://www.home-assistant.io/integrations/mqtt/) | Smart Dimmer that attaches to existing Toggle light Switch. |
| [LIFX Mini White](https://amzn.to/2UFDvmh) | 1 | Wi-Fi| [LIFX](https://www.home-assistant.io/integrations/lifx/) | Non color changing Wi-Fi smart bulbs.  Used in places where Zigbee is not reliable (detached garage) |
| [Philips Color A19](https://amzn.to/3Sk1sfe) | 7 | Wi-Fi| [WiZ](https://www.home-assistant.io/integrations/wiz/) | Color changing Wi-Fi smart bulb. Used for various lights in place of Zigbee, which has not been the most reliable protocol for me. |

Many of my automations rely on some form of lighting but many examples can be found in [lights.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/lights.yaml) and [location.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml).


## <a name="climate">Climate</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ecobee 3](https://amzn.to/2L72d9A) | 1 | Wi-Fi | [ecobee](https://www.home-assistant.io/components/ecobee/) / [Ecobee Thermostat](https://www.home-assistant.io/components/climate.ecobee/) | Used as primary thermostat |
| [Ecobee Room Sensor](https://amzn.to/2L9cORm) | 9 | Ecobee3 | [Ecobee Binary Sensor](https://www.home-assistant.io/components/binary_sensor.ecobee/) | Provides room temperature and room occupancy.|
| [Dyson Pure Hot + Cool Link](https://amzn.to/2RQjDtR) | 1 | Wi-Fi | [Dyson](https://github.com/shenxn/ha-dyson/) (Custom Component) | Dyson Fan with Heater and Air Purifier|
| [Temp Sensor Probe DS18b20](https://amzn.to/3bx9RGF) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/) | Waterproof Temperature sensor, connected directly to ESPHome module |

I utilize a number of automations that adjust climate controls.  Mostly they can be found in [climate.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/climate.yaml). Ecobee room sensors are heavily used in [occupancy.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/occupancy.yaml) and as conditions in many automations

More detailed information on the ESPhome configuration can be found in [here](https://github.com/geekofweek/homeassistant/tree/master/esphome/garage_door_relay)

## <a name="outlets">Outlets & Switches</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Wemo Mini Smart Plug](https://amzn.to/2wQ05jE) | 3 | Wi-Fi | [Belkin WeMo](https://www.home-assistant.io/components/wemo/) | Smart outlets utilized to control various devices via powering the outlet on/off (fans, Christmas Tree, etc).  These are slowly being phased out |
| [GE Z-Wave Wireless Smart Lighting Control Outdoor Module](https://amzn.to/2KuFRxN) | 4 | Z-Wave| [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Used to control low voltage outdoor lighting transformers, bug zapper, and Christmas lights (Holiday time only) |
| [Remotec Zwave Dry Contact Fixture Module](https://amzn.to/2rOmcBW) | 1 | Z-Wave| [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Used to control gas fireplace |
| [Dome Home Automation Water Shut-Off Valve](https://amzn.to/2IzJR1J) | 1 | Z-Wave| [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Used to shut off Water Main Supply to House in the event of water leak detected or while on Vacation |
| [Kasa Outdoor Smart Plug](https://amzn.to/3JFdn5W) | 1 | Wi-Fi | [TP-Link Kasa Smart](https://www.home-assistant.io/integrations/tplink/) | Used to control outdoor devices, fountain pump, etc. |
| [Kasa Smart Plug Mini with Energy Monitoring](https://amzn.to/3quAo48) | 2 | Wi-Fi | [TP-Link Kasa Smart](https://www.home-assistant.io/integrations/tplink/) | Used to control charging and power monitoring of electric bikes |
| [Kasa Smart Plug Mini](https://www.amazon.com/dp/B091FXLMS8/ref=cm_sw_r_as_gl_api_gl_i_XTMKH4J7T66JNP11Z60N?linkCode=ml1&tag=homeassistant-20) | 4 | Wi-Fi | [TP-Link Kasa Smart](https://www.home-assistant.io/integrations/tplink/) | Used to control various devices, slowing phasing out Wemo in favor of these |
| [Kasa Smart Plug Power Strip](https://amzn.to/3rlYajd) | 3 | Wi-Fi | [TP-Link Kasa Smart](https://www.home-assistant.io/integrations/tplink/) | Used to control various devices with energy monitoring |


Switches and outlets are used in various capacities, some are for lighting and some are for fans type devices.  [lights.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/lights.yaml) should have some good examples.


## <a name="locks">Locks</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Schlage Connect Touchscreen Deadbolt](https://amzn.to/2KwXltd) | 3 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Smart locks used in automations to auto lock / unlock doors |

Locks are used mostly as a way to lock / unlock doors based on locations, see [location.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and [locks.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/locks.yaml) for some examples

## <a name="security">Security</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [GoControl Door/Window Sensor](https://amzn.to/2wOhLfn) | 3 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Door sensors to detect if exterior doors have been opened / closed |
| [GoControl Siren and Strobe](https://amzn.to/2k4bK4U) | 1 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Alarm used for when alarm is triggered or when you want to get someone's attention|

Door sensors, motion sensors, and the alarm siren are used in many different ways via [alarm.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/alarm.yaml).  I've also implemented some of the alarm functions as part of [water_works.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/water_works.yaml).

## <a name="voice">Voice Assistant</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Amazon Echo](https://amzn.to/2KuPHjd) | 1 | Wi-Fi | [Home Assistant Cloud](https://www.home-assistant.io/cloud/) | Audio only Voice Assistant |
| [Amazon Echo Dot](https://amzn.to/2wSreSW) | 7 | Wi-Fi | [Home Assistant Cloud](https://www.home-assistant.io/cloud/) | Audio only Voice Assistant |
| [Amazon Echo Spot](https://amzn.to/2rOVZ6a) | 1 | Wi-Fi | [Home Assistant Cloud](https://www.home-assistant.io/cloud/) | Voice Assistant with small display |
| [Amazon Echo Show](https://amzn.to/2rRhN0n) | 1 | Wi-Fi | [Home Assistant Cloud](https://www.home-assistant.io/cloud/) |Voice Assistant with display |
| [Amazon Echo Show 5](https://amzn.to/3sPEh09) | 1 | Wi-Fi | [Home Assistant Cloud](https://www.home-assistant.io/cloud/) |Voice Assistant with display 

I go for native Echo integration wherever possible, but a few devices are not currently supported where I've had to implement some work arounds via Home Assistant Cloud (previously Emulated Hue).  Most of these are just exposed via an [input_boolean]( https://github.com/geekofweek/homeassistant/blob/master/input_boolean.yaml) and [customize.yaml]( https://github.com/geekofweek/homeassistant/blob/master/customize.yaml).  This allows the ability to have echo turn on or off an [input_boolean]( https://github.com/geekofweek/homeassistant/blob/master/input_boolean.yaml)  in turn triggering an automation.

I also utilized the [Amazon Alexa Media Player Custom Component](https://github.com/custom-components/alexa_media_player), mostly to pick up the timers into Home Assistant

## <a name="media">Media</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Apple TV 4k](https://amzn.to/3FugTN4) | 6 | Wi-Fi | [Apple TV](https://www.home-assistant.io/components/apple_tv/) | Used for media playback on 4k TVs |
| [Sonos Arc](https://amzn.to/3xb9JY1) | 1 | Ethernet |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | TV Soundbar for audio playback and Home Assistant TTS. |
| [Sonos Sub](https://amzn.to/3lgO5iB) | 1 | Ethernet | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS |
| [Sonos Play:1](https://amzn.to/2IrsIor) | 10 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS |
| [Sonos One SL](https://amzn.to/37aXQqa) | 2 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS |
| [Sonos Move](https://amzn.to/2mJ0mAk) | 2 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Portable Audio playback and Home Assistant TTS |
| [Sonos Roam](https://amzn.to/3zZHU6v) | 1 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Portable Audio playback and Home Assistant TTS |
| [Sonos Beam](https://amzn.to/3mWzhCM) | 2 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | TV Soundbar for Audio playback and Home Assistant TTS |
| [Sonos Port](https://amzn.to/3bnJyn8) | 1 | Ethernet |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS. Connects Sonos to existing surround sound system |
| [Sonos Connect:AMP](https://amzn.to/2rQ0XzM) | 1 | Wi-Fi |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS. Connects Sonos to outdoor speakers |
| [Lutron Caseta Pico Remote Control for Audio](https://amzn.to/2QsBtnj) | 3 | Lutron Clear Connect | [Lutron Caséta](https://www.home-assistant.io/integrations/lutron_caseta) | Decora wall mountable remote. Used to control Sonos |
| [Logitech Harmony Hub](https://amzn.to/2IuEvlS) | 3 | Wi-Fi | [Harmony Hub Remote](https://www.home-assistant.io/components/remote.harmony/) | Controls various AV equipment and other devices that utilize infrared remotes |
| [Samsung QN75Q80TA](https://amzn.to/3qzvOx7) | 1 | Wi-Fi | [Samsung Smart TV](https://www.home-assistant.io/integrations/samsungtv/) | 75" 4K QLED TV |
| [LG OLED55BXPUA](https://amzn.to/36THinl) | 1 | Wi-Fi | [LG webOS Smart TV](https://www.home-assistant.io/integrations/webostv/) | 55" 4K OLED TV |
| [Plex Media Server](https://plex.tv) | 1 | Ethernet | [Plex](https://www.home-assistant.io/components/media_player.plex) / [Plex Activity Monitor](https://www.home-assistant.io/components/sensor.plex/) |  Media Server|  

Most media player based automations can be found in [media.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/media.yaml) and some Text to Speech (TTS) based automation in various automations.

Harmony Hubs work via a combination of [input_selects]( https://github.com/geekofweek/homeassistant/blob/master/input_select.yaml), [scripts]( https://github.com/geekofweek/homeassistant/blob/master/scripts.yaml), and automations in [media.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/media.yaml).

## <a name="sensors">Sensors</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Nest Protect v2 Battery](https://amzn.to/2LJ0ACn) | 6 | Wi-Fi | [Nest](https://www.home-assistant.io/components/nest/) | Smoke Alarm and CO Alarm.  I realized most of my Smoke Alarms had long suprased the 10 year mark and it was time for some replacements. I usually avoid Google owned products for various reasons, but the Nest Protect line has high praise. |
| [Dome Motion Detector - Light Sensor](https://amzn.to/2W9TMDS) | 8 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Motion and Light Level sensor used to automate around motion events and current room brightness. |
| [GoControl PIR Motion Detector](https://amzn.to/2HCvyZJ) | 1 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Motion sensor used to automate around motion events. |
| [ZOOZ 4-in-1 Sensor ZSE40](https://amzn.to/3aTqGhZ) | 5 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Motion,temperature, humidity, and light level sensor used to automate around motion events. |
| [Dome Home Automation Leak Sensor](https://amzn.to/2IA5XBj) | 8 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Water sensors used to detect the pressence of water as a preventive measure |
| [Aeon Labs Water Sensor](https://amzn.to/2rM6KFE) | 2 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Water sensors used to detect the pressence of water as a preventive measure |
| [Ecolink Door/Window Sensor](https://amzn.to/3cCjhUU) | 2 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Trial run on Window sensors to stop my blinds from closing when a Window is Open.  Starting small but we all know how that will end up.  ALL THE WINDOWS! |
| [Flume v2](https://amzn.to/3zx6grj) | 2 | Wi-Fi | [Flume](https://www.home-assistant.io/integrations/flume/) | Monitors whole house water consumption based on water meter useage |

Water sensors serve one major function, to alert me to the presence of water.  Almost all of those automations can be fond via [water_works.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/water_works.yaml)

## <a name="cameras">Cameras</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ring Video Doorbell 3 Plus](https://amzn.to/34ysSWV) | 1 | Wi-Fi | [Ring](https://www.home-assistant.io/components/ring/) / [Ring Binary Sensor](https://www.home-assistant.io/components/binary_sensor.ring/) | Automated around binary sensors via motion or doorbell button press |
| [Ubiquiti Unifi Protect G4 Pro](https://amzn.to/2CrW5cK) | 1 | Ethernet | [Unifi Protect](https://www.home-assistant.io/integrations/unifiprotect/) | 4K POE Camera. |
| [Ubiquiti Unifi G4 Bullet](https://amzn.to/2XRWtIv) | 1 | Ethernet | [Unifi Protect](https://www.home-assistant.io/integrations/unifiprotect/) | 1440p POE Camera. |
| [Ubiquiti UniFi Video G5 Flex](https://amzn.to/2PKrSqA) | 5 | Ethernet | [Unifi Protect](https://www.home-assistant.io/integrations/unifiprotect/) | 1440p POE Camera. |
| [Ubiquiti UniFi Video G3 Flex](https://amzn.to/2PKrSqA) | 1 | Ethernet | [Unifi Protect](https://www.home-assistant.io/integrations/unifiprotect/) | 1080p POE Camera. |
| [Unifi Network Video Recorder (UNVR)](https://amzn.to/3l5xfSV) | 1 | Ethernet | [Unifi Protect](https://www.home-assistant.io/integrations/unifiprotect/) | Unifi Protect NVR. |

Nothing is currently automated around cameras, just a [UI](https://github.com/geekofweek/homeassistant/blob/master/images/camera-screenshot.jpg) element.  The Ring doorbell is used in a number of ways to trigger an action based on motion detection or someone ringing the doorbell.  Examples can be found in [doorbell.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/doorbell.yaml)

I also send camera feeds as a payload on a few iOS notifications, those can mostly be found in [camera.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/camera.yaml)

## <a name="garage">Garage</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [4 Relay ESP32](https://amzn.to/3abd0vG) | 1 | Wi-Fi | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Automated to open / close garage door on location and auto close after specific time intervals |
| [Honeywell Ademco 958 Overhead Door Contacts](https://amzn.to/33CpKZG) | 1 | [4 Relay ESP32](https://amzn.to/3abd0vG) | [ESPHome](https://www.home-assistant.io/integrations/esphome/)| Door Sensor used with ESPHome Relay |

Similar to locks, the Garage door is mostly automated to open / close based on location and after a set amount of time.  Examples can be found in [location.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and [garage.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/garage.yaml)

More detailed information on the ESPhome configuration can be found in [here](https://github.com/geekofweek/homeassistant/tree/master/esphome/garage_door_relay)

## <a name="vacuum">Vacuum</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [iRobot j9+ Combo](https://amzn.to/3RpkcfN) | 1 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [iRobot j7+](https://amzn.to/3qFjcXj) | 1 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [iRobot i7+](https://amzn.to/3f3rksO) | 1 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [iRobot Braava jet 240](https://amzn.to/2FRJnEa) | 1 | Bluetooth | NA | Currently not integrated into Home Assistant. Unknown if this can ever be automated |

All Roomba related automations can be found in [roomba.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/roomba.yaml)

## <a name="blinds">Blinds</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ikea FYRTUR](https://www.ikea.com/us/en/cat/electric-blinds-44531/) | 10 | Zigbee | [ZHA](https://www.home-assistant.io/integrations/zha/) | Automated to open and close blinds based on motion, location, and sun elevation |
| [Ikea PRAKTLYSING](https://www.ikea.com/us/en/p/praktlysing-cellular-blind-smart-wireless-battery-operated-white-00514274/) | 2 | Zigbee | [ZHA](https://www.home-assistant.io/integrations/zha/) | Automated to open and close blinds based on motion, location, and sun elevation |

All Blinds related automations can be found in [blinds.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/blinds.yaml)

## <a name="energy">Energy</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [IoTaWatt](https://iotawatt.com) | 1 | Wi-Fi | [IoTaWatt](https://www.home-assistant.io/integrations/iotawatt/)| Electric power meter that monitors via CT clamps on Mains power and circuit breakers |
| [AccuCT 200A x 25mm split-core](https://stuff.iotawatt.com/product/accuct-200a-x-24mm-split-core/?v=7516fd43adaa) | 2 | IoTaWatt | [IoTaWatt](https://www.home-assistant.io/integrations/iotawatt/)| 200 Amp CT Clamps for Mains power monitoring |
| [AccuCT 100A x 16mm split-core](https://stuff.iotawatt.com/product/accuct-100a-x-16mm-split-core/?v=7516fd43adaa) | 2 | IoTaWatt | [IoTaWatt](https://www.home-assistant.io/integrations/iotawatt/)| 100 Amp CT Clamps for Hot Tub and Air Conditioner power monitoring |
| [AccuCT 100A x 16mm split-core](https://stuff.iotawatt.com/product/accuct-50a-x-10mm-split-core/?v=7516fd43adaa) | 3 | IoTaWatt | [IoTaWatt](https://www.home-assistant.io/integrations/iotawatt/)| 50 Amp CT Clamps for various circuits power monitoring such as Furnace and refrigerator |

Utilzing Home Assitant Energy dashboard plus creating sensors and automations for things such as my Hot Tub and Air Conditoner / HVAC system.

## <a name="appliances">Appliances</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [LG Washer WT7300CW](https://www.lg.com/us/washers/lg-WT7300CW-top-load-washer) | 1 | Wi-Fi | [LG ThinQ](https://github.com/ollo69/ha-smartthinq-washer)| Automated for notifications and remaining run time.  Currently using a custom component for testing purposes |
| [LG Dryer DLGX7801WE](https://www.lg.com/us/dryers/lg-DLGX7801WE-gas-dryer) | 1 | Wi-Fi | [LG ThinQ](https://github.com/ollo69/ha-smartthinq-washer)| Automated for notifications and remaining run time. Currently using a custom component for testing purposes |

All laundry related automations can be found in [laundry.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/laundry.yaml)

## <a name="network">Network</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ubiquiti UniFi Cloud Key Gen2 Plus](https://amzn.to/2RUxtz1) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/) | Unifi Controller. Presence detection for non household members and devices |
| [Ubiquiti Networks Unifi Next-generation Gateway Pro (UXG-Pro-US)](https://store.ui.com/products/unifi-next-generation-gateway-professional) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Primary Router. Presence detection for non household members and devices |
| [Ubiquiti Networks UniFi Enterprise PoE - 24 Ports (USW-Enterprise-24-PoE)](https://amzn.to/3JAVe8R) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Primary Network Switch. Presence detection for non household members and devices |
| [Ubiquiti Networks UniFi Switch PRO PoE - 24 Ports (USW-Pro-24-POE)](https://amzn.to/2YB8jHL) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Secondary Network Switch. Presence detection for non household members and devices |
| [Ubiquiti Networks UniFi Switch Enterprise - 8 Ports (USW-Enterprise-8-PoE)](https://amzn.to/2Iuoah9) | 2 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Additional Network Switches. Presence detection for non household members and devices |
| [Ubiquiti Networks UniFi Access Point WiFi 6 Enterprise (U6-Enterprise)](https://amzn.to/3qZecPW) | 3 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Presence detection for non household members and devices. |
| [Ubiquiti Networks UniFi Access Point WiFi 6 Long-Range (U6-LR-US)](https://amzn.to/3cFM2yX) | 2 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Presence detection for non household members and devices. |


Since I don’t use the network equipment as my primary presence detection method most of the automation is around house guests via [location.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml).  The main function of the network equipment is to be network equipment for my fiber internet service.

## <a name="other">Other Hardware</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Intel NUC NUC8i5BEH](https://amzn.to/2GxgStD) | 1 | Ethernet | NA | Primary Linux server. Docker Containers and Plex media server run off this device. |
| [QNAP TS-453D](https://amzn.to/3TcxgEx) | 1 | Ethernet | [QNAP Sensor](https://www.home-assistant.io/components/sensor.qnap/)| Primary storage array. Configured with 4x [Ultrastar 14TB Data Center Hard Disk Drives](https://amzn.to/42epr56) |
| [QNAP TS-453 Pro](https://amzn.to/2wRmtJh) | 1 | Ethernet | [QNAP Sensor](https://www.home-assistant.io/components/sensor.qnap/)| Secondary storage array. Configured with 4x [WD Red Pro 4TB NAS Hard Disk Drives](https://amzn.to/2IvE7DO) |
| [Prusa MK4](https://www.prusa3d.com/product/original-prusa-mk4-2/) | 1 | Ethernet | [PrusaLink](https://www.home-assistant.io/integrations/prusalink/)| 3D Printer connected to Home Assitant via PrusaLink.  Because if you're going to make useless non-sense, might as well double down. |
| [Prusa i3 MK3S+](https://shop.prusa3d.com/en/3d-printers/180-original-prusa-i3-mk3s-kit.html) | 1 | Ethernet | [RESTful](https://www.home-assistant.io/integrations/rest/)| 3D Printer connected to Home Assitant via the PrusaLink RESTful API running on a Raspberry Pi 4 B.  I would be using PrusaLink integration but it's busted for the updated versions of the API.  Sometimes I make neat objects to help with Home Automation, but mostly useless stuff for fun. |
| [HP OfficeJet Pro 8025](https://amzn.to/3bRP3vv) | 1 | Wi-Fi | [Internet Printing Protocol (IPP)](https://www.home-assistant.io/integrations/ipp/)| Regualr inkjet printer that works whenever it feels like because it's a printer. |
| [APC 1500VA Back-Up UPS](https://amzn.to/2LopbsD) | 2 | USB / Ethernet | [NUT Sensor](https://www.home-assistant.io/components/sensor.nut/)| Primary Uninterruptible Power Supply (UPS). Connected via the NUT component utlizing to a Linux NUT server |
| [Ulanzi Awtrix Smart Pixel Clock](https://www.amazon.com/dp/B0BS8Q9749/ref=cm_sw_r_as_gl_api_gl_i_ZK74G02XHDKXS01RH3VE?linkCode=ml1&tag=homeassistant-20) | 2 | Wi-Fi | [MQTT](https://www.home-assistant.io/integrations/mqtt/)| 8x32 RGB LED panel used to display time and various notifications / status.  Using the [Awtrix Light](https://github.com/Blueforcer/awtrix-light) project to integrate with MQTT and Home Assistant.  It also looks super cool. |

## <a name="software">Software</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [iOS App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401?mt=8) | 2 | NA | [iOS](https://www.home-assistant.io/docs/ecosystem/ios/)| Used as Home Assistant interface on mobile devices and primary method of presence detection. |
| [Docker](https://www.docker.com) | 1 | Ethernet | [Installation on Docker](https://www.home-assistant.io/docs/installation/docker/) | Home Assistant install runs as a Docker Container |
| [Pi-hole](https://pi-hole.net) | 2 | Ethernet / Wi-Fi | [Pi-Hole Sensor](https://www.home-assistant.io/components/sensor.pi_hole/) | Ad blocking. Primary instance runs within a Docker container and the secondary runs on a [Raspberry-pi Zero W](https://amzn.to/2Kwcz1S) |
| [Home Assistant Management Tool](https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt-docker.sh) | 1 | Ethernet | NA | Custom Shell script for managing Home Assistant |

The iOS app is used for some notifications within various automations. The native iOS app is the main method of doing any location based automations via [location.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and many of the conditions I use are based on presence detection of household members.

More detailed information on the custom Home Assistant Managment Tools can be found [here](https://github.com/geekofweek/homeassistant/tree/master/tools).

## <a name="retired">Retired</a>

| [Menu](#menu) | [Screenshots](#screenshots) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [SONOFF Zigbee 3.0 USB Dongle v2 (Plus-E) ](https://amzn.to/3FsEjCk)| 1 | USB | [ZHA](https://www.home-assistant.io/integrations/zha/) | Used to control all Zigbee smart bulbs and Blinds. Replaced by Home Assistant SkyConnect |
| [Hue Hub v2](https://amzn.to/2IpNA3G)| 1 | Ethernet | [Philips Hue](https://www.home-assistant.io/components/hue/) | Used to control all Zigbee smart bulbs. Replaced by Home Assistant ZHA |
| [IKEA TRÅDFRI](https://www.ikea.com/us/en/p/tradfri-gateway-white-00337813/)| 1 | Ethernet | [IKEA TRÅDFRI](https://www.home-assistant.io/integrations/tradfri/) | Currently only used to support the IKEA line of blinds. Replaced by Home Assistant ZHA |
| [Vera Plus](https://amzn.to/2IJGx4M)| 1 | Ethernet | [Vera](https://www.home-assistant.io/components/vera/) | Used as a dumb hub to connect Z-Wave devices. Replaced by a Z-Wave Stick |
| [Wink Hub v1](https://amzn.to/2wMUjis)| 1 | Wi-Fi | [Wink](https://www.home-assistant.io/components/wink/) | ~~Semi retired, using it as a z-wave repeater for Vera.~~ Once upon a time I really loved Wink, but when you don't stock hardware for almost a year and your buisness model is selling hardware... time for that slow ride to the Cloud API in the sky. Not to mention the massive outages when staff clock out and don't fix until morning (forget to renew an expired certificate anyone). It was a fun ride Wink, hopefully your death will not be to slow and painful, but i.am+ wants to watch the world burn... probably.|
| [Quirky + GE Aros Smart Window Air Conditioner](https://amzn.to/2ImtdEi) | 1 | Wi-Fi | [Wink Climate](https://www.home-assistant.io/components/climate.wink/) | No longer used after new HVAC system installed.  Cooling effieceny had dropped and was more of an energy hog than actually making a difference in temprature comfort. |
| [Frigidaire Cool Connect Smart Portable Air Conditioner](https://amzn.to/2k7kszE) | 1 | Wi-Fi | [Harmony Hub Remote](https://www.home-assistant.io/components/remote.harmony/) | No longer in daily use after new HVAC system installed. May be brought back into service as needed. |
| [iHome WiFI Smart Plug](https://amzn.to/2rReF4z) | 2 | Wink Hub (Wi-Fi) | [Wink Switch](https://www.home-assistant.io/components/switch.wink/) | Not using these anymore due to overall poor reliability |
| [Foscam FI9800P](https://amzn.to/2Gu6r7I) | 1 | Wi-Fi | [Foscam IP Camera](https://www.home-assistant.io/components/camera.foscam/) | Replaced by Unifi G3 Flex |
| [Ubiquiti UniFi Cloud Key](https://amzn.to/2Waveqn) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Unifi Controller. Replaced by CloudKey gen2 Plus |
| [Ubiquiti UVC-G3 UniFi Video Camera](https://amzn.to/2L987ah) | 2 | Ethernet | [Unifi Protect](https://github.com/briis/unifiprotect)(Custom Component) | 1080p POE Camera. Replaced with G4 versions |
| [MyQ Smart Garage Door Opener](https://amzn.to/2Iu4Joy) | 1 | Wi-Fi | [MyQ Cover](https://www.home-assistant.io/components/cover.myq/)| Got fed up with the sheer disrepect this device had for reliability. Would work great for months, then decide it had enough and work when it felt like. |
| [MyQ Home Bridge](https://amzn.to/2LyCQk7) | 1 | Wi-Fi | [MyQ Cover](https://www.home-assistant.io/components/cover.myq/)| See Above |
| [TP-Link Smart Plug HS100](https://amzn.to/2L5Bt9r) | 1 | Wi-Fi | [TP-Link Switch](https://www.home-assistant.io/components/switch.tplink/) | No longer needed, might re-use at some point |
| [Wink Relay](https://amzn.to/2GtKAx3) | 2 | Wi-Fi | [Wink](https://www.home-assistant.io/components/wink/)| Wall mounted touch screen. Wink interface was rubbish and was replaced with the Home Assistant dashboard. It provides binary sensors for the two push buttons, temperature, and humidity sensors. Doesn't get used much but looks cool. Turns out it was just rubbish and decided to go into an endless reboot loop, on top of the screen already having burn in problems even when not on all the time.  Retired to the trash can. |
| [Ubiquiti Networks airGateway LR Wireless AP ](https://amzn.to/2Kzbg2d) | 1 | Wi-Fi | NA | Was used to connect Ubiquiti UVC-G3 UniFi Video Camera to the wireless network where running an ethernet cable wasn't feasible. Connects to POE injector.  Replaced by Mesh AP and Switch |
| [Sonos Connect](https://amzn.to/2wSsup8) | 1 | Ethernet |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS. Connects Sonos to existing surround sound system. Now considered a legacy Sonos device |
| [Ubiquiti Networks Unifi AP PRO (UAP-AC-PRO-US)](https://amzn.to/2rP3BFJ) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Replaced by the Unifi NanoHD. |
| [Ubiquiti Networks Unifi AP Long Range (UAP-AC-LR-US)](https://amzn.to/2IsvLwD) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Access Point for interior use. Presence detection for non household members and devices. |
| [Insignia - Wi-Fi Garage Door Controller](https://www.bestbuy.com/site/insignia-wi-fi-garage-door-controller-for-apple-homekit-white/5933701.p?skuId=5933701) | 1 | Wi-Fi | [HomeKit Controller](https://www.home-assistant.io/components/homekit_controller/)| Automated to open / close garage door on location and auto close after specific time intervals |
| [Ring Video Doorbell](https://amzn.to/2KvrzwP) | 1 | Wi-Fi | [Ring](https://www.home-assistant.io/components/ring/) / [Ring Binary Sensor](https://www.home-assistant.io/components/binary_sensor.ring/) | Automated around binary sensors via motion or doorbell button press.  Replaced with a Version 3 Plus. |
| [iRobot Roomba 650](https://amzn.to/2wO2w60) | 1 | NA | NA | Currently not integrated into Home Assistant. Investigating options for future integration |
| [Lutron Smart Bridge 2](https://amzn.to/2GpRGEX)| 1 | Ethernet | [Lutron Caseta](https://www.home-assistant.io/components/lutron_caseta/)| Replaced with a Lutron Smart Bridge 2 Pro |
| [Creality Ender 3 V2](https://amzn.to/3bROjXf) | 1 | Wi-Fi | [OctoPrint](https://www.home-assistant.io/integrations/octoprint/)| 3D Printer connected to Home Assitant via OctoPrint running on a Raspberry Pi 3 B+.  Got tired of messing around with it, I just want to print useless objects with ease |
| [Yamaha RX-V483BL](https://amzn.to/2DhNh89) | 1 | Wi-Fi | [Yamaha Network Receivers](https://www.home-assistant.io/components/media_player.yamaha/) | Surround Sound Receiver. Works in conjunction with the Sonos Connect, Harmony Hub, Apple TV 4k and various other media devices.  Replaced with Sonos Arc System |
| [Ubiquiti Networks UniFi nanoHD (UAP-NANOHD-US)](https://amzn.to/2wPS2no) | 2 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Presence detection for non household members and devices. Replaced by WiFi 6 Models |
| [Ubiquiti Networks Unifi AP Lite (UAP-AC-LITE)](https://amzn.to/2YS8woA) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Access Point for interior use. Presence detection for non household members and devices. Replaced by WiFi 6 Models |
| [iRobot Roomba 980](https://amzn.to/2L9q1tm) | 1 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [Ubiquiti Networks Unifi Security Gateway (USG)](https://amzn.to/2wM62hk) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Primary Router. Presence detection for non household members and devices. Replaced by UXG Pro |
| [Locative iOS App](https://itunes.apple.com/us/app/locative/id725198453?mt=8) | 2 | NA | [Locative](https://www.home-assistant.io/components/device_tracker.locative/) | Put back in retirement since the native iOS app works so well |
| [LUMIMAN LM530](https://amzn.to/3xhHg4m) | 1 | Wi-Fi| [Tuya](https://www.home-assistant.io/integrations/tuya/) | Retired in favor of Philips Wiz line.  Tuya integration is hot garbage.  Routine issues and an account that expires after 6 monhts. |
| [Apple TV 4](https://www.amazon.com/Apple-TV-32GB-4th-Generation/dp/B075NFX24M/ref=sr_1_1?s=electronics&ie=UTF8&qid=1526581435&sr=1-1&keywords=Apple+TV) | 2 | Wi-Fi | [Apple TV](https://www.home-assistant.io/components/apple_tv/) | Used for media playback on TVs. Replaced by newer Apple TVs |
| [Wemo Insight Smart Plug](https://amzn.to/2CfzHRa) | 2 | Wi-Fi | [Belkin WeMo](https://www.home-assistant.io/components/wemo/) | Smart outlet utilized to monitor power.  Wemo devices started to become unreliable so they are being phased out. |
| [Ubiquiti Networks UniFi Switch - 24 Ports (US-24-250W)](https://amzn.to/2LbWLlJ) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Secondary Network Switch. Presence detection for non household members and devices |
| [Ubiquiti Networks 8-Port UniFi Switch (US-8-150W)](https://amzn.to/2Iuoah9) | 2 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Additional Network Switches. Presence detection for non household members and devices |
| [Ubiquiti Networks Unifi Access Point WiFi 6 Lite (U6-Lite-US)](https://amzn.to/3l3Dman) | 2 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Access Point for interior use. Presence detection for non household members and devices. |
| [Ubiquiti Networks Unifi Mesh AP (UAP-AC-M-US)](https://amzn.to/31QrE6E) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Mesh Access Point for exterior use. Used in detached garage to provide internet and network traffic for cameras and devices.  Presence detection for non household members and devices. |
| [Ubiquiti Networks Unifi AP PRO (UAP-AC-PRO-US)](https://amzn.to/2rP3BFJ) | 1 | Ethernet | [Ubiquiti Unifi](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Presence detection for non household members and devices. |
| [Zooz Power Switch ZEN15](https://amzn.to/2WRPeiv) | 2 | Z-Wave | [Z-Wave JS](https://www.home-assistant.io/integrations/zwave_js/) | Realized these would flood the z-wave network with traffic and make it unstable, do not recommend |
| [iRobot Roomba 980](https://amzn.to/2L9q1tm) | 1 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [Prusa Mini+](https://shop.prusa3d.com/en/3d-printers/994-original-prusa-mini.html) | 1 | Ethernet | [PrusaLink](https://www.home-assistant.io/integrations/prusalink/)| 3D Printer connected to Home Assitant via PrusaLink. |

# <a name="screenshots">Screenshots</a>

| [Menu](#menu) |

![UI](images/home-screenshot.jpg?raw=true "Home Page")

| [Menu](#menu) |

![UI](images/living-room-screenshot.jpg?raw=true "Living Room")

| [Menu](#menu) |

![UI](images/dining-screenshot.jpg?raw=true "Dining and Kitchen")

| [Menu](#menu) |

![UI](images/bedrooms-screenshot.jpg?raw=true "Bedrooms")

| [Menu](#menu) |

![UI](images/bath-screenshot.jpg?raw=true "Bathrooms")

| [Menu](#menu) |

![UI](images/offices-screenshot.jpg?raw=true "Offices")

| [Menu](#menu) |

![UI](images/basement-screenshot.jpg?raw=true "Basement")

| [Menu](#menu) |

![UI](images/upstairs-screenshot.jpg?raw=true "Upstairs")

| [Menu](#menu) |

![UI](images/outdoor-screenshot.jpg?raw=true "Outdoors")

| [Menu](#menu) |

![UI](images/weather-screenshot.jpg?raw=true "Weather")

| [Menu](#menu) |

![UI](images/alarm-screenshot.jpg?raw=true "Alarm")

| [Menu](#menu) |

![UI](images/3d-print-screenshot.jpg?raw=true "3D Printer")

| [Menu](#menu) |

![UI](images/system-screenshot.jpg?raw=true "System")

| [Menu](#menu) |

![UI](images/power-screenshot.jpg?raw=true "Power")

| [Menu](#menu) |

![UI](images/water-screenshot.jpg?raw=true "Water")

| [Menu](#menu) |




