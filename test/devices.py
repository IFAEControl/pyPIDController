#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 3/30/17
# @Author  : Otger Ballester (otger@ifae.es)
import time
import threading
from pidcontroller import PIDController


class System(object):
    """Simple system that simulates a glass of water with an actuator"""
    def __init__(self, init_temp=275, temp_amb=295, specific_heat=4.1868, mass=10, update_time=0.1):
        self.temp = init_temp
        self.temp_amb = temp_amb
        self.c = specific_heat
        self.m = mass
        self.actuator_power = 100
        self.percent = 0
        self.w_applied = 0
        self.lost_heat = 0
        self.applied_heat = 0
        self.delta_time = 0
        self.last_update = time.time()
        self.timer = None
        self.update_time = update_time

    def update(self):
        now = time.time()
        self.delta_time = now - self.last_update
        self.last_update = now

        self.lost_heat = 0.1*(self.temp - self.temp_amb)*self.delta_time
        self.applied_heat = self.w_applied * self.delta_time

        self.temp += (self.applied_heat - self.lost_heat)/(self.m*self.c)

        self.timer = threading.Timer(self.update_time, self.update)
        self.timer.start()

    def change_actuator(self, percent):
        self.percent = percent
        self.w_applied = self.actuator_power * percent / 100

    def start(self):
        if self.timer is None:
            self.update()


if __name__ == "__main__":
    cooler_system = System()
    cooler_system.actuator_power = -50  # negative, because it is a cooler
    cooler_system.start()

    cooler_pid = PIDController(kp=-5, ki=-3, kd=-3)  # negative values because it is a cooler
    cooler_pid.setpoint = 200

    heater_system = System()
    heater_system.actuator_power = 100
    heater_system.start()
    heater_pid = PIDController(kp=5, ki=3, kd=3)
    heater_pid.setpoint = 300

    def update():
        cooler_system.change_actuator(cooler_pid.update(cooler_system.temp))
        heater_system.change_actuator(heater_pid.update(heater_system.temp))
        print('{0:.2f} - {1:.2f} ({2:.1f} + {3:.1f} + {4:.1f}) -  {5:.2f} - {6:.2f}  ({7:.1f} + {8:.1f} + {9:.1f})'.format(
            cooler_system.temp, cooler_system.percent, cooler_pid.out_components[0], cooler_pid.out_components[1], cooler_pid.out_components[2],
            heater_system.temp, heater_system.percent, heater_pid.out_components[0], heater_pid.out_components[1], heater_pid.out_components[2]))
        # print(cooler_pid.status)
        timer = threading.Timer(2, update)
        timer.start()

    update()
    time.sleep(100)
    print('Change setpoints')
    cooler_pid.setpoint = 250
    heater_pid.setpoint = 295
