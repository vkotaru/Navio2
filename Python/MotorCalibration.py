#!/usr/bin/sudo python

import sys
import time

import navio.pwm
import navio.util
import datetime

navio.util.check_apm()

PWM_OUTPUT = 3
SERVO_MIN = 1.060 #ms
SERVO_MAX = 1.860 #ms
SERVO_NOM = 1.500 #ms

def loop_for(seconds, func, *args):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    while True:
        if datetime.datetime.now() >= endTime:
            break
        func(*args)

def main():

    pwm = []
    for i in range(4):
        pwm.append(navio.pwm.PWM(i))
        pwm[i].initialize()
        pwm[i].set_period(50)
        pwm[i].enable()


    for i in range(4):
        loop_for(3,pwm[i].set_duty_cycle, SERVO_MAX)
        loop_for(5,pwm[i].set_duty_cycle, SERVO_MIN)
        loop_for(3,pwm[i].set_duty_cycle,SERVO_MIN)
        loop_for(3,pwm[i].set_duty_cycle,SERVO_NOM)


main()
