#ChangeDutyCycle: 2.5 = 0degree 7.5 = 90degree 12.5 = 180degree

import RPi.GPIO as GPIO
import time
import numpy


# Pins of the servos
servo_pin_1 = 8
servo_pin_2 = 13

def main():
    # setup :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(servo_pin_1, GPIO.OUT)
    GPIO.setup(servo_pin_2, GPIO.OUT)
    p = GPIO.PWM(servo_pin_1, 50)
    g = GPIO.PWM(servo_pin_2, 50)
    
    # movement :
    p.start(3)
    g.start(6)
    input()
    

    for a in numpy.arange(3, 11, 0.01):
        p.ChangeDutyCycle(a)
        time.sleep(0.005)


    time.sleep(2)
    
# crane
    

    for b in numpy.arange(6, 9, 0.01):
        g.ChangeDutyCycle(b)
        time.sleep(0.001)


    time.sleep(1)
    for c in numpy.arange(9, 4, -0.01):
        g.ChangeDutyCycle(c)
        time.sleep(0.001)


    time.sleep(1)
    for f in numpy.arange(4, 9, 0.01):
        g.ChangeDutyCycle(f)
        time.sleep(0.001)

    time.sleep(1)
    for h in numpy.arange(9, 4, -0.01):
        g.ChangeDutyCycle(h)
        time.sleep(0.001)
    
    time.sleep(1)

    for d in numpy.arange(4, 6, 0.01):
        g.ChangeDutyCycle(d)
        time.sleep(0.001)


# crane

    time.sleep(3)

    for e in numpy.arange(11, 3, -0.01):
        p.ChangeDutyCycle(e)
        time.sleep(0.005)




    
    p.stop()
    g.stop()

if __name__ == "__main__":
    main()
    GPIO.cleanup(servo_pin_1)
    GPIO.cleanup(servo_pin_2)
    