#!/usr/bin/env python

"""Function to calibrate ESCs 
    using code
"""

import sys
import time

import navio.pwm
import navio.util

def main():
    
    if ~length(sys.argv)>1:
        print"provide the pwm number connected to the ESC"
        sys.exit(1)

    navio.util.check_apm()

    PWM_OUTPUT = int(sys.argv[1])
    Motor_Reverse = 1.6
    Motor_Brake = 1.75
    Motor_Drag = 1.2
    Motor_Max = 2.0
    Motor_Min = 1.0
    Motor_Neutral = 1.5

    with navio.pwm.PWM(PWM_OUTPUT) as pwm:
        pwm.set_period(50)
        pwm.enable

        pwm.set_duty_cycle(Motor_Neutral)
        time.sleep(7)
        pwm.set_duty_cycle(Motor_Max)
        time.sleep(7)
        pwm.set_duty_cycle(Motor_Min)
        time.sleep(7)
        pwm.set_duty_cycle(Motor_Neutral)
        time.sleep(5)

        while (True):
            pwm.set_duty_cycle(1.75)

if __name__ == '__main__':
    main()
