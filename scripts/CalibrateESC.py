#!/usr/bin/sudo python

import sys
import time
import argparse
import threading

import navio.pwm
import navio.util
import datetime


navio.util.check_apm()

PWM_OUTPUT = 3
SERVO_MIN = 1.05 #ms
SERVO_MAX = 1.95 #ms
SERVO_NOM = 1.500 #ms

def loop_for(seconds, func, *args):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    while True:
        if datetime.datetime.now() >= endTime:
            break
        func(*args)

def initialize(motors,freq=50):
    print("Frequency of ESCs %d"%freq)
    pwm = []
    for m in motors:
        pwm.append(navio.pwm.PWM(m))

    for i in range(len(pwm)):
        pwm[i].initialize()
        pwm[i].set_period(freq)
        pwm[i].enable()
    
    return pwm

def calibrate(motors,pwm):
    for i in range(len(pwm)):
        print "calibrating motor: "
        print  i
        print "\n"
        loop_for(3,pwm[i].set_duty_cycle, SERVO_MAX)
        loop_for(5,pwm[i].set_duty_cycle, SERVO_MIN)
        loop_for(3,pwm[i].set_duty_cycle,SERVO_MIN)
        loop_for(3,pwm[i].set_duty_cycle,SERVO_NOM)

def test(motors,pwm):

    for m in range(len(pwm)):
        
        loop_for(3,pwm[m].set_duty_cycle,SERVO_MIN)
        N = 4
        Nmax = 5
        dServo = float(SERVO_MAX - SERVO_MIN)/(Nmax)
        pwm_value = 0.0

        a = range(0,N+1)+range(N-1,-1,-1)
        for i in a:
            pwm_value = float(SERVO_MIN+i*dServo)
            print "pwm value: " + str(pwm_value) + "\n" 
            loop_for(5,pwm[m].set_duty_cycle,pwm_value)

def build_parser():
    """Creates parser for command line arguments """
    parser = argparse.ArgumentParser(description="Calibrate ESCs...")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose output")
    parser.add_argument('-m', '--motor',
                        help='Motor pinout',
                        required=True,
                        nargs=1,
                        type=str)
    parser.add_argument('-t','--test',
                        action='store_true',
                        help='Test a specific motor')
    parser.add_argument('-f','--frequency',
			help='ESC frequency',
			required=False,
			nargs=1,
			type=str,
			default='50')
    return parser


def validate_args(cmd_args):
    """ Validates the arguments parsed by the parser generated in the build_parser() function. We
        must always have a bag file, but other than the bag file, there are valid combinations of
        different arguments.
    """
    valid = cmd_args.motor is not None

    if not valid:
        print('Must specify a/all Motor Pinouts')

    print(cmd_args.motor)

    return valid

def main():
    """
    function to parse the arguments passed through terminal
    """
    # Parse the command line arguments
    argument_parser = build_parser()
    args = argument_parser.parse_args()
    if not validate_args(args):
        print('No valid arguments')
        sys.exit()

    if args.motor[0] == 'all':
        motor_ids = [0,1,2,3]
    else:
        if int(args.motor[0])>3:
            print("Motor pinout %d is not valid!"%int(args.motor[0]))
            sys.exit()
        else:
            motor_ids = [int(args.motor[0])]


    pwm = initialize(motor_ids,int(args.frequency[0]))
    if args.test:
        test(motor_ids,pwm)
    else:
        calibrate(motor_ids,pwm)
        test(motor_ids,pwm)
    

if __name__ == "__main__":
    main()
