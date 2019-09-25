"""Methods used to GET/POST data from/to an Apple TV."""

import re
import logging

from copy import copy


from .. import exceptions
from . import parser
from .tag_definitions import lookup_tag

_LOGGER = logging.getLogger(__name__)

_DMAP_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip',
    'Client-DAAP-Version': '3.13',
    'Client-ATV-Sharing-Version': '1.2',
    'Client-iTunes-Sharing-Version': '3.15',
    'User-Agent': 'Remote/1021',
    'Viewer-Only-Client': '1',
}


DEFAULT_TIMEOUT = 10.0  # Seconds


class DaapRequester:
    """Helper class that makes it easy to perform DAAP requests.

    It will automatically do login and other necesarry book-keeping.
    """

    def __init__(self, http, login_id):
        """Initialize a new DaapRequester."""
        self.http = http
        self._login_id = login_id
        self._session_id = 0

    async def login(self):
        """Login to Apple TV using specified login id."""
        # Do not use session.get_data(...) in login as that would end up in
        # an infinte loop.
        def _login_request():
            return self.http.get_data(
                self._mkurl('login?[AUTH]&hasFP=1',
                            session=False, login_id=True),
                headers=_DMAP_HEADERS)

        resp = await self._do(_login_request, is_login=True)
        self._session_id = parser.first(resp, 'mlog', 'mlid')

        _LOGGER.info('Logged in and got session id %s', self._session_id)
        return self._session_id

    async def get(self, cmd, daap_data=True, timeout=None, **args):
        """Perform a DAAP GET command."""
        def _get_request():
            return self.http.get_data(
                self._mkurl(cmd, *args),
                headers=_DMAP_HEADERS,
                timeout=timeout)

        await self._assure_logged_in()
        return await self._do(_get_request, is_daap=daap_data)

    def get_url(self, cmd, **args):
        """Expand the request URL for a request."""
        return self.http.base_url + self._mkurl(cmd, *args)

    async def post(self, cmd, data=None, timeout=None, **args):
        """Perform DAAP POST command with optional data."""
        def _post_request():
            headers = copy(_DMAP_HEADERS)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            return self.http.post_data(
                self._mkurl(cmd, *args),
                data=data,
                headers=headers,
                timeout=timeout)

        await self._assure_logged_in()
        return await self._do(_post_request)

    async def _do(self, action, retry=True, is_login=False, is_daap=True):
        resp, status = await action()
        if is_daap:
            resp = parser.parse(resp, lookup_tag)

        self._log_response(str(action.__name__) + ': %s', resp, is_daap)
        if 200 <= status < 300:
            return resp

        if not is_login:
            # If a request fails, try to login again before retrying
            _LOGGER.info('implicitly logged out, logging in again')
            await self.login()

        # Retry once if we got a bad response, otherwise bail out
        if retry:
            return (await self._do(
                action, False, is_login=is_login, is_daap=is_daap))

        raise exceptions.AuthenticationError(
            'failed to login: ' + str(status))

    def _mkurl(self, cmd, *args, session=True, login_id=False):
        url = '{}'.format(cmd.format(*args))
        parameters = []
        if login_id:
            if re.match(r'0x[0-9a-fA-F]{16}', self._login_id):
                parameters.append('pairing-guid={}'.format(self._login_id))
            else:
                parameters.append('hsgid={}'.format(self._login_id))
        if session:
            parameters.insert(0, 'session-id={}'.format(self._session_id))
        return url.replace('[AUTH]', '&'.join(parameters))

    async def _assure_logged_in(self):
        if self._session_id != 0:
            _LOGGER.debug('Already logged in, re-using seasion id %d',
                          self._session_id)
        else:
            await self.login()

    @staticmethod
    def _log_response(text, data, is_daap):
        if _LOGGER.isEnabledFor(logging.INFO):
            formatted = data
            if is_daap:
                formatted = parser.pprint(data, lookup_tag)
            _LOGGER.debug(text, formatted)
