from pywink.devices.base import WinkDevice


# pylint: disable=too-many-public-methods
class WinkAirConditioner(WinkDevice):
    """
    Represents a Wink air conditioner.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkAirConditioner, self).__init__(device_state_as_json, api_interface)

    def state(self):
        return self.current_mode()

    def modes(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        modes = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'mode':
                modes = field.get('choices')
        return modes

    def current_mode(self):
        return self._last_reading.get('mode')

    def current_temperature(self):
        return self._last_reading.get('temperature')

    def current_max_set_point(self):
        return self._last_reading.get('max_set_point')

    def current_fan_speed(self):
        return self._last_reading.get('fan_speed')

    def is_on(self):
        return self._last_reading.get('powered', False)

    def schedule_enabled(self):
        return self._last_reading.get('schedule_enabled')

    def total_consumption(self):
        # This is the total consumption of watts
        return self._last_reading.get('consumption')

    def set_schedule_enabled(self, state):
        """
        :param state: a boolean True (on) or False (off)
        :return: nothing
        """
        desired_state = {"schedule_enabled": state}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_ac_fan_speed(self, speed):
        """
        :param speed: a float from 0.0 to 1.0 (0 - 100%)
        :return: nothing
        """
        desired_state = {"fan_speed": speed}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_operation_mode(self, mode):
        """
        :param mode: a string one of ["off", "auto_eco", "cool_only", "fan_only"]
        :return: nothing
        """
        if mode == "off":
            desired_state = {"powered": False}
        else:
            desired_state = {"powered": True, "mode": mode}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_temperature(self, max_set_point=None):
        """
        :param temperature: a float for the temperature value in celsius
        :return: nothing
        """
        desired_state = {}

        if max_set_point:
            desired_state['max_set_point'] = max_set_point

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)
