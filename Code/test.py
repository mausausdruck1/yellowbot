import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()  
import config
import drive
import config as cf
import time
import rpmread
import sys
import drive
import sched
#GPIO.output(cf.motorL_forward, True)
#GPIO.output(cf.motorL_backward, True)
#GPIO.output(cf.motorR_forward, True)
#GPIO.output(cf.motorR_backward, False)
#drive.drive('R','F',10)
#drive.drive('L','F',10)

#l/r (speed mm/s, duty, direction, lasttime)

gears=[[1,0,"F"],[1,0,"F"]]
def speedC(lr):
    global gears
    this=gears[lr]
    ist=rpmread.rpm[lr]*cf.radius_rad*2.231*2/10/60/1000#U/Min* mm => cm/s
    rpmread.rpmreset(lr)
    soll=this[0]
    pw=0
    if soll >0 and this[1]==0: # anfahren
        drive.drive(lr,this[2],8)
        gears[lr]=[soll,8,this[2]]
    elif soll==0:
        drive.drive(lr,this[2],0)
        gears[lr]=[soll,0,this[2]]
    elif soll>0 and this[1]>0 and ist>0:
        if ist>soll:
            pw=this[1]-2
            if pw<8:
                pw=8
        else:
            pw=this[1]+2;
            if pw>100:
                pw=100
        gears[lr]=[soll,pw,this[2]]       
        drive.drive(lr,this[2], pw)    
        
    print(lr,soll,ist,pw)
    s.enter(0.5,3,speedC,(lr,))
    
rpmread.rpmclean()    
rpmread.rpminit()                    
s = sched.scheduler(time.time, time.sleep)
s.enter(0.2,3,speedC,(0,)) #Einstiegsfunktion
s.enter(0.2,3,speedC,(1,)) #Einstiegsfunktion
s.run();

    

#drive.stop('R')
#drive.stop('L')