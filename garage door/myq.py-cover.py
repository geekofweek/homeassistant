"""
Support for MyQ garage doors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/cover.myq/
"""

import logging
import requests

from homeassistant.components.cover import CoverDevice
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_NAME, STATE_OPEN, STATE_CLOSED


DEPENDENCIES = []

CONF_BRAND = 'brand'

LIFTMASTER = 'liftmaster'
CHAMBERLAIN = 'chamberlain'
CRAFTMASTER = 'craftmaster'

SUPPORTED_BRANDS = [LIFTMASTER, CHAMBERLAIN, CRAFTMASTER]
SUPPORTED_DEVICE_TYPE_NAMES = ['GarageDoorOpener', 'Garage Door Opener WGDO']

DEFAULT_BRAND = CHAMBERLAIN
DEFAULT_NAME = "MyQ"

APP_ID = 'app_id'
HOST_URI = 'host_uri'

BRAND_MAPPINGS = {
    LIFTMASTER: {
        APP_ID: 'JVM/G9Nwih5BwKgNCjLxiFUQxQijAebyyg8QUHr7JOrP+tuPb8iHfRHKwTmDzHOu',
        HOST_URI: 'myqexternal.myqdevice.com'
    },
    CHAMBERLAIN: {
        APP_ID: 'Vj8pQggXLhLy0WHahglCD4N1nAkkXQtGYpq2HrHD7H1nvmbT55KqtN6RSF4ILB%2Fi',
        HOST_URI: 'myqexternal.myqdevice.com'
    },
    CRAFTMASTER: {
        APP_ID: 'eU97d99kMG4t3STJZO/Mu2wt69yTQwM0WXZA5oZ74/ascQ2xQrLD/yjeVhEQccBZ',
        HOST_URI: 'craftexternal.myqdevice.com'
    }
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the MyQ garage door."""

    # name = config.get(CONF_NAME) if \
        # CONF_NAME else DEFAULT_NAME

    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    logger = logging.getLogger(__name__)

    if username is None or password is None:
        logger.error("MyQ Cover - Missing username or password.")
        return

    try:
        brand = BRAND_MAPPINGS[config.get(CONF_BRAND)];
    except KeyError:
        logger.error("MyQ Cover - Missing or unsupported brand. Supported brands: %s", ', '.join(SUPPORTED_BRANDS))
        return

    myq = MyQAPI(username, password, brand, logger)

    add_devices(MyQCoverDevice(myq, door) for door
                in myq.get_garage_doors())


class MyQAPI(object):
    """Class for interacting with the MyQ iOS App API."""

    LOCALE = "en"
    LOGIN_ENDPOINT = "Membership/ValidateUserWithCulture"
    DEVICE_LIST_ENDPOINT = "api/UserDeviceDetails"
    DEVICE_SET_ENDPOINT = "Device/setDeviceAttribute"
    DEVICE_STATUS_ENDPOINT = "/Device/getDeviceAttribute"

    DOOR_STATE = {
        '1': STATE_OPEN, #'open',
        '2': STATE_CLOSED, #'close',
        '4': STATE_OPEN, #'opening',
        '5': STATE_CLOSED, #'closing',
        '8': STATE_OPEN, #'in_transition',
        '9': STATE_OPEN, #'open'
    }

    def __init__(self, username, password, brand, logger):
        """Initialize the API object."""
        self.username = username
        self.password = password
        self.brand = brand
        self._logger = logger;

        self.security_token = None
        self._logged_in = False

    def login(self):
        """Log in to the MyQ service."""

        params = {
            'username': self.username,
            'password': self.password,
            'appId': self.brand[APP_ID],
            'culture': self.LOCALE
        }

        login = requests.get(
            'https://{host_uri}/{login_endpoint}'.format(
                host_uri=self.brand[HOST_URI],
                login_endpoint=self.LOGIN_ENDPOINT),
            params=params,
			headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
        auth = login.json()
        self.security_token = auth['SecurityToken']
        self._logger.debug('Logged in to MyQ API')
        return True

    def get_devices(self):
        """List all MyQ devices."""

        if not self._logged_in:
            self._logged_in = self.login()

        params = {
            'appId': self.brand[APP_ID],
            'securityToken': self.security_token
        }

        devices = requests.get(
            'https://{host_uri}/{device_list_endpoint}'.format(
                host_uri=self.brand[HOST_URI],
                device_list_endpoint=self.DEVICE_LIST_ENDPOINT),
            params=params,
			headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

        devices = devices.json()['Devices']

        return devices

    def get_garage_doors(self):
        """List only MyQ garage door devices."""

        devices = self.get_devices()

        garage_doors = []

        for device in devices:
            if device['MyQDeviceTypeName'] in SUPPORTED_DEVICE_TYPE_NAMES:
                dev = {}
                for attribute in device['Attributes']:
                   if attribute['AttributeDisplayName'] == 'desc':
                        dev['deviceid'] = device['DeviceId']
                        dev['name'] = attribute['Value']
                        garage_doors.append(dev)


        return garage_doors

    def get_status(self, device_id):
        """Get device status."""

        params = {
            'appId': self.brand[APP_ID],
            'securityToken': self.security_token,
            'devId': device_id,
            'name': 'doorstate',
        }

        device_status = requests.get(
            'https://{host_uri}/{device_status_endpoint}'.format(
                host_uri=self.brand[HOST_URI],
                device_status_endpoint=self.DEVICE_STATUS_ENDPOINT),
            params=params,
			headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

        attval = device_status.json()['AttributeValue']

        garage_state = self.DOOR_STATE[attval]
        return garage_state

    def close_device(self, device_id):
        """Close MyQ Device."""
        return self.set_state(device_id, '0')

    def open_device(self, device_id):
        """Open MyQ Device."""
        return self.set_state(device_id, '1')


    def set_state(self, device_id, state):
        """Set device state."""
        payload = {
            'AttributeName': 'desireddoorstate',
            'DeviceId': device_id,
            'ApplicationId': self.brand[APP_ID],
            'AttributeValue': state,
            'SecurityToken': self.security_token,
        }
        device_action = requests.put(
            'https://{host_uri}/{device_set_endpoint}'.format(
                host_uri=self.brand[HOST_URI],
                device_set_endpoint=self.DEVICE_SET_ENDPOINT),
            data=payload,
			headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

        return device_action.status_code == 200


class MyQCoverDevice(CoverDevice):
    """Representation of a MyQ cover."""

    def __init__(self, myq, device):
        """Initialize with API object, device id, and name."""
        self.myq = myq
        self.device_id = device['deviceid']
        self._name = device['name']
        self._status = STATE_CLOSED

    @property
    def should_poll(self):
        """Poll for state."""
        return True

    @property
    def name(self):
        """Return the name of the garage door if any."""
        return self._name if self._name else DEFAULT_NAME

    @property
    def is_closed(self):
        """Return True if cover is closed, else False."""
        return self._status == STATE_CLOSED

    @property
    def current_cover_position(self):
        """Return current position of cover."""
        return 0 if self.is_closed else 100

    def close_cover(self):
        """Issue close command to cover."""
        self.myq.close_device(self.device_id)

    def open_cover(self):
        """Issue open command to cover."""
        self.myq.open_device(self.device_id)

    def update(self):
        self._status = self.myq.get_status(self.device_id)
