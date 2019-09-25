"""Support for Apple TV."""
import asyncio
import logging
from typing import Sequence, TypeVar, Union

import voluptuous as vol

from homeassistant.components.discovery import SERVICE_APPLE_TV
from homeassistant.const import ATTR_ENTITY_ID, CONF_HOST, CONF_NAME
from homeassistant.helpers import discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "apple_tv_mrp"

SERVICE_SCAN = "apple_tv_mrp_scan"
SERVICE_AUTHENTICATE = "apple_tv_mrp_authenticate"

ATTR_ATV = "atv"
ATTR_POWER = "power"

CONF_PORT = "port"
CONF_START_OFF = "start_off"
CONF_CREDENTIALS = "credentials"

DEFAULT_NAME = "Apple TV"

DATA_APPLE_TV = "data_apple_tv_mrp"
DATA_ENTITIES = "data_apple_tv_mrp_entities"

KEY_CONFIG = "apple_tv_mrp_configuring"

NOTIFICATION_AUTH_ID = "apple_tv_mrp_auth_notification"
NOTIFICATION_AUTH_TITLE = "Apple TV Authentication"
NOTIFICATION_SCAN_ID = "apple_tv_mrp_scan_notification"
NOTIFICATION_SCAN_TITLE = "Apple TV Scan"

T = TypeVar("T")  # pylint: disable=invalid-name


# This version of ensure_list interprets an empty dict as no value
def ensure_list(value: Union[T, Sequence[T]]) -> Sequence[T]:
    """Wrap value in list if it is not one."""
    if value is None or (isinstance(value, dict) and not value):
        return []
    return value if isinstance(value, list) else [value]


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_HOST): cv.string,
                        vol.Required(CONF_PORT): cv.string,
                        vol.Optional(CONF_CREDENTIALS): cv.string,
                        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                        vol.Optional(CONF_START_OFF, default=False): cv.boolean,
                    }
                )
            ],
        )
    },
    extra=vol.ALLOW_EXTRA,
)

# Currently no attributes but it might change later
APPLE_TV_SCAN_SCHEMA = vol.Schema({})

APPLE_TV_AUTHENTICATE_SCHEMA = vol.Schema({ATTR_ENTITY_ID: cv.entity_ids})

def request_pin(hass, config, atv):
    configurator = hass.components.configurator

    async def configuration_callback(callback_data):
        from .pyatv_mrp import exceptions

        pin = callback_data.get("pin")

        try:
            atv.pairing.pin(pin)
            await atv.pairing.stop()

            if atv.pairing.has_paired:
                hass.components.persistent_notification.async_create(
                    f"Authentication succeeded!<br /><br />Add the following to credentials: in your apple_tv_mrp configuration:<br /><br/>{atv.pairing.credentials}",
                    title=NOTIFICATION_AUTH_TITLE,
                    notification_id=NOTIFICATION_AUTH_ID
                )
            else:
                hass.components.persistent_notification.async_create(
                    "Authentication failed!",
                    title=NOTIFICATION_AUTH_TITLE,
                    notification_id=NOTIFICATION_AUTH_ID
                )

            hass.async_add_job(configurator.request_done, instance)

        except Exception as ex:
            hass.components.persistent_notification.async_create(
                f"Authentication failed!<br/>Message: {ex}", 
                title=NOTIFICATION_AUTH_TITLE, 
                notification_id=NOTIFICATION_AUTH_ID
            )

    instance = configurator.request_config(
        "Apple TV Authentication",
        configuration_callback,
        description="Please enter PIN code shown on screen.",
        submit_caption="Confirm",
        fields=[{"id": "pin", "name": "PIN Code", "type": "password"}],
    )

