import time
import datetime


class PIDController(object):
    """
    Simple PID Controller
    """

    def __init__(self, kp, ki=0, kd=0, setpoint=0, output_range=(0, 100)):
        self.last_in_value = 0
        self.output = 0
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_update = get_utc_ts()

        self.max_out = 0  # definition of attr at __init__
        self.min_out = 0  # definition of attr at __init__
        self.output_range = output_range

        self.enabled = True

        self.out_components = [0, 0, 0]
        self.delta_time = 0

        self.updates = 0

    def _set_output_range(self, output_range):
        self.max_out = output_range[1]
        self.min_out = output_range[0]

    def _get_output_range(self):
        return self.min_out, self.max_out

    output_range = property(_get_output_range, _set_output_range)

    def _get_status(self):
        return {'last_update_ts_utc': self.last_update,
                'last_update_ts': utc_ts_string(self.last_update),
                'last_delta_time': self.delta_time,
                'last_input_value': self.last_in_value,
                'constants': {'kp': self.kp,
                              'ki': self.ki,
                              'kd': self.kd},
                'output_components': {'p': self.out_components[0],
                                      'i': self.out_components[1],
                                      'd': self.out_components[2]},
                'output': self.output,
                'output_range': self.output_range,
                'updates': self.updates,
                'enabled': self.enabled}

    status = property(_get_status)

    def _clamp_term(self, value):
        return max(min(value, self.max_out), self.min_out)

    def update(self, in_value):
        now = get_utc_ts()
        self.delta_time = now - self.last_update
        input_value = in_value - self.last_in_value
        error = self.setpoint - in_value
        self.out_components[0] = self.kp * error
        self.out_components[1] = self.ki * error * self.delta_time
        self.out_components[2] = self.kd * input_value / self.delta_time
        out = self.out_components[0] + self.out_components[1] + self.out_components[2]
        self.output = self._clamp_term(out)

        self.last_in_value = in_value
        self.last_update = now

        self.updates += 1

        if not self.enabled:
            return 0
        return self.output


def get_utc_ts():
    now = datetime.datetime.utcnow()
    return time.mktime(now.timetuple()) + now.microsecond / 1e6


def utc_ts_string(ts, strformat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.utcfromtimestamp(ts).strftime(strformat)
