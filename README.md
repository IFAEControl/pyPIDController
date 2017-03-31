# PID Controller

Simple library that implements a PID Controller in Python

## Usage

    heater_pid = PIDController(kp=5, ki=3, kd=3)
    heater_pid.setpoint = 300
    
    while True:
        current_temp = get_current_temp()
        new_actuator_value = heater_pid.update(current_temp)
        change_actuator_power(new_actuator_value)
        time.sleep(1)

Check test/devices.py for an extended example