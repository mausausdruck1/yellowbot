import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import config
import drive
import config as cf
import time
import rpmread
import sys
import drive
import sched
import mkmap
#GPIO.output(cf.motorL_forward, True)
#GPIO.output(cf.motorL_backward, True)
#GPIO.output(cf.motorR_forward, True)
#GPIO.output(cf.motorR_backward, False)
#drive.drive('R','F',10)
#drive.drive('L','F',10)

#l/r (speed mm/s, duty, direction, lasttime)

gears=[[cf.v,0,"F",0],[cf.v,0,"F",0]]
beta=0#rel. Kursrichtung soll

debug=1
state=0

        
def speedC(lr):
    global gears,debug
    this=gears[lr]
        
    ist=round(rpmread.rpm[lr]*cf.radius_rad*2.231*2/60/1000,1)#U/Min* mm => cm/s
    soll=this[0]
    
    pw=0
    if soll >0 and this[1]==0: # anfahren
        drive.drive(lr,this[2],cf.pwmin[lr])
        gears[lr]=[soll,cf.pwmin[lr],this[2], ist]
    elif soll==0:
        drive.drive(lr,this[2],0)
        gears[lr]=[soll,0,this[2], ist]
    elif soll>0 and this[1]>0 and ist>0: 
        pw=this[1]
        if ist>soll:
            pw=this[1]-4
            if pw<cf.pwmin[lr]:
                pw=cf.pwmin[lr]
            if debug:
                print('speedC: speeddown ',lr,soll,ist,pw) 
        elif ist<soll: 
            pw=this[1]+4;
            if pw>100:
                pw=100
            if debug:
                print('speedC: speedup ',lr,soll,ist,pw)                
        gears[lr]=[soll,pw,this[2], ist]       
        drive.drive(lr,this[2], pw)

    

def speedcontrol(s):
    global state
    speedC(0)
    speedC(1)
    mkmap.update(rpmread.s);
    rpmread.rpmreset(0)
    rpmread.rpmreset(1)
    adjust(s)
    if state:
        s.enter(0.3,3,speedcontrol,(s,))
        if mkmap.debug:
            s.enter(1,4,print,('map / s:',mkmap.map,rpmread.s))
    
   
    
def setstop():
    global gears,state
    state=0
    l=gears[0]
    l=[0,0,l[2],0];
    r=gears[1]
    r=[0,0,r[2],0];
    gears=[l,r]
    print("stopping...");
    if mkmap.debug:
        print('waylog:', mkmap.waylog)
    
def setstart(s):
    global gears, state
    mkmap.reset()
    state=1
    l=gears[0]
    l=[cf.v,0,l[2],0];
    r=gears[1]
    r=[cf.v,0,r[2],0];
    gears=[l,r]
    #s.enter(0.5,3, adjust,(s,))
    print("starting.................................");
    
def halfleft(s):
    global gears
    gears=[[0.8,0,"F",0],[1.2,0,"F",0]]
def left(s):
    global gears
    gears=[[0,0,"F",0],[0.8,0,"F",0]]
def leftturn(s):
    global gears
    gears=[[0.8,0,"B",0],[0.8,0,"F",0]]
    
def back(s):
    global gears
    gears=[[0.8,0,"B",0],[0.8,0,"B",0]]
    s.enter(1,2,forward,(s))
def forward(s):
    global gears, beta
    gears=[[cf.v,0,"F",0],[cf.v,0,"F",0]]

def adjust(s):
    global beta, gears, debug, state
    delta=beta-mkmap.map[3]
    l=gears[0];
    r=gears[1];
    c=0.05
    a=0.1
    b=0.1 # winkelfehlertol
    #wenn kleiner als Soll ist die  Seite schneller
    if mkmap.map[3] <(beta+b) and abs(r[0]-r[3])<a and abs(l[0]-l[3])<a:
        r=[r[0]-c,r[1]-1,r[2], r[3]];
        l=[l[0]+c,l[1]+1,l[2], l[3]];
        if debug:
            print("adjust corr r");
        gears=[l,r];
    if mkmap.map[3]>(beta-b) and abs(r[0]-r[3])<a and abs(l[0]-l[3])<a:
        l=[l[0]-c,l[1]-1,l[2],l[3]];
        r=[r[0]+c,r[1]+1,r[2],r[3]];
        if debug:
            print("adjust corr l");
        gears=[l,r];
    #if state:
    #    s.enter(0.4,3, adjust,(s,))
    
 
rpmread.rpmclean()    
rpmread.rpminit()                    


print(gears[1][3])
    

#drive.stop('R')
#drive.stop('L')
