#ChangeDutyCycle: 2.5 = 0degree 7.5 = 90degree 12.5 = 180degree

import RPi.GPIO as GPIO
import time


# Pins of the servos
servo_pin_1 = 17

def main():
    # setup :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(servo_pin_1, GPIO.OUT)
    p = GPIO.PWM(servo_pin_1, 50)
    
    # movement :
    p.start(2.5)
    time.sleep(0.5)
    i = 3
    for i in range(12):
        p.ChangeDutyCycle(i)
        time.sleep(0.5)

    # p.ChangeDutyCycle(12.5)
    # time.sleep(4)
    i = 12
    for i in range(3):
        p.ChangeDutyCycle(i)
        time.sleep(0.5)
    
    
    p.stop()

if __name__ == "__main__":
    main()
    GPIO.cleanup(servo_pin_1)
    