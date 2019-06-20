# by mausauftruck1

#init
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import config as cf
import time
import sys
import drive
import sched
import drivecntrl as dc
# pin setup
GPIO.setup(cf.tasterRun, GPIO.IN)
GPIO.setup(cf.led[0], GPIO.OUT)

#Some prechecks
if GPIO.input(cf.tasterRun):
    print("Start-Taster allready high -- Massefehler?", GPIO.input(cf.tasterRun))
    exit()

runswitch=0;
GPIO.output(cf.led[0], 1)
# loop

#scheduler.enter(3, 1, print_event, ('second',))

def runblink(status):
    global runswitch
    if runswitch:
        GPIO.output(cf.led[0], status)
    if status and runswitch:
        s.enter(0.2,5,runblink,(False,))
    if status==False and runswitch:
        s.enter(0.2,5,runblink,(True,))
        
def readbutton():
    global runswitch
    if GPIO.input(cf.tasterRun) and runswitch==1:
        runswitch=0
        GPIO.output(cf.led[0], 1)
        s.enter(0.2,3,dc.setstop,()) #
        print('Status: Standby')
    elif GPIO.input(cf.tasterRun) and runswitch==0:
        runswitch=1
        s.enter(0.2,3,runblink,(False,))
        print('Status: run')
        s.enter(0.1,3,dc.setstart,(s,)) #
        s.enter(0.2,3,dc.speedcontrol,(s,))       
 
    s.enter(0.5,3,readbutton,())
    

# Scheduler Loop

s = sched.scheduler(time.time, time.sleep)
s.enter(0.5,3,readbutton,()) #Einstiegsfunktion
s.run()




