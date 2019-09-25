"""Library for controlling an Apple TV."""

import asyncio
import logging
import concurrent
from ipaddress import ip_address
from threading import Lock

from zeroconf import ServiceBrowser, Zeroconf
from aiohttp import ClientSession

from . import (conf, exceptions)
from .airplay import player
from .airplay.api import AirPlayAPI
from .const import (PROTOCOL_MRP, PROTOCOL_DMAP)
from .net import HttpSession

from .dmap import DmapAppleTV
from .mrp import MrpAppleTV

_LOGGER = logging.getLogger(__name__)


HOMESHARING_SERVICE = '_appletv-v2._tcp.local.'
DEVICE_SERVICE = '_touch-able._tcp.local.'
MEDIAREMOTE_SERVICE = '_mediaremotetv._tcp.local.'
AIRPLAY_SERVICE = '_airplay._tcp.local.'


class _ServiceListener:

    # pylint: disable=too-many-arguments
    def __init__(self, loop, abort_on_found, device_ip, protocol, semaphore):
        """Initialize a new _ServiceListener."""
        self.loop = loop
        self.abort_on_found = abort_on_found
        self.device_ip = None if not device_ip else ip_address(device_ip)
        self.protocol = protocol
        self.semaphore = semaphore
        self.found_devices = {}
        self.lock = Lock()

    def add_service(self, zeroconf, service_type, name):
        """Handle callback from zeroconf when a service has been discovered."""
        self.lock.acquire()
        try:
            self._internal_add(zeroconf, service_type, name)
        finally:
            self.lock.release()

    def _internal_add(self, zeroconf, service_type, name):
        if self.abort_on_found and len(self.found_devices) == 1:
            return

        info = zeroconf.get_service_info(service_type, name)
        address = ip_address(info.address)

        # We might be looking for a particular device
        if self.device_ip and self.device_ip != address:
            _LOGGER.debug('Ignoring %s (not matching %s)',
                          address, self.device_ip)
            return

        if info.type == HOMESHARING_SERVICE:
            self.add_hs_service(info, address)
        elif info.type == DEVICE_SERVICE:
            self.add_non_hs_service(info, address)
        elif info.type == MEDIAREMOTE_SERVICE:
            self.add_mrp_service(info, address)
        elif info.type == AIRPLAY_SERVICE:
            self.add_airplay_service(info, address)
        else:
            _LOGGER.warning('Discovered unknown device: %s', info)

    def add_hs_service(self, info, address):
        """Add a new device to discovered list."""
        if self.protocol and self.protocol != PROTOCOL_DMAP:
            return

        name = info.properties[b'Name'].decode('utf-8')
        hsgid = info.properties[b'hG'].decode('utf-8')
        self._handle_service(
            address, name, conf.DmapService(hsgid, port=info.port))

    def add_non_hs_service(self, info, address):
        """Add a new device without Home Sharing to discovered list."""
        if self.protocol and self.protocol != PROTOCOL_DMAP:
            return

        name = info.properties[b'CtlN'].decode('utf-8')
        self._handle_service(
            address, name, conf.DmapService(None, port=info.port))

    def add_mrp_service(self, info, address):
        """Add a new MediaRemoteProtocol device to discovered list."""
        if self.protocol and self.protocol != PROTOCOL_MRP:
            return

        name = info.properties[b'Name'].decode('utf-8')
        self._handle_service(address, name, conf.MrpService(info.port))

    def add_airplay_service(self, info, address):
        """Add a new AirPlay device to discovered list."""
        name = info.name.replace('._airplay._tcp.local.', '')
        self._handle_service(address, name, conf.AirPlayService(info.port))

    def _handle_service(self, address, name, service):
        if address not in self.found_devices:
            self.found_devices[address] = conf.AppleTV(address, name)

        _LOGGER.debug('Auto-discovered %s at %s:%d (protocol: %s)',
                      name, address, service.port, service.protocol)

        atv = self.found_devices[address]
        atv.add_service(service)

        # Check if we should continue to run or not
        if self._should_abort(address):
            _LOGGER.debug('Aborting since a device was found')

            # Only return the found device as a convenience to the user
            self.found_devices = {address: atv}

            # zeroconf is run in a different thread so this must be a
            # thread-safe call
            self.loop.call_soon_threadsafe(self.semaphore.release)

    def _should_abort(self, address):
        if not self.abort_on_found:
            return False

        return self.found_devices[address].usable_service()


# pylint: disable=too-many-arguments
async def scan_for_apple_tvs(loop, timeout=5, abort_on_found=False,
                             device_ip=None, only_usable=True,
                             protocol=None):
    """Scan for Apple TVs using zeroconf (bonjour) and returns them."""
    semaphore = asyncio.Semaphore(value=0, loop=loop)
    listener = _ServiceListener(
        loop, abort_on_found, device_ip, protocol, semaphore)
    zeroconf = Zeroconf()
    try:
        ServiceBrowser(zeroconf, HOMESHARING_SERVICE, listener)
        ServiceBrowser(zeroconf, DEVICE_SERVICE, listener)
        ServiceBrowser(zeroconf, MEDIAREMOTE_SERVICE, listener)
        ServiceBrowser(zeroconf, AIRPLAY_SERVICE, listener)
        _LOGGER.debug('Discovering devices for %d seconds', timeout)
        await asyncio.wait_for(semaphore.acquire(), timeout, loop=loop)
    except concurrent.futures.TimeoutError:
        pass  # Will happen when timeout occurs (totally normal)
    finally:
        zeroconf.close()

    def _should_include(atv):
        if not only_usable:
            return True

        return atv.is_usable()

    return list(filter(_should_include, listener.found_devices.values()))


def connect_to_apple_tv(details, loop, protocol=None, session=None):
    """Connect and logins to an Apple TV."""
    service = _get_service_used_to_connect(details, protocol)

    # If no session is given, create a default one
    if session is None:
        session = ClientSession(loop=loop)

    # AirPlay service is the same for both DMAP and MRP
    airplay = _setup_airplay(loop, session, details)

    # Create correct implementation depending on protocol
    if service.protocol == PROTOCOL_DMAP:
        return DmapAppleTV(loop, session, details, airplay)

    return MrpAppleTV(loop, session, details, airplay)


def _get_service_used_to_connect(details, protocol):
    if not protocol:
        service = details.usable_service()
    else:
        service = details.get_service(protocol)

    if not service:
        raise exceptions.NoUsableServiceError(
            'no usable service to connect to')

    return service


def _setup_airplay(loop, session, details):
    airplay_service = details.airplay_service()
    airplay_player = player.AirPlayPlayer(
        loop, session, details.address, airplay_service.port)
    airplay_http = HttpSession(
        session, 'http://{0}:{1}/'.format(
            details.address, airplay_service.port))
    return AirPlayAPI(airplay_http, airplay_player)
