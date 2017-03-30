import time
import math


class PID(object):
    def __init__(self, kp, ki, kd, reverse=False, min_out=0, max_out=100):
        self.last_input = 0
        self.output = 0
        self.setpoint = 0
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.reverse = reverse
        self.set_tunings(kp, ki, kd)

        self.last_update = time.time()

        self.max_out = max_out
        self.min_out = min_out

        self.enabled = True

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def update(self, in_value):
        if not self.enabled:
            return 0
        now = time.time()
        delta_time = now - self.last_update
        d_input = in_value - self.last_input
        error = self.setpoint - in_value
        iterm = self.ki*error*delta_time
        iterm = max(min(iterm, self.max_out), self.min_out)

        out = self.kp*error + iterm - self.kd*d_input/delta_time
        self.output = max(min(out, self.max_out), self.min_out)

        self.last_input = in_value
        self.last_update = now
        return self.output

    def set_tunings(self, kp=None, ki=None, kd=None):
        self.kp = math.fabs(kp or self.kp)
        self.ki = math.fabs(ki or self.ki)
        self.kd = math.fabs(kd or self.kd)

        if self.reverse:
            self.kp = -self.kp
            self.ki = -self.ki
            self.kd = -self.kd

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_direction(self, reverse=False):
        """When a bigger output makes decrease input, it is a reverse system"""
        self.reverse = reverse
        self.set_tunings()
