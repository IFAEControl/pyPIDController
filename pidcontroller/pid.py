import time
import math


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

        self.last_update = time.time()

        self.max_out = output_range[1]
        self.min_out = output_range[0]

        self.enabled = True

        self.terms = [0, 0, 0]

    def _set_setpoint(self, setpoint):
        self._setpoint = setpoint

    def _get_setpoint(self):
        return self._setpoint
    setpoint = property(_get_setpoint, _set_setpoint)

    def _clamp_term(self, value):
        return max(min(value, self.max_out), self.min_out)

    def update(self, in_value):
        now = time.time()
        delta_time = now - self.last_update
        input_value = in_value - self.last_in_value
        error = self.setpoint - in_value
        self.terms[0] = self.kp*error
        self.terms[1] = self.ki*error*delta_time
        self.terms[2] = self.kd*input_value/delta_time
        out = self.terms[0] + self.terms[1] + self.terms[2]
        self.output = self._clamp_term(out)

        self.last_in_value = in_value
        self.last_update = now

        if not self.enabled:
            return 0
        return self.output

