#ChangeDutyCycle: 2.5 = 0degree 7.5 = 90degree 12.5 = 180degree

import RPi.GPIO as GPIO
import time
import numpy


# Pins of the servos
servo_pin_1 = 17

def main():
    # setup :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(servo_pin_1, GPIO.OUT)
    p = GPIO.PWM(servo_pin_1, 50)
    
    # movement :

    p.start(9.6)
    time.sleep(1)



    for i in numpy.arange(9.6, 2.5, -0.01):
        p.ChangeDutyCycle(i)
        time.sleep(0.002)
    
    time.sleep(3)


    for i in numpy.arange(2.5, 9.6, 0.01):
        p.ChangeDutyCycle(i)
        time.sleep(0.002)
    
    
    p.stop()

if __name__ == "__main__":
    main()
    GPIO.cleanup(servo_pin_1)
    