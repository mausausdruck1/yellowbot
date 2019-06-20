#config

debug=True
#Track
XLimits = (-5, 5)
YLimits = (0, 10)
steps = 0.1

#Motoren-Richtung
motorL_forward = 24
motorL_backward = 23
motorR_forward = 25
motorR_backward = 4


#Motoren-PWM
motorL_PWM = 5 #p18
motorR_PWM = 6 #p22

pwmin=[19,20]
pwm_freq=70
v=1.2
vmax=3
#Kamera


#Ultraschall
sonicL=[7,8]
sonicM=[0]
sonicR=[0]

#LEDs
led=[13]#p33

#startStop Taster
tasterRun=19# 35

#Drehzahlsensoren
rpmL = 21#13
rpmR = 20#15
radius_rad = 45 #Radius Rad in mm
Drehscheibe = 20 # Anzahl Löcher Drehscheibe (Standard: 20)
waymulti=radius_rad*3.142*2/1000*10 #Multiplikator zu cm
#Gyro
