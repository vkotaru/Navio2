#!/usr/bin/sudo python

import sys
import time

import navio.pwm
import navio.util
import datetime

navio.util.check_apm()

PWM_OUTPUT = 0
SERVO_MIN = 1.000 #ms
SERVO_MAX = 2.000 #ms
SERVO_NOM = 1.600 #ms

def loop_for(seconds, func, *args):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    while True:
        if datetime.datetime.now() >= endTime:
            break
        func(*args)

def main():
    pwm =  navio.pwm.PWM(PWM_OUTPUT)
    pwm.initialize()
    pwm.set_period(50)
    pwm.enable()

    loop_for(3, pwm.set_duty_cycle, SERVO_MAX)
    loop_for(5, pwm.set_duty_cycle, SERVO_MIN)
    loop_for(3, pwm.set_duty_cycle, SERVO_MIN)
    loop_for(3, pwm.set_duty_cycle, SERVO_NOM)

main()
