import sys, time

import navio.rcinput
import navio.util

navio.util.check_apm()

rcin = navio.rcinput.RCInput()

while (True):

    for i in range(8):
        period = rcin.read(i)
        print "i="+ str(i) + " period =" + period

    time.sleep(1)
