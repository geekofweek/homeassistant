
# Overview
My personal [Home Assistant](https://home-assistant.io) configurations with 300+ automations.  These are my active automations and configurations that I use every day.  Updated frequently as I add more devices and come up with more and more complicated ways to do simple tasks.

Published configruations working with Home Assistant Version: 0.91.4

# <a name="menu">Menu</a>
 | [Hubs](#hubs) | [Lighting](#lighting) | [Climate](#climate)| [Outlets & Switches](#outlets)|  [Locks](#locks) | [Security](#security) | [Voice Assistant](#voice) | [Media](#media) | [Sensors](#sensors) | [Cameras](#cameras) | [Garage](#garage) | [Vacuum](#vacuum) | [Network](#network) | [Other Hardware](#other) | [Retired Devices](#retired) | [Software](#software) | [Screenshots](#screenshots) |

## <a name="hubs">Hubs</a>

| [Go to Menu](#menu) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Hue Hub v2](https://amzn.to/2IpNA3G) | 1 | Ethernet | [Philips Hue](https://www.home-assistant.io/components/hue/) | Used to control all Zigbee smart bulbs |
| [Lutron Smart Bridge 2](https://amzn.to/2GpRGEX) | 1 | Ethernet | [Lutron Caseta](https://www.home-assistant.io/components/lutron_caseta/) | Used to control Lutron Caseta light switches and dimmers |
| [Vera Plus](https://amzn.to/2IJGx4M) | 1 | Ethernet | [Vera](https://www.home-assistant.io/components/vera/) | Used as a dumb hub to connect Z-Wave devices.|
| [Wink Hub v1](https://amzn.to/2wMUjis) | 1 | Wi-Fi | [Wink](https://www.home-assistant.io/components/wink/) | Semi retired, using it just as a z-wave repeater for Vera. Once upon a time I really loved Wink, but when you don't stock hardware for almost a year and your buisness model is selling hardware, you have to see the writing on the wall. Not to mention the massive outages that. It was a fun ride Wink, hopefully your death will not be to slow and painful. |

Relevant hub configurations can be found within [configuration.yaml](https://github.com/geekofweek/homeassistant/blob/master/configuration.yaml)

## <a name="lighting">Lighting</a>

| [Go to Menu](#menu) | [Home Screenshot](images/home-screenshot.jpg?raw=true "Home Page") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Philips Hue White and Color Ambiance](https://amzn.to/2Ip8waU) | 9 | Ethernet | [Philips Hue Light](https://www.home-assistant.io/components/light.hue/) | Color changing smart bulbs|
| [Philips Hue White and Color Ambiance LightStrip Plus Dimmable](https://amzn.to/2Kx27qF) | 1 | Hue Hub (Zigbee)| [Philips Hue Light](https://www.home-assistant.io/components/light.hue/) | Color changing smart led strip. Used as accent lighting|
| [Philips Hue White](https://amzn.to/2LaUFTd) | 5 | Hue Hub (Zigbee)| [Philips Hue Light](https://www.home-assistant.io/components/light.hue/) | Non color changing smart bulbs|
| [Cree Connected](https://amzn.to/2IpKAnZ) | 8 | Hue Hub (Zigbee)| [Philips Hue Light](https://www.home-assistant.io/components/light.hue/) | Non color changing smart bulbs|
| [Lutron Caseta Wireless Dimmer](https://amzn.to/2KwDJWc) | 14 | Lutron Clear Connect | [Lutron Caseta Light](https://www.home-assistant.io/components/lutron_caseta/) | Smart dimmer switches that do not require a neutral wire|

Many of my automations rely on some form of lighting but many examples can be found in [lights.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/lights.yaml) and [location.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml).

Lights are grouped via [light_group.yaml](https://github.com/geekofweek/homeassistant/blob/master/light_group.yaml)

## <a name="climate">Climate</a>

| [Go to Menu](#menu) | [Weather Screenshot](images/weather-screenshot.jpg?raw=true "Weather") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ecobee 3](https://amzn.to/2L72d9A) | 1 | Wi-Fi | [ecobee](https://www.home-assistant.io/components/ecobee/) / [Ecobee Thermostat](https://www.home-assistant.io/components/climate.ecobee/) | Used as primary thermostat |
| [Ecobee Room Sensor](https://amzn.to/2L9cORm) | 9 | Ecobee3 | [Ecobee Binary Sensor](https://www.home-assistant.io/components/binary_sensor.ecobee/) | Provides room temperature and room occupancy.|
| [Dyson Pure Hot + Cool Link](https://amzn.to/2RQjDtR) | 1 | Wi-Fi | [Dyson](https://www.home-assistant.io/components/dyson/) | Dyson Fan with Heater and Air Purifier|

I utilize a number of automations that adjust climate controls.  Mostly they can be found in [climate.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/climate.yaml). Ecobee room sensors are heavily used in [occupancy.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/occupancy.yaml) and as conditions in many automations

## <a name="outlets">Outlets & Switches</a>

| [Go to Menu](#menu) | [Home Screenshot](images/home-screenshot.jpg?raw=true "Home Page") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Wemo Mini Smart Plug](https://amzn.to/2wQ05jE) | 4 | Wi-Fi | [Belkin WeMo](https://www.home-assistant.io/components/wemo/) | Smart outlets utilized to control various devices via powering the outlet on/off (fans, Christmas Tree, etc) |
| [Wemo Insight Smart Plug](https://amzn.to/2CfzHRa) | 1 | Wi-Fi | [Belkin WeMo](https://www.home-assistant.io/components/wemo/) | Smart outlet utilized to monitor power to washing machine |
| [GE Z-Wave Wireless Smart Lighting Control Outdoor Module](https://amzn.to/2KuFRxN) | 2 | Wink Hub (Z-Wave)| [Wink Switch](https://www.home-assistant.io/components/switch.wink/) | Used to control low voltage outdoor lighting transformers |
| [Remotec Zwave Dry Contact Fixture Module](https://amzn.to/2rOmcBW) | 1 | Wink Hub (Z-Wave)| [Wink Switch](https://www.home-assistant.io/components/switch.wink/) | Used to control gas fireplace |
| [TP-Link Smart Plug HS100](https://amzn.to/2L5Bt9r) | 1 | Wi-Fi | [TP-Link Switch](https://www.home-assistant.io/components/switch.tplink/) | Smart outlet used to control power to MyQ Device|

Switches and outlets are used in various capacities, some are for lighting and some are for fans type devices.  [lights.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/lights.yaml) and [occupancy.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/occupancy.yaml) should have some good examples.

Washing machine is automated around the Wemo Insight Plug.  This outlet can monitor power consumption, I created a [sensor](https://github.com/geekofweek/homeassistant/blob/master/sensors.yaml) based on the power reading that shows a simple status of running or not running thus [automating](https://github.com/geekofweek/homeassistant/blob/master/automation/laundry.yaml) around that sensor.

## <a name="locks">Locks</a>

| [Go to Menu](#menu) | [Automation Screenshot](images/automation-screenshot.jpg?raw=true "Automations") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Schlage Connect Touchscreen Deadbolt](https://amzn.to/2KwXltd) | 3 | Wink Hub (Z-Wave) | [Wink Lock](https://www.home-assistant.io/components/lock.wink/) | Smart locks used in automations to auto lock / unlock doors |

Locks are used mostly as a way to lock / unlock doors based on locations, see [location.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and [locks.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/locks.yaml) for some examples

## <a name="security">Security</a>

| [Go to Menu](#menu) | [Automation Screenshot](images/automation-screenshot.jpg?raw=true "Automations") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [GoControl Door/Window Sensor](https://amzn.to/2wOhLfn) | 3 | Wink Hub (Z-Wave) | [Wink Binary Sensor](https://www.home-assistant.io/components/binary_sensor.wink/) | Door sensors to detect if exterior doors have been opened / closed |
| [GoControl Siren and Strobe](https://amzn.to/2k4bK4U) | 1 | Wink Hub (Z-Wave) | [Wink Alarm](https://www.home-assistant.io/components/alarm_control_panel.wink/) | Alarm used for when alarm is triggered or when you want to get someone's attention|

Door sensors are used in many different ways. I trigger on them via [doors.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/doors.yaml), use them for security in [security.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/security.yaml), and as various conditions in [notification_audio.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/notification_audio.yaml) and [climate.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/climate.yaml).
The alarm siren is used in [security.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/security.yaml) and in the security [scene](https://github.com/geekofweek/homeassistant/blob/master/scenes.yaml). I've also implemented the alarm as part of [water_sensors.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/water_sensors.yaml).

## <a name="voice">Voice Assistant</a>

| [Go to Menu](#menu) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Amazon Echo](https://amzn.to/2KuPHjd) | 1 | Wi-Fi | [Emulated Hue Bridge](https://www.home-assistant.io/components/emulated_hue/) | Audio only Voice Assistant |
| [Amazon Echo Dot](https://amzn.to/2wSreSW) | 6 | Wi-Fi | [Emulated Hue Bridge](https://www.home-assistant.io/components/emulated_hue/) | Audio only Voice Assistant |
| [Amazon Echo Spot](https://amzn.to/2rOVZ6a) | 1 | Wi-Fi | [Emulated Hue Bridge](https://www.home-assistant.io/components/emulated_hue/) | Voice Assistant with small display |
| [Amazon Echo Show](https://amzn.to/2rRhN0n) | 1 | Wi-Fi |  [Emulated Hue Bridge](https://www.home-assistant.io/components/emulated_hue/) |Voice Assistant with display |

I go for native Echo integration wherever possible, but a few devices are not currently supported where I've had to implement some work arounds via emulated hue.  Most of these are just exposed via an [input_boolean]( https://github.com/geekofweek/homeassistant/blob/master/input_boolean.yaml) and [customize.yaml]( https://github.com/geekofweek/homeassistant/blob/master/customize.yaml).  This allows the ability to have echo turn on or off an [input_boolean]( https://github.com/geekofweek/homeassistant/blob/master/input_boolean.yaml)  in turn triggering an automation.

## <a name="media">Media</a>

| [Go to Menu](#menu) | [Media Screenshot](images/media-screenshot.jpg?raw=true "Media") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Apple TV 4k](https://www.amazon.com/Apple-MQD22LL-A-TV-4K/dp/B075NCMLYL/ref=sr_1_2?ie=UTF8&qid=1526581374&sr=8-2&keywords=Apple+TV) | 2 | Wi-Fi | [Apple TV](https://www.home-assistant.io/components/apple_tv/) | Used for media playback on 4k TVs |
| [Apple TV 4](https://www.amazon.com/Apple-TV-32GB-4th-Generation/dp/B075NFX24M/ref=sr_1_1?s=electronics&ie=UTF8&qid=1526581435&sr=1-1&keywords=Apple+TV) | 2 | Wi-Fi | [Apple TV](https://www.home-assistant.io/components/apple_tv/) | Used for media playback on TVs |
| [Sonos Play:1](https://amzn.to/2IrsIor) | 10 | Wi-Fi | [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS |
| [Sonos Connect](https://amzn.to/2wSsup8) | 1 | Ethernet |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS. Connects Sonos to existing surround sound system |
| [Sonos Connect:AMP](https://amzn.to/2rQ0XzM) | 1 | Wi-Fi |  [Sonos](https://www.home-assistant.io/components/media_player.sonos/) | Audio playback and Home Assistant TTS. Connects Sonos to outdoor speakers |
| [Logitech Harmony Hub](https://amzn.to/2IuEvlS) | 3 | Wi-Fi | [Harmony Hub Remote](https://www.home-assistant.io/components/remote.harmony/) | Controls various AV equipment and other devices that utilize infrared remotes |
| [Yamaha RX-V483BL](https://amzn.to/2DhNh89) | 1 | Wi-Fi | [Yamaha Network Receivers](https://www.home-assistant.io/components/media_player.yamaha/) | Surround Sound Receiver. Works in conjunction with the Sonos Connect, Harmony Hub, Apple TV 4k and various other media devices |
| [Plex Media Server](https://plex.tv) | 1 | Ethernet | [Plex](https://www.home-assistant.io/components/media_player.plex) / [Plex Activity Monitor](https://www.home-assistant.io/components/sensor.plex/) |  Media Server|  

Most media player based automations can be found in [media.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/media.yaml) and some Text to Speech (TTS) based automation in [notification_audio.yaml
]( https://github.com/geekofweek/homeassistant/blob/master/automation/notification_audio.yaml).

Harmony Hubs work via a combination of [input_selects]( https://github.com/geekofweek/homeassistant/blob/master/input_select.yaml), [scripts]( https://github.com/geekofweek/homeassistant/blob/master/scripts.yaml), and automations in [media.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/media.yaml).

## <a name="sensors">Sensors</a>

| [Go to Menu](#menu) | [Sensors Screenshot](images/sensors-screenshot.jpg?raw=true "Sensors") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Aeon Labs Water Sensor](https://amzn.to/2rM6KFE) | 2 | Wink Hub (Z-Wave) | [Wink Binary Sensor](https://www.home-assistant.io/components/binary_sensor.wink/) | Water sensors used to detect water in basement as a preventive measure |
| [Nest Protect v2 Battery](https://amzn.to/2LJ0ACn) | 6 | Wi-Fi | [Nest](https://www.home-assistant.io/components/nest/) | Smoke Alarm and CO Alarm.  I realized most of my Smoke Alarms had long suprased the 10 year mark and it was time for some replacements. I usually avoid Google owned products for various reasons, but the Nest Protect line has high praise. |

Water sensors serve one major function, to alert me to the presence of water.  Almost all of those automations can be fond via [water_sensors.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/water_sensors.yaml)

Smoke detectors, like the water sensors, have one real function to alert me of smoke or CO2.  Almost all of those automations can be fond via [smoke_alarm.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/smoke_alarm.yaml)

## <a name="cameras">Cameras</a>

| [Go to Menu](#menu) | [Cameras Screenshot](images/camera-screenshot.jpg?raw=true "Cameras") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ring Video Doorbell](https://amzn.to/2KvrzwP) | 1 | Wi-Fi | [Ring](https://www.home-assistant.io/components/ring/) / [Ring Binary Sensor](https://www.home-assistant.io/components/binary_sensor.ring/) | Automated around binary sensors via motion or doorbell button press |
| [Ubiquiti UVC-G3 UniFi Video Camera](https://amzn.to/2L987ah) | 2 | Ethernet | [Generic IP Camera](https://www.home-assistant.io/components/camera.generic/) | 1080p POE Camera. |
| [Ubiquiti UniFi Video G3 Flex](https://amzn.to/2PKrSqA) | 5 | Ethernet | [Generic IP Camera](https://www.home-assistant.io/components/camera.generic/) | 1080p POE Camera. |
| [Ubiquiti UniFi Cloud Key Gen2 Plus](https://amzn.to/2RUxtz1) | 1 | Ethernet | [Generic IP Camera](https://www.home-assistant.io/components/camera.generic/) | Unifi Protect NVR. |

Nothing is currently automated around cameras, just a [UI](https://github.com/geekofweek/homeassistant/blob/master/images/camera-screenshot.jpg) element.  The Ring doorbell is used in a number of ways to trigger an action based on motion detection or someone ringing the doorbell.  Examples can be found in [doorbell.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/doorbell.yaml)

I also send camera feeds as a payload on a few iOS notifications, those can mostly be found in [notification_text.yaml](https://github.com/geekofweek/homeassistant/blob/master/automation/notification_text.yaml)

## <a name="garage">Garage</a>

| [Go to Menu](#menu) | [Auto Screenshot](images/auto-screenshot.jpg?raw=true "Auto") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Insignia - Wi-Fi Garage Door Controller](https://www.bestbuy.com/site/insignia-wi-fi-garage-door-controller-for-apple-homekit-white/5933701.p?skuId=5933701) | 1 | Wi-Fi | [HomeKit Controller](https://www.home-assistant.io/components/homekit_controller/)| Automated to open / close garage door on location and auto close after specific time intervals |

Similar to locks, the Garage door is mostly automated to open / close based on location and after a set amount of time.  Examples can be found in [location.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and [garage.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/garage.yaml)

## <a name="vacuum">Vacuum</a>

| [Go to Menu](#menu) | [Home Screenshot](images/home-screenshot.jpg?raw=true "Home Page") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [iRobot Roomba 980](https://amzn.to/2L9q1tm) | 2 | Wi-Fi | [iRobot Roomba](https://www.home-assistant.io/components/vacuum.roomba/)| Automated to run at specific times based on presence detection |
| [iRobot Roomba 650](https://amzn.to/2wO2w60) | 1 | NA | NA | Currently not integrated into Home Assistant. Investigating options for future integration |
| [iRobot Braava jet 240](https://amzn.to/2FRJnEa) | 1 | Bluetooth | NA | Currently not integrated into Home Assistant. Unknown if this can ever be automated |

All Roomba related automations can be found in [roomba.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/roomba.yaml)

## <a name="network">Network</a>

| [Go to Menu](#menu) | [Sensors Screenshot](images/sensors-screenshot.jpg?raw=true "Sensors") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Ubiquiti UniFi Cloud Key Gen2 Plus](https://amzn.to/2RUxtz1) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Unifi Controller. Presence detection for non household members and devices |
| [Ubiquiti Networks Unifi Security Gateway (USG)](https://amzn.to/2wM62hk) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Primary Router. Presence detection for non household members and devices |
| [Ubiquiti Networks UniFi Switch - 24 Ports (US-24-250W)](https://amzn.to/2LbWLlJ) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Primary Switch. Presence detection for non household members and devices |
| [Ubiquiti Networks 8-Port UniFi Switch (US-8-150W)](https://amzn.to/2Iuoah9) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Secondary Switch. Presence detection for non household members and devices |
| [Ubiquiti Networks Unifi AP PRO (UAP-AC-PRO-US)](https://amzn.to/2rP3BFJ) | 3 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/)| Wireless Access Point for interior and exterior use. Presence detection for non household members and devices. |
| [Ubiquiti Networks Unifi AP Long Range (UAP-AC-LR-US)](https://amzn.to/2IsvLwD) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Access Point for interior use. Presence detection for non household members and devices. |
| [Ubiquiti Networks Unifi AP Lite (UAP-AC-LITE)](https://amzn.to/2YS8woA) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Wireless Access Point for interior use. Presence detection for non household members and devices. |
| [Ubiquiti Networks airGateway LR Wireless AP ](https://amzn.to/2Kzbg2d) | 1 | Wi-Fi | NA | Used to connect Ubiquiti UVC-G3 UniFi Video Camera to the wireless network where running an ethernet cable wasn't feasible. Connects to POE injector |

Since I don’t use the network equipment as my primary presence detection method most of the automation is around house guests via [house_guest.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/house_guest.yaml).  The main function of the network equipment is to be network equipment for my fiber internet service.

## <a name="other">Other Hardware</a>

| [Go to Menu](#menu) | [System Screenshot](images/system-screenshot.jpg?raw=true "System") |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [QNAP TS-453 Pro](https://amzn.to/2wRmtJh) | 1 | Ethernet | [QNAP Sensor](https://www.home-assistant.io/components/sensor.qnap/)| Main storage array. Docker Containers and Plex media server run off this device. Configured with 4x [WD Red Pro 4TB NAS Hard Disk Drives](https://amzn.to/2IvE7DO) |
| [APC 1500VA Back-Up UPS](https://amzn.to/2LopbsD) | 1 | USB / Ethernet | [NUT Sensor](https://www.home-assistant.io/components/sensor.nut/)| Primary Uninterruptible Power Supply (UPS). Connected via the NUT component utlizing the QNAP NAS native UPS server component |
| [Wink Relay](https://amzn.to/2GtKAx3) | 2 | Wi-Fi | [Wink](https://www.home-assistant.io/components/wink/)| Wall mounted touch screen. Wink interface was rubbish and was replaced with the Home Assistant dashboard. It provides binary sensors for the two push buttons, temperature, and humidity sensors. Doesn't get used much but looks cool. |

## <a name="retired">Retired</a>

| [Go to Menu](#menu) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [Quirky + GE Aros Smart Window Air Conditioner](https://amzn.to/2ImtdEi) | 1 | Wi-Fi | [Wink Climate](https://www.home-assistant.io/components/climate.wink/) | No longer used after new HVAC system installed.  Cooling effieceny had dropped and was more of an energy hog than actually making a difference in temprature comfort. |
| [Frigidaire Cool Connect Smart Portable Air Conditioner](https://amzn.to/2k7kszE) | 1 | Wi-Fi | [Harmony Hub Remote](https://www.home-assistant.io/components/remote.harmony/) | No longer in daily use after new HVAC system installed. May be brought back into service as needed. |
| [iHome WiFI Smart Plug](https://amzn.to/2rReF4z) | 2 | Wink Hub (Wi-Fi) | [Wink Switch](https://www.home-assistant.io/components/switch.wink/) | Not using these anymore due to overall poor reliability |
| [Foscam FI9800P](https://amzn.to/2Gu6r7I) | 1 | Wi-Fi | [Foscam IP Camera](https://www.home-assistant.io/components/camera.foscam/) | Replaced by Unifi G3 Flex |
| [Ubiquiti UniFi Cloud Key](https://amzn.to/2Waveqn) | 1 | Ethernet | [Ubiquiti Unifi WAP](https://www.home-assistant.io/components/device_tracker.unifi/) | Unifi Controller. Replaced by CloudKey gen2 Plus |
| [Locative iOS App](https://itunes.apple.com/us/app/locative/id725198453?mt=8) | 2 | NA | [Locative](https://www.home-assistant.io/components/device_tracker.locative/) | Retired in favor of native iOS app |
| [MyQ Smart Garage Door Opener](https://amzn.to/2Iu4Joy) | 1 | Wi-Fi | [MyQ Cover](https://www.home-assistant.io/components/cover.myq/)| Got fed up with the sheer disrepect this device had for reliability. Would work great for months, then decide it had enough and work when it felt like. |
| [MyQ Home Bridge](https://amzn.to/2LyCQk7) | 1 | Wi-Fi | [MyQ Cover](https://www.home-assistant.io/components/cover.myq/)| See Above |

## <a name="software">Software</a>

| [Go to Menu](#menu) |

| Device  | Quantity | Connection | Home Assistant | Notes |
| ------------- | :---: | ------------- | ------------- | ------------- |
| [iOS App](https://itunes.apple.com/us/app/home-assistant-open-source-home-automation/id1099568401?mt=8) | 2 | NA | [iOS](https://www.home-assistant.io/docs/ecosystem/ios/)| Used as Home Assistant interface on mobile devices and primary method of presence detection. |
| [Docker](https://www.docker.com) | 1 | Ethernet | [Installation on Docker](https://www.home-assistant.io/docs/installation/docker/) | Home Assistant install runs as a Docker Container |
| [Pi-hole](https://pi-hole.net) | 2 | Ethernet / Wi-Fi | [Pi-Hole Sensor](https://www.home-assistant.io/components/sensor.pi_hole/) | Ad blocking. Primary instance runs within a Docker container and the secondary runs on a [Raspberry-pi Zero W](https://amzn.to/2Kwcz1S) |
| [Home Assistant Management Tool](https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt-docker.sh) | 1 | Ethernet | NA | Custom Shell script for managing Home Assistant |

The iOS app is used for some notifications in [notification_text.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/notification_text.yaml). Locative is the main method of doing any location based automations via [location.yaml]( https://github.com/geekofweek/homeassistant/blob/master/automation/location.yaml) and many of the conditions I use are based on presence detection of household members provided by Locative.

The [Home Assistant Management Tool](https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt-docker.sh) is something I built for my personal use, but can easily be modified to suite different setups.  Adjust the variables to your settings and setup shared SSH keys (if desired).  Probably a million other more efficient ways to do this, but it has worked out so far for me.  I had a previous version that I was using before converting to a Docker based installation. That one works with a more traditional installation.  You can check out that version [here]( https://github.com/geekofweek/homeassistant/blob/master/tools/ha-mgmt.sh)

#### Overview:

- Bash Shell script, should work anywhere you can use Bash
- All HA configs are stored on my local workstation within Dropbox (doesn’t have to be but I like the versioning and access to it from any machine).
- Edit locally with Text Editor.  Currently using [Atom]( https://atom.io) and VIM

#### Options:

1.	Deploy Home Assistant Configs
    - Creates tar file of current configs
    - Backs up tar file to local workstation (I use a Dropbox Folder)
    - rsyncs config directory from local workstation (Dropbox Folder)
2.	Restart Home Assistant
    - Restarts the Home Assistant Docker container, thus restarting Home Assistant
3. 	Stop Home Assistant
    - Stops the Home Assistant Docker Container
4.	Start Home Assistant
    - Starts the Home Assistant Docker Container
5.	Upgrade Home Assistant
    - Does a docker pull for the latest version of Home Assistant
    - Stops the Home Assistant Docker Container
    - Deletes the Home Assistant Docker Container
    - Creates a new Home Assistant Docker Container
6.	Check Database Size
    - Check the size of the MySQL Database
7. 	Validate Home Assistant Config
    - Runs a config check using a Docker Container
8. 	Backup Home Assistant
    - Creates tar file of current configs
    - Backs up tar file to local workstation (Dropbox Folder)
9. 	Copy Configs to GitHub
    - Copy’s current config to local workstation Github, scrubs any data that is listed in [redacted.txt]( https://github.com/geekofweek/homeassistant/blob/master/tools/redacted.txt) using [ha-github-scrub.sh]( https://github.com/geekofweek/homeassistant/blob/master/tools/ha-github-scrub.sh).  
10.	Renew SSL Certificate
    - Runs a certbot (Let's Encrypt) Docker container that generates a new SSL certificate

x)  Exit
    – I shouldn’t need to explain that one

#### Variables:

hauser=“USER_ACCOUNT” **<-- Home Assistant User Account**

habin="/usr/local/bin/hass" **<-- Home Assistant Binary**

haconfigdir="/home/USER/.homeassistant" **<-- Home Assistant Config Directory**

hahost=“HOSTNAME/IP” **<-- Home Assistant Hostname or IP address**

localuser=“USER_ACCOUNT” **<-- Local Computer Username, account from where this shell script will run**

localhost=“HOSTNAME/IP” **<-- Local Computer Hostname or IP address**

localpath=“PATH_TO_LOCAL_HA_CONFIGS” **<-- Where I store my local HA configs and backups**

docker="/PATH/TO/DOCKER/bin " **<-- Docker Binary**


Within the local folder, variable localpath="PATH_TO_LOCAL_HA_CONFIGS", I have two folders:

**Config:** All of the .yaml files for Home Assistant

**Backup:** Place for backup tar file



# <a name="screenshots">Screenshots</a>

| [Go to Menu](#menu) |

![UI](images/home-screenshot.jpg?raw=true "Home Page")
![UI](images/living-room-screenshot.jpg?raw=true "Living Room")
![UI](images/dining-screenshot.jpg?raw=true "Dining and Kitchen")
![UI](images/bedrooms-screenshot.jpg?raw=true "Bedrooms")
![UI](images/bath-screenshot.jpg?raw=true "Bathrooms")
![UI](images/offices-screenshot.jpg?raw=true "Offices")
![UI](images/basement-screenshot.jpg?raw=true "Basement")
![UI](images/outdoor-screenshot.jpg?raw=true "Outdoors")
![UI](images/weather-screenshot.jpg?raw=true "Weather")
![UI](images/media-screenshot.jpg?raw=true "Media")
![UI](images/camera-screenshot.jpg?raw=true "Cameras")
![UI](images/auto-screenshot.jpg?raw=true "Auto")
![UI](images/automation-screenshot.jpg?raw=true "Automations")
![UI](images/sensors-screenshot.jpg?raw=true "Sensors")
![UI](images/system-screenshot.jpg?raw=true "System")

| [Go to Menu](#menu) |




