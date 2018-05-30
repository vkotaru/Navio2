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
    startTime = datetime.datetime.now()
    endTime = startTime + datetime.timedelta(seconds=seconds)

    while True:
        #currentTime = startTime - datetime.datetime.now()
    
        #print "time: " + str(currentTime.seconds) + "\n"
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

    N = 15
    Nmax = 20
    dServo = float(SERVO_MAX - SERVO_MIN)/(Nmax)

    pwm_value = 0.0

    a = range(0,N+1)+range(N-1,-1,-1)
    for i in a:
        pwm_value = float(SERVO_MIN+i*dServo)

        print "pwm value: " + str(pwm_value) + "\n"
        loop_for(5,pwm.set_duty_cycle,pwm_value)

        #print "pwm value: " + str(pwm_value) + "\n"
        #WAITING = 1
        #while WAITING:
        #rpm_value = raw_input("enter rpm value: \n")
        #weight_Value = raw_input("enter weigth value: \n")
        #thrust_value = raw_input("enter thrust value: \n")
        #torque_value = raw_input("enter torque value: \n")

        #str_value = str(pwm_value) + "\t " + rpm_value + "\t " + thrust_value + "\t " + torque_value + "\n"
        #fout.write(str_value)


    fout.close    
main()
