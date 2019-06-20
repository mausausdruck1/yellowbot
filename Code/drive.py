#FireHead Motorantriebs-Modul
#18.05.2019
#by Fabio Aufinger

import RPi.GPIO as GPIO
import config as cf

GPIO.setmode(GPIO.BCM)
GPIO.setup(cf.motorL_PWM, GPIO.OUT)
GPIO.setup(cf.motorR_PWM, GPIO.OUT)
GPIO.setup(cf.motorL_backward, GPIO.OUT)
GPIO.setup(cf.motorL_forward, GPIO.OUT)
GPIO.setup(cf.motorR_backward, GPIO.OUT)
GPIO.setup(cf.motorR_forward, GPIO.OUT)

PWML = GPIO.PWM(cf.motorL_PWM, cf.pwm_freq)
PWMR = GPIO.PWM(cf.motorR_PWM, cf.pwm_freq)
PWML.start(0)
PWMR.start(0)

def drive(motor, direction, speed):
    if motor==0:
        motor="L"
    if motor==1:
        motor="R";

    if motor == "L" and direction == "F":
        GPIO.output(cf.motorL_backward, False)
        GPIO.output(cf.motorL_forward, True)
        PWML.ChangeDutyCycle(speed)

    if motor == "L" and direction == "B":
        GPIO.output(cf.motorL_forward, False)
        GPIO.output(cf.motorL_backward, True)
        PWML.ChangeDutyCycle(speed)

    if motor == "R" and direction == "F":
        GPIO.output(cf.motorR_backward, False)
        GPIO.output(cf.motorR_forward, True)
        PWMR.ChangeDutyCycle(speed)

    if motor == "R" and direction == "B":
        GPIO.output(cf.motorR_forward, False)
        GPIO.output(cf.motorR_backward, True)
        PWMR.ChangeDutyCycle(speed)


def stop(motor):
    if motor==0:
        motor="L"
    if motor==1:
        motor="R";
    if motor == "L":
        GPIO.output(cf.motorL_backward, False)
        GPIO.output(cf.motorL_forward, False)
        PWML.stop()
        
    if motor == "R":
        GPIO.output(cf.motorR_backward, False)
        GPIO.output(cf.motorR_forward, False)
        PWMR.stop()