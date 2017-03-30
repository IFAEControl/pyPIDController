#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 3/30/17
# @Author  : Otger Ballester (otger@ifae.es)
import time
import threading
from pidcontroller.pid import PID


class System(object):
    def __init__(self, init_temp=275, temp_amb=295, specific_heat=4.1868, mass=10):
        self.temp = init_temp
        self.temp_amb = temp_amb
        self.c = specific_heat
        self.m = mass
        self.w = 100
        self.percent = 0
        self.w_applied = 0
        self.lost_heat = 0
        self.applied_heat = 0
        self.delta_time = 0
        self.last_update = time.time()
        self.timer = None

    def update(self):
        now = time.time()
        self.delta_time = now - self.last_update
        self.last_update = now

        self.lost_heat = 0.1*(self.temp - self.temp_amb)*self.delta_time
        self.applied_heat = -self.w_applied * self.delta_time

        self.temp += (self.applied_heat - self.lost_heat)/(self.m*self.c)

        self.timer = threading.Timer(0.1, self.update)
        #print(str([now, self.lost_heat, self.applied_heat]))
        self.timer.start()

    def apply_heat(self, percent):
        self.percent = percent
        self.w_applied = self.w * percent/100

    def start(self):
        if self.timer is None:
            self.update()


if __name__ == "__main__":
    s = System()
    s.start()
    pid = PID(kp=5, ki=0.2, kd=1.5)
    pid.set_setpoint(200)
    pid.set_direction(reverse=True)


    def update():
        output = pid.update(s.temp)
        s.apply_heat(output)
        print('{0} - {1} - {2}'.format(time.time(), output, str([s.temp, s.applied_heat, s.lost_heat, s.delta_time])))
        timer = threading.Timer(2, update)
        timer.start()

    update()
    time.sleep(100)
