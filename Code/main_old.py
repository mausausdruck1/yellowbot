# by mausauftruck1

#init
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import config as cf
import time
import sys
import drive

# pin setup
GPIO.setup(cf.tasterRun, GPIO.IN)
GPIO.setup(cf.led[0], GPIO.OUT)

#Some prechecks
if GPIO.input(cf.tasterRun):
    print("Start-Taster allready high -- Massefehler?", GPIO.input(cf.tasterRun))
    exit()


# loop
looptime=0
runswitch=0;
schedul=[time.time(),0] # 1. Blink
schedulnext=[False,0]
GPIO.output(cf.led[0], 1)



while True:
    try:
        looptime=time.time()
        #### Programm standby/start        
        if time.time()-schedul[1] >0.5 and GPIO.input(cf.tasterRun) and runswitch==0:
            runswitch=1
            schedul[1]=time.time()
        if time.time()-schedul[1] >0.5 and GPIO.input(cf.tasterRun) and runswitch==1:
            runswitch=0
            schedul[1]=time.time()
            GPIO.output(cf.led[0], True)        
        if runswitch==0:
            continue;
        ################################ AKTIV
        #blink status
        if time.time()-schedul[0] >= 0.2:
            schedul[0]=time.time();
            GPIO.output(cf.led[0], schedulnext[0])
            if schedulnext[0]:
                schedulnext[0]=False
            else:
                schedulnext[0]=True;
                
        #         
        
        
        ############################### AKtivitaet ende
        ## loop ende        
        #print("timing",time.time()-looptime)
        
    except KeyboardInterrupt:
        print("Keybord Interrupt")       
        GPIO.cleanup()       
        exit()
        
