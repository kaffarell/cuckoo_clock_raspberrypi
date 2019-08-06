#ChangeDutyCycle: 2.5 = 0degree 7.5 = 90degree 12.5 = 180degree

import RPi.GPIO as GPIO
import time


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
    p.start(2.5)
    g.start(2.5)
    time.sleep(0.5)
    
    p.ChangeDutyCycle(12.5)
    time.sleep(2)
    for i in range(2):
        g.ChangeDutyCycle(12.5)
        time.sleep(2)
        g.ChangeDutyCycle(2.5)
        time.sleep(2)
    
    # set back to zero
    p.ChangeDutyCycle(2.5)
    g.ChangeDutyCycle(2.5)
    time.sleep(3)
    
    p.stop()
    g.stop()

if __name__ == "__main__":
    main()
    GPIO.cleanup(servo_pin_1)
    GPIO.cleanup(servo_pin_2)
    