async def scan_for_apple_tvs(hass):
    """Scan for devices and present a notification of the ones found."""
    from .pyatv_mrp import scan_for_apple_tvs
    from .pyatv_mrp.const import PROTOCOL_MRP

    atvs = await scan_for_apple_tvs(hass.loop, timeout=3)

    devices = []
    for atv in atvs:
        mrp_service = atv.get_service(PROTOCOL_MRP)

        if mrp_service is None:
            continue

        devices.append(f"Name: {atv.name}<br/>Host: {atv.address}<br/>Port: {mrp_service.port}")

    if not devices:
        devices = ["No device(s) found"]

    hass.components.persistent_notification.async_create(
        "The following devices were found:<br /><br />" + "<br /><br />".join(devices),
        title=NOTIFICATION_SCAN_TITLE,
        notification_id=NOTIFICATION_SCAN_ID,
    )


async def async_setup(hass, config):
    """Set up the Apple TV component."""
    if DATA_APPLE_TV not in hass.data:
        hass.data[DATA_APPLE_TV] = {}

    async def async_service_handler(service):
        """Handle service calls."""

        if service.service == SERVICE_SCAN:
            hass.async_add_job(scan_for_apple_tvs, hass)
            return
        elif service.service == SERVICE_AUTHENTICATE:
            entity_ids = service.data.get(ATTR_ENTITY_ID)

            if entity_ids:
                devices = [
                    device
                    for device in hass.data[DATA_ENTITIES]
                    if device.entity_id in entity_ids
                ]
            else:
                devices = hass.data[DATA_ENTITIES]

        for device in devices:
            atv = device.atv
            await atv.pairing.start()

            hass.async_add_job(request_pin, hass, config, atv)

    tasks = [_setup_atv(hass, config, conf) for conf in config.get(DOMAIN, [])]
    if tasks:
        await asyncio.wait(tasks)

    hass.services.async_register(
        DOMAIN, SERVICE_SCAN, async_service_handler, schema=APPLE_TV_SCAN_SCHEMA
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_AUTHENTICATE,
        async_service_handler,
        schema=APPLE_TV_AUTHENTICATE_SCHEMA,
    )

    return True


async def _setup_atv(hass, hass_config, atv_config):
    """Set up an Apple TV."""
    from .pyatv_mrp import connect_to_apple_tv
    from .pyatv_mrp.const import PROTOCOL_MRP
    from .pyatv_mrp.conf import (AppleTV, MrpService)

    name = atv_config.get(CONF_NAME)
    host = atv_config.get(CONF_HOST)
    port = int(atv_config.get(CONF_PORT))
    start_off = atv_config.get(CONF_START_OFF)
    credentials = atv_config.get(CONF_CREDENTIALS)

    if host in hass.data[DATA_APPLE_TV]:
        return

    details = AppleTV(host, name)
    details.add_service(MrpService(port, device_credentials=credentials))

    session = async_get_clientsession(hass)
    atv = connect_to_apple_tv(details, hass.loop, protocol=PROTOCOL_MRP, session=session)

    power = AppleTVPowerManager(hass, atv, start_off)
    hass.data[DATA_APPLE_TV][host] = {ATTR_ATV: atv, ATTR_POWER: power}

    hass.async_create_task(
        discovery.async_load_platform(
            hass, "media_player", DOMAIN, atv_config, hass_config
        )
    )

    hass.async_create_task(
        discovery.async_load_platform(hass, "remote", DOMAIN, atv_config, hass_config)
    )


class AppleTVPowerManager:
    """Manager for global power management of an Apple TV.

    An instance is used per device to share the same power state between
    several platforms.
    """

    def __init__(self, hass, atv, is_off):
        """Initialize power manager."""
        self.hass = hass
        self.atv = atv
        self.listeners = []
        self._is_on = not is_off

    def init(self):
        """Initialize power management."""
        if self._is_on:
            self.atv.push_updater.start()

    @property
    def turned_on(self):
        """Return true if device is on or off."""
        return self._is_on

    def set_power_on(self, value):
        """Change if a device is on or off."""
        if value != self._is_on:
            self._is_on = value
            if not self._is_on:
                self.atv.push_updater.stop()
            else:
                self.atv.push_updater.start()

            for listener in self.listeners:
                self.hass.async_create_task(listener.async_update_ha_state())