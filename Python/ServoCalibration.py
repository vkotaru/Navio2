#!/usr/bin/sudo python

import sys
import time

import navio.pwm
import navio.util
import datetime

navio.util.check_apm()

PWM_OUTPUT = 1 
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
    pwm =  navio.pwm.PWM(PWM_OUTPUT)
    pwm.initialize()
    pwm.set_period(50)
    pwm.enable()

    fout = open('motor_calibration.txt','w')
    first_line = "pwm[ms]\t rpm\t thrust[kgf]\t torque[Nm]"
    fout.write(first_line)

    loop_for(3,pwm.set_duty_cycle, SERVO_MAX)
    loop_for(5,pwm.set_duty_cycle, SERVO_MIN)
    loop_for(3,pwm.set_duty_cycle,SERVO_MIN)

    N = 20.0
    dServo = float(SERVO_MAX - SERVO_MIN)/N

    pwm_value = 0.0

    a = range(0,N+1)+range(N-1,-1,-1)
    for i in range(0,N):
        pwm_value = SERVO_MAX-i*dServo
        pwm.set_duty_cycle(pwm_value)

        print "pwm value: " + str(pwm_value) + "\n"

        rpm_value = raw_input("enter rpm value: \n")
        #weight_Value = raw_input("enter weigth value: \n")
        thrust_value = raw_input("enter thrust value: \n")
        torque_value = raw_input("enter torque value: \n")

        str_value = str(pwm_value) + "\t " + rpm_value + "\t " + thrust_value + "\t " + torque_value + "\n"
        fout.write(str_value)


    fout.close    
main()